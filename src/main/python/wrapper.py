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

# NOTE: select the desired target CDM version below
from omop_etl_wrapper.cdm import cdm531 as cdm
# from omop_etl_wrapper.cdm import cdm600 as cdm


logger = logging.getLogger(__name__)


class Wrapper(BaseWrapper):
    cdm = cdm

    def __init__(self, config):
        super().__init__(config)
        # Load config settings
        self.source_folder = Path(config['run_options']['source_data_folder'])
        self.path_mapping_tables = Path('./resources/mapping_tables')
        self.path_sql_transformations = Path('./src/main/sql')
        # Load data to objects
        # self.variable_concept_mapper = VariableConceptMapper(self.path_mapping_tables)
        # self.ontology_concept_mapper = OntologyConceptMapper(self.path_mapping_tables)
        # self.regimen_exposure_mapper = RegimenExposureMapper(self.path_mapping_tables)
        # NOTE: replace the following with project-specific source table names!
        self.sample_source_table = None

    def transform(self):

        # NOTE: replace the following with project-specific transformations from python/transformations/ or sql/ folder!
        # make sure execution follows order of table dependencies (see cdm model)
        self.execute_transformation(dm_to_person)
        self.execute_transformation(sample_source_table_to_person)
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
        self.load_custom_vocabularies()

        # Load source to concept mappings
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

    # TODO: change the following to load these programmatically from a source data folder?
    # NOTE: replace the following with project-specific source tables and function names!
    def get_sample_source_table(self):
        if not self.sample_source_table:
            self.sample_source_table = SourceData(self.source_folder / 'sample_source_table.csv')
        return self.sample_source_table
