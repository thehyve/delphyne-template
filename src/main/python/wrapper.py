import logging

from delphyne import Wrapper as BaseWrapper
from delphyne.config.models import MainConfig

from src.main.python import cdm
from src.main.python.transformation import *


logger = logging.getLogger(__name__)


class Wrapper(BaseWrapper):
    cdm = cdm

    def __init__(self, config: MainConfig):
        super().__init__(config, cdm)

    def transform(self):
        # Replace the following with project-specific transformations
        # from python/transformations/ or sql/ folder!
        self.execute_transformation(dm_to_person)
        self.execute_transformation(sample_source_table_to_person)
        self.execute_transformation(sample_source_table_to_condition_occurrence)
        self.execute_sql_file('sample_script.sql')

    def run(self):
        # Prepare source
        self.create_schemas()
        self.drop_cdm()
        self.create_cdm()

        # Load vocabularies and source_to_concept_map tables
        self.vocab_manager.load_standard_vocabularies()
        self.vocab_manager.load_custom_vocabularies()
        self.vocab_manager.load_stcm()

        # Transform source data to the OMOP CDM
        self.transform()

        # Log/write overview of transformations and sources
        self.summarize()
