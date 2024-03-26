from headlineGenerator.config.configuration import ConfigurationManager
from headlineGenerator.components.data_transformation import DataTransformation


class DataTransformationPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        data_transformation_config = self.config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.transform_and_save()
