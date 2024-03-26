from headlineGenerator.constants import *
from headlineGenerator.utils.common import read_yaml, create_directories
from headlineGenerator.entity import (DataScraperConfig, DataPreparationConfig)


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILEPATH, params_filepath=PARAMS_FILEPATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_scraper_config(self) -> DataScraperConfig:
        config = self.config.data_scraper

        create_directories([config.root_dir])

        data_scraper_config = DataScraperConfig(
            root_dir=config.root_dir,
            save_dir=config.save_dir,
            source_url=config.source_url,
            categories=config.categories,
            max_pages=config.max_pages
        )

        return data_scraper_config

    def get_data_preparation_config(self) -> DataPreparationConfig:
        config = self.config.data_preparation

        create_directories([config.root_dir])

        data_preparation_config = DataPreparationConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            save_dir=config.save_dir,
        )

        return data_preparation_config
