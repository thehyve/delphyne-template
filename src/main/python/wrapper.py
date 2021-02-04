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

        # given a generator function, the batch transformation will insert 10 records at a time
        self.execute_batch_transformation(sample_batch_source_table_to_condition_occurrence,
                                          batch_size=3)

        self.execute_sql_file('sample_script.sql')

    def run(self):
        # Prepare source
        self.create_schemas()
        self.drop_cdm()
        self.create_cdm()

        # Load (custom) vocabularies and source_to_concept_map tables
        self.vocab_manager.standard_vocabularies.load()
        self.vocab_manager.load_custom_vocab_and_stcm_tables()

        # Transform source data to the OMOP CDM
        self.transform()

        # Log/write overview of transformations and sources
        self.summarize()
