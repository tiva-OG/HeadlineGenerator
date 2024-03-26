import torch
import pandas as pd
from tqdm import tqdm
from datasets import load_from_disk, load_metric
from headlineGenerator.entity import ModelEvaluationConfig
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    @staticmethod
    def generate_batches(list_of_elements, batch_size):
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i: i + batch_size]

    def calculate_metric(self, dataset, metric, model, tokenizer, batch_size, column_story, column_headline):
        story_batches = list(self.generate_batches(dataset[column_story], batch_size))
        target_batches = list(self.generate_batches(dataset[column_headline], batch_size))

        for story_batch, target_batch in tqdm(zip(story_batches, target_batches), total=len(story_batches)):
            inputs = tokenizer(story_batch, max_length=1024, truncation=True, padding="max_length", return_tensors="pt")
            headlines = model.generate(
                input_ids=inputs["input_ids"].to(self.device),
                attention_mask=inputs["attention_mask"].to(self.device),
                max_length=30,
                length_penalty=0.8,
                num_beams=8
            )
            '''`length_penalty` ensures that the model does not generate sequences that are ...'''

            decoded_headlines = [tokenizer.decode(h, skip_special_tokens=True, clean_up_tokenization_spaces=True) for h
                                 in headlines]
            decoded_headlines = [h.replace("", " ") for h in decoded_headlines]

            metric.add_batch(predictions=[decoded_headlines], references=[target_batches])

        score = metric.compute()

        return score

    def evaluate(self):
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(self.device)
        news_dataset = load_from_disk(self.config.data_path)

        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        rouge_metric = load_metric("rouge")

        score = self.calculate_metric(news_dataset["test"], rouge_metric, model, tokenizer, 2, "full_story", "headline")

        rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)
        df = pd.DataFrame(rouge_dict, index=["t5-small"])
        df.to_csv(self.config.metrics_file, index=False)
