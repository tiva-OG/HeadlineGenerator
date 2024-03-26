from datasets import load_from_disk
from transformers import AutoTokenizer
from headlineGenerator.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.checkpoint)

    def transform(self, examples):
        model_inputs = self.tokenizer(examples["full_story"], max_length=1024, truncation=True)
        labels = self.tokenizer(examples["headline"], max_length=128, truncation=True)

        model_inputs["labels"] = labels["input_ids"]

        return model_inputs

    def transform_and_save(self):
        news_dataset = load_from_disk(self.config.data_dir)
        news_dataset = news_dataset.map(self.transform, batched=True)
        news_dataset.save_to_disk(self.config.save_dir)
