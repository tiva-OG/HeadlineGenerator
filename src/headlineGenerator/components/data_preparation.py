import os
import re
from headlineGenerator.entity import DataPreparationConfig
from datasets import load_dataset, concatenate_datasets, DatasetDict


class DataPreparation:
    def __init__(self, config: DataPreparationConfig):
        self.config = config
        self.news_dataset = DatasetDict()
        self.business_file = os.path.join(self.config.data_dir, "business_contents.csv")
        self.entertainment_file = os.path.join(self.config.data_dir, "entertainment_contents.csv")
        self.sports_file = os.path.join(self.config.data_dir, "sports_contents.csv")

    @staticmethod
    def add_category(example, category):
        return {"category": category}

    @staticmethod
    def build_full_story(example):
        if example["summary"] is None:
            return {"full_story": example["main_story"]}

        return {"full_story": example["summary"] + " " + example["main_story"]}

    @staticmethod
    def edit_writer(example):
        if example["writer"] is None:
            return {"writer": "UNK"}
        else:
            return {"writer": re.sub("by.", "", example["writer"].lower()).strip()}

    @staticmethod
    def lowercase_content(example):
        return {"headline": example["headline"].lower(), "full_story": example["full_story"].lower()}

    @staticmethod
    def compute_story_length(example):
        return {"story_length": len(example["full_story"].split())}

    def load_data(self):
        business_dataset = load_dataset("csv", data_files=self.business_file, split="train")
        entertainment_dataset = load_dataset("csv", data_files=self.entertainment_file, split="train")
        sports_dataset = load_dataset("csv", data_files=self.sports_file, split="train")

        # add category to datasets
        business_dataset = business_dataset.map(self.add_category, fn_kwargs={"category": "business"})
        entertainment_dataset = entertainment_dataset.map(self.add_category, fn_kwargs={"category": "entertainment"})
        sports_dataset = sports_dataset.map(self.add_category, fn_kwargs={"category": "sports"})

        # concatenate data
        news_dataset = concatenate_datasets([business_dataset, entertainment_dataset, sports_dataset])
        self.news_dataset = news_dataset.shuffle(seed=84)

    def clean_data(self):
        # remove any content with no story
        self.news_dataset = self.news_dataset.filter(lambda x: x["main_story"] is not None)

        # encode the `category` column
        self.news_dataset = self.news_dataset.class_encode_column("category")

        # create a full story by combining the summary and main story
        self.news_dataset = self.news_dataset.map(self.build_full_story)

        # edit content writers, removing `by.` from their names
        self.news_dataset = self.news_dataset.map(self.edit_writer)

        # convert all headlines and stories to lowercase
        self.news_dataset = self.news_dataset.map(self.lowercase_content)

        # compute length of each story
        self.news_dataset = self.news_dataset.map(self.compute_story_length)

        # remove contents > 1000 words in `story_length`
        self.news_dataset = self.news_dataset.filter(lambda x: x["story_length"] < 1000)

    def split_and_save(self):
        # remove unwanted columns
        news_dataset_clean = self.news_dataset.remove_columns(
            ["last_update", "summary", "editor", "writer", "main_story", ])

        split_data = news_dataset_clean.train_test_split(train_size=0.7, seed=84)
        val_n_test = split_data["test"].train_test_split(train_size=0.4, seed=84)
        split_data["validation"] = val_n_test["train"]
        split_data["test"] = val_n_test["test"]

        split_data.save_to_disk(self.config.save_dir)
