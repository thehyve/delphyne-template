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

import logging

from delphyne import Wrapper as BaseWrapper
from delphyne.config.models import MainConfig

from src.main.python.transformation import *
from src.main.python import cdm


logger = logging.getLogger(__name__)


class Wrapper(BaseWrapper):
    cdm = cdm

    def __init__(self, config: MainConfig):
        super().__init__(config, cdm)

    def transform(self):
        # NOTE: replace the following with project-specific transformations from python/transformations/ or sql/ folder!
        # make sure execution follows order of table dependencies (see cdm model)
        self.execute_transformation(dm_to_person)
        self.execute_transformation(sample_source_table_to_person)
        self.execute_transformation(sample_source_table_to_condition_occurrence)
        # self.execute_sql_file('sample_script.sql')

    def run(self):
        # Prepare source
        self.create_schemas()
        self.drop_cdm()
        self.create_cdm()

        # Load custom vocabularies
        self.vocab_manager.load_custom_vocabularies()

        # Load source to concept mappings
        self.vocab_manager.load_stcm()

        # Load source data
        self.transform()

        # Log/write overview of transformations and sources
        self.summarize()
