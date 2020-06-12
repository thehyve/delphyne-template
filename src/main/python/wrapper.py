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
import yaml

from omop_etl_wrapper import Wrapper as BaseWrapper # TODO: check import location
from omop_etl_wrapper.cdm import hybrid # TODO: customize CDM version
from src.main.python.transformation import *
from src.main.python.model.SourceData import SourceData # TODO: use local version for the moment, will be made general (for data files & database)
from src.main.python.util import VariableConceptMapper # TODO: add to package?
from src.main.python.util import OntologyConceptMapper # TODO: add to package?
from src.main.python.util import RegimenExposureMapper # TODO: add to package?

logger = logging.getLogger(__name__)

class Wrapper(BaseWrapper):

    def __init__(self, config):
        super().__init__(database=config['database'], cdm=hybrid, sql_parameters=config['sql_parameters'])
        # load config settings
        self.source_folder = Path(config['file_paths']['path_source_folder'])
        self.path_mapping_tables = Path(config['file_paths']['path_mapping_tables'])
        self.path_custom_vocabularies = Path(config['file_paths']['path_custom_vocabularies'])
        self.skip_vocabulary_loading = config['custom_vocabulary_loading'].getboolean('skip_vocabulary_loading', fallback=True)
        # load data to objects
        self.variable_concept_mapper = VariableConceptMapper(self.path_mapping_tables)
        self.ontology_concept_mapper = OntologyConceptMapper(self.path_mapping_tables)
        self.regimen_exposure_mapper = RegimenExposureMapper(self.path_mapping_tables)
        # TODO: better way of doing this, e.g. systematically add all available from source folder?
        # NOTE: replace the following with project-specific source table names!
        self.sample_source_table = None

    # TODO: make this a base Wrapper method? since used only once during setup, I would actually make the method
    def do_skip_vocabulary_loading(self, skip_vocab=True):
        self.skip_vocabulary_loading = skip_vocab

    def run(self):

        self.start_timing()

        logger.info('{:-^100}'.format(' Source Counts '))
        self.log_tables_rowcounts(self.source_folder)

        logger.info('{:-^100}'.format(' Setup '))

        # Prepare source
        self.drop_cdm()
        self.create_cdm()

        # Load custom concepts
        if not self.skip_vocabulary_loading:
            logger.info('Loading custom concepts')
            self.create_custom_vocabulary()

        # Transformations - make sure execution follows order of table dependencies (see cdm model)
        logger.info('{:-^100}'.format(' ETL '))
        # NOTE: replace the following with project-specific transformations from the transformations/ folder!
        self.execute_transformation(sample_source_table_to_person)
        self.execute_sql_file('./src/main/sql/sample_script.sql')

        self.log_summary()
        self.log_runtime()

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
