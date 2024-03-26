from headlineGenerator.config.configuration import ConfigurationManager
from headlineGenerator.components.data_preparation import DataPreparation


class DataPreparationPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        data_preparation_config = self.config.get_data_preparation_config()
        data_preparation = DataPreparation(config=data_preparation_config)
        data_preparation.load_data()
        data_preparation.clean_data()
        data_preparation.split_and_save()
