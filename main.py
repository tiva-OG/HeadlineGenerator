from headlineGenerator.logging import logger
from headlineGenerator.pipeline.stage_01_data_scraper import DataScraperPipeline
from headlineGenerator.pipeline.stage_02_data_preparation import DataPreparationPipeline
from headlineGenerator.pipeline.stage_03_data_transformation import DataTransformationPipeline
from headlineGenerator.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from headlineGenerator.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline


def main_template(stage_name, pipeline_class):
    try:
        logger.info(f"<<<<< {stage_name} begun >>>>>")
        pipeline = pipeline_class()
        pipeline.main()
        logger.info(f"<<<<< {stage_name} completed >>>>>")
        logger.info("-x-" * 30)
    except Exception as e:
        logger.exception(e)
        raise e


##################################################################
# main_template("Data-Scraper STAGE", DataScraperPipeline)
##################################################################
# main_template("Data-Preparation STAGE", DataPreparationPipeline)
##################################################################
# main_template("Data-Transformation STAGE", DataTransformationPipeline)
##################################################################
# main_template("Model-Trainer STAGE", ModelTrainerPipeline)
##################################################################
main_template("Model-Evaluation STAGE", ModelEvaluationPipeline)
##################################################################
