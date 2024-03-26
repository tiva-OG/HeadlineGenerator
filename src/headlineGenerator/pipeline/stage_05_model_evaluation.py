from headlineGenerator.components.model_evaluation import ModelEvaluation
from headlineGenerator.config.configuration import ConfigurationManager


class ModelEvaluationPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        model_evaluation_config = self.config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()
