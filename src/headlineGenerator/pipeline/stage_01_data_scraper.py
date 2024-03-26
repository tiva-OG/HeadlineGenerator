from headlineGenerator.components.data_scraper import DataScraper
from headlineGenerator.config.configuration import ConfigurationManager


class DataScraperPipeline:
    def __init__(self):
        self.config = ConfigurationManager()

    def main(self):
        data_scraper_config = self.config.get_data_scraper_config()
        data_scraper = DataScraper(config=data_scraper_config)
        data_scraper.scrape_data()
