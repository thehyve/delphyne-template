# Copyright 2020 The Hyve
#
# Licensed under the GNU General Public License, version 3,
# or (at your option) any later version (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.gnu.org/licenses/
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# !/usr/bin/env python3

from pathlib import Path
import logging
from omop_etl_wrapper import Wrapper as BaseWrapper
from src.main.python.transformation import *
from src.main.python.model.sourcedata import SourceData # TODO: use local version for the moment, will be made general (for data files & database)
from src.main.python.util import VariableConceptMapper # TODO: add to package?
from src.main.python.util import OntologyConceptMapper # TODO: add to package?
from src.main.python.util import RegimenExposureMapper # TODO: add to package?


logger = logging.getLogger(__name__)

class Wrapper(BaseWrapper):

    def __init__(self, config):
        super().__init__(config)
        # Load config settings
        self.source_folder            = Path(config['run_options']['source_data_folder'])
        self.path_mapping_tables      = Path('./resources/mapping_tables')
        self.path_custom_vocabularies = Path('./resources/custom_vocabularies')
        self.path_sql_transformations = Path('./src/main/sql')
        self.skip_vocabulary_loading  = False
        # Load data to objects
        # self.variable_concept_mapper = VariableConceptMapper(self.path_mapping_tables)
        # self.ontology_concept_mapper = OntologyConceptMapper(self.path_mapping_tables)
        # self.regimen_exposure_mapper = RegimenExposureMapper(self.path_mapping_tables)
        # NOTE: replace the following with project-specific source table names!
        self.sample_source_table = None


    def transform(self):

        # NOTE: replace the following with project-specific transformations from the python/transformations/ or sql/ folder!
        # make sure execution follows order of table dependencies (see cdm model)
        self.execute_transformation(dm_to_person)
        # self.execute_transformation(sample_source_table_to_person)
        # self.execute_sql_file(self.path_sql_transformations / 'sample_script.sql')


    def run(self):

        # self.start_timing()

        logger.info('{:-^100}'.format(' Source Counts '))
        # self.log_tables_rowcounts(self.source_folder)

        logger.info('{:-^100}'.format(' Setup '))

        # Prepare source
        self.create_schemas()
        self.drop_cdm()
        self.create_cdm()

        # Load custom concepts
        if not self.skip_vocabulary_loading:
            logger.info('Loading custom concepts')
            self.create_custom_vocabulary()

        # Load stem tables
        self.truncate_stcm_table()
        self.load_stcm()

        # Load source data

        logger.info('{:-^100}'.format(' ETL '))

        # These queries are cdm6 specific
        # self.stem_table_to_domains()

        self.transform()

        self.etl_stats.write_summary_files()
        self.etl_stats.log_summary()


        # self.log_summary()
        # self.log_runtime()

        # TODO: can this be made into a general function, or too project-specific? remove?
        try:
            self.execute_sql_query('GRANT INSERT, SELECT, UPDATE, DELETE, REFERENCES, TRIGGER ON ALL TABLES IN SCHEMA omopcdm TO ohdsi_app;', verbose=False)
            self.execute_sql_query('GRANT ALL ON ALL TABLES IN SCHEMA omopcdm TO ohdsi_admin;', verbose=False)
            logger.info("Permissions granted to HONEUR admin and app roles")
        except:
            logger.error("Failed to grant permissions to HONEUR admin and app roles")

    # TODO: change the following to load these programmatically from a source data folder?
    # NOTE: replace the following with project-specific source tables and function names!
    def get_sample_source_table(self):
        if not self.sample_source_table:
            self.sample_source_table = SourceData(self.source_folder / 'sample_source_table.csv')
        return self.sample_source_table
    
    # TODO: make this a base Wrapper method? since used only once during setup, I would actually make the method
    def do_skip_vocabulary_loading(self, skip_vocab=True):
        self.skip_vocabulary_loading = skip_vocab

    # TODO: add this to Wrapper methods? note that any custom vocabulary will be available in resources/custom_vocabularies,
    #  so rewriting the details here is completely unnecessary
    def create_custom_vocabulary(self):
        session = self.db.get_new_session()

        if not session.query(Vocabulary).get('Honeur'): # TODO: get this from XXX_vocabulary.tsv
            session.add(
                Vocabulary(
                    vocabulary_id='Honeur',
                    vocabulary_concept_id=0,  # We could make separate concept and link it
                    vocabulary_name='HONEUR',
                    vocabulary_reference='HONEUR',
                    vocabulary_version='APRIL 2019'
                )
            )

        for concept_class_id in ['Combination Therapy', 'Honeur Class']: # TODO: get this from XXX_concept_class.tsv
            if not session.query(ConceptClass).get(concept_class_id):
                session.add(
                    ConceptClass(
                        concept_class_id=concept_class_id,
                        concept_class_concept_id=0,  # We could make separate concept and link it
                        concept_class_name=concept_class_id
                    )
                )

        session.commit()
        session.close()
        self.load_concept_from_csv(self.path_custom_vocabularies)
