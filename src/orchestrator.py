"""Orchestration of the ETL pipeline for farms and maps 

- extraction from transcription data & transformation into farms/extraction of map data
- storage of farms & maps in persistent cache
- transformation of cached data into Discovery-schema JSON
- rendering of JSONs
"""
from abc import ABC, abstractmethod


class SurveyProcessor(ABC):
    # Template method defining the overall process
    def process_survey(self):
        self.extract_data()
        self.cache_data()
        self.build_documents()
        self.write_documents()
        self.zip_documents()

    # Common methods
    def cache_data(self):
        print("Writing data to cache")

    def write_documents(self):
        print("Writing data to JSONs")

    def zip_documents(self):
        print("Zipping the JSONs")

    @abstractmethod
    def extract_data(self):
        """extract & transform data from single input file
        """

    @abstractmethod
    def build_documents(self):
        """retrieve data from cache corresponding to input file and transform into JSONs
        """

# Concrete subclass for procesing farm survey forms
class FarmProcessor(SurveyProcessor):
    def extract_data(self):
        print("Run src.farm_harvester")

    def build_documents(self):
        print("Run src.farm_publisher.build_catalogue_documents")

# Concrete subclass for map sheet data
class MapProcessor(SurveyProcessor):
    def extract_data(self):
        print("Run src.map_maker")

    def build_documents(self):
        print("Run src.map_publisher.build_catalogue_documents")

if __name__ == '__main__':
    print('\nProcessing forms:')
    farm_processor = FarmProcessor()
    map_processor = MapProcessor()

    farm_processor.process_survey()
    map_processor.process_survey()