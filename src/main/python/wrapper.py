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

from ohdsi_etl_wrapper import Wrapper as BaseWrapper
from src.main.python.cdm_custom import TreatmentLine # only custom tables, other provided within Wrapper class
from src.main.python.transformation import *
# TODO: where to import these from, will also be part of the package?
from src.main.python.model.SourceData import SourceData
from src.main.python.util import VariableConceptMapper
from src.main.python.util import RegimenExposureMapper
from src.main.python.util import OntologyConceptMapper

logger = logging.getLogger(__name__)

# TODO: use config.yml file instead?
PATH_MAPPING_TABLES = Path('./resources/mapping_tables')
PATH_CUSTOM_VOCABULARY = Path('./resources/custom_vocabulary/')


class Wrapper(BaseWrapper):  # TODO: call the subclass something else or ok to rename imported module (see imports)?

    def __init__(self, database, source_folder, debug=False):
        super().__init__(database=database, source_schema='', debug=debug)
        self.source_folder = Path(source_folder)
        self.skip_vocabulary_loading = False
        self.variable_concept_mapper = VariableConceptMapper(PATH_MAPPING_TABLES)
        self.regimen_exposure_mapper = RegimenExposureMapper(PATH_MAPPING_TABLES)
        self.ontology_concept_mapper = OntologyConceptMapper(PATH_MAPPING_TABLES)
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
        self.truncate_tables()
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

    # TODO: either group all of the following in a single method, or update base metadata with custom tables (preferred)

    self.custom_table_list = self._get_cdm_tables_to_drop() + [TreatmentLine]

    def create_cdm(self): # TODO: this won't work, base method doesn't take custom list
        '''
        Creates OMOP CDM (non-vocabulary) tables, if they do not exist.
        Extends the original Wrapper method to enable the use of custom tables, by adding them to the list below.
        Remove this method if no custom table is needed.
        '''
        return super(BaseWrapper, self).create_all(self.custom_table_list)

    def drop_cdm(self):
        '''
        Drops OMOP CDM (non-vocabulary) tables, if they exist.
        Extends the original Wrapper method to enable the use of custom tables, by adding them to the list below.
        Remove this method if no custom table is needed.
        '''
        return super(BaseWrapper, self).drop_cdm(self.custom_table_list)

    def truncate_cdm(self): # TODO: method does not exist in Wrapper; see CLLEAR for an example
        '''
        Truncates OMOP CDM (non-vocabulary) tables, if they exist.
        Extends the original Wrapper method to enable the use of custom tables, by adding them to the list below.
        Remove this method if no custom table is needed.
        '''
        return super(BaseWrapper, self).truncate_cdm(self.custom_table_list)

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
        self.load_concept_from_csv(PATH_CUSTOM_VOCABULARY) # TODO: put this in a config file with the previous two (XXX_concept.tsv)
