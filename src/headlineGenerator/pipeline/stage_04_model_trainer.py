from headlineGenerator.components.model_trainer import ModelTrainer
from headlineGenerator.config.configuration import ConfigurationManager


class ModelTrainerPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        model_trainer_config = self.config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train()
