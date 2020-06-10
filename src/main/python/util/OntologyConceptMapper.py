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
import csv
from pathlib import Path
from typing import Dict
import logging

logger = logging.getLogger(__name__)


# TODO: refactor to use Target from VariableConceptMapper
class OntologyTarget:

    def __init__(self):
        self.source_value = None         # variable name
        self.value_source_value = None   # ontology code
        self.source_concept_id = None    # concept_id for ontology code
        self.value_as_concept_id = None  # standard concept_id for concept expressed by ontology code

    def __str__(self):
        return f'{self.source_value}-{self.value_source_value} => ' \
               f'source_value: {self.source_value}, ' \
               f'source_concept_id: {self.source_concept_id}, ' \
               f'value_source_value: {self.value_source_value}, ' \
               f'value_as_concept_id: {self.value_as_concept_id}'



# TODO: refactor to subclass VariableConceptMapper
class OntologyConceptMapper:

    mapping_table_dict = {
        'spec_malignita_sledovani': 'MKN10_only_C.tsv',
        'spec_komorbidita_sledov': 'MKN10_without_C.tsv',
        'spec_lymfoproliferace_sledovan': 'MKN10_only_C.tsv'
    }

    def __init__(self, directory: Path):
        self.value_to_ontology_code: Dict[str, Dict[str, str]] = {}  # mapping table : value : ontology code
        self.ontology_code_to_source_concept: Dict[str] = {}
        self.ontology_code_to_standard_concept: Dict[str] = {}

        if directory:
            self.load(directory)

    def __call__(self, variable: str, value: str) -> OntologyTarget:
        return self.lookup(variable, value)

    def load(self, directory: Path):
        if not directory.exists():
            raise FileNotFoundError(f"No such directory: '{directory}'")

        for mapping_table in set(self.mapping_table_dict.values()):
            table_path = directory / mapping_table
            if table_path.exists():
                logger.info(f"Loading {table_path.name}...")
                self._load_ontology_map(table_path)

    def _load_ontology_map(self, file_path: Path):

        mapping_table = file_path.name
        self.value_to_ontology_code[mapping_table] = {}

        for row in self._load_map(file_path):
            value = str(row['source_code'])  # TODO: change to sourceCode
            ontology_code = row['MKN10_code']  # TODO: change to ontologyCode
            self.value_to_ontology_code[mapping_table][value] = ontology_code
            self.ontology_code_to_source_concept[ontology_code] = row['source_concept_id']
            self.ontology_code_to_standard_concept[ontology_code] = row['target_concept_id']

    @staticmethod
    def _load_map(file_path: Path):
        with file_path.open(encoding='ISO-8859-2') as f_in:
            for row in csv.DictReader(f_in, delimiter='\t'):
                yield row

    def has_mapping_for_variable(self, variable: str):
        return variable in self.mapping_table_dict.keys()

    def has_mapping_for_value(self, value: str, variable: str):
        mapping_table = self.mapping_table_dict[variable]
        return value in self.value_to_ontology_code[mapping_table].keys()

    def lookup(self, variable: str, value: str) -> OntologyTarget:
        """
        For given variable/value pair, looks up the target ontology code (value source value)
        and the corresponding (source) concept_id and standard concept_id (value as concept_id).
        :param variable: string
        :param value: string
        :return: OntologyTarget
        """
        variable = variable.lower()
        value = str(value).lower()

        target = OntologyTarget()

        if not self.has_mapping_for_variable(variable):
            logger.warning(f"Variable {variable} does not match any ontology mapping table")
            return target
        elif not self.has_mapping_for_value(value, variable):
            logger.warning(f"Value {value} for variable {variable} does not map to any ontology code")
            target.source_value = variable
            target.value_source_value = value
            target.source_concept_id = None
            target.value_as_concept_id = None
            return target

        map_table = self.mapping_table_dict[variable]
        ontology_code = self.value_to_ontology_code[map_table][value]

        target.source_value = variable
        target.value_source_value = ontology_code
        target.source_concept_id = self.ontology_code_to_source_concept.get(ontology_code, None)
        target.value_as_concept_id = self.ontology_code_to_standard_concept.get(ontology_code, None)

        return target


if __name__ == '__main__':
    mapper = OntologyConceptMapper(Path('./resources/mapping_tables'))

    import numpy as np
    # TESTS
    # existing values
    print(mapper.lookup('spec_malignita_sledovani', '955'))
    print(mapper.lookup('spec_komorbidita_sledov', '50'))
    print(mapper.lookup('spec_lymfoproliferace_sledovan', '955'))
    print(mapper.lookup('spec_malignita_sledovani', 955))
    print(mapper.lookup('spec_komorbidita_sledov', 50))
    print(mapper.lookup('spec_lymfoproliferace_sledovan', 955))
    # non-existent values
    print(mapper.lookup('spec_malignita_sledovani', '50'))
    print(mapper.lookup('spec_komorbidita_sledov', '955'))
    print(mapper.lookup('spec_lymfoproliferace_sledovan', '50'))
    # non-existent variables
    print(mapper.lookup('random_var', '123'))
    # special cases
    print(mapper.lookup('', ''))
    print(mapper.lookup('spec_malignita_sledovani', None))
    print(mapper.lookup('spec_malignita_sledovani', np.nan))