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
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class DrugTarget:

    def __init__(self):
        self.drug_concept_id = None
        self.ingredient_name = None
        self.start_day = None
        self.end_day = None
        self.sig = None
        self.dose_number = None
        self.dose_unit = None
        self.route_concept_id = None
        self.route_source_value = None

    def __str__(self):
        return f'DrugTarget => ' \
               f'concept_id: {self.drug_concept_id}, ' \
               f'ingredient_name: {self.ingredient_name}, ' \
               f'start_day: {self.start_day}, ' \
               f'end_day: {self.end_day}, ' \
               f'sig: {self.sig}, ' \
               f'dose_number: {self.dose_number}, ' \
               f'dose_unit: {self.dose_unit}, ' \
               f'route_concept_id: {self.route_concept_id}, ' \
               f'route_source_value: {self.route_source_value}'


class RegimenExposureMapper:

    def __init__(self, path):
        self.input_path = path
        self.regimen_to_exposures: Dict[str, List[DrugTarget]] = {}
        self.load_drug_regimens()

    def load_drug_regimens(self):
        # Regimen code,Regimen name,Ingredient,concept_id,treatment line,start day,end day,sig,dose,unit,Route,original sig,comments,
        with self.input_path.open() as f_in:
            drug_exposures = csv.DictReader(f_in)
            for row in drug_exposures:
                key = self.create_key(row['Regimen code'], row['treatment line'])
                drug_exposure = DrugTarget()
                drug_exposure.drug_concept_id = row['concept_id']
                drug_exposure.ingredient_name = row['Ingredient']
                drug_exposure.start_day = row['start day']
                drug_exposure.end_day = row['end day']
                drug_exposure.sig = row['sig']
                drug_exposure.dose_number = self.parse_dose(row['dose'])
                drug_exposure.dose_unit = row['unit']
                drug_exposure.route_source_value = row['Route']
                drug_exposure.route_concept_id = row['route_concept_id']

                exposures_list = self.regimen_to_exposures.setdefault(key, [])
                exposures_list.append(drug_exposure)

    @staticmethod
    def parse_dose(dose_string):
        if '-' in dose_string:
            dose_string = dose_string.split('-')[0]
        dose_cleaned = dose_string.replace(',', '.')
        if not dose_cleaned:
            return None
        return float(dose_cleaned)

    @staticmethod
    def create_key(regimen_code, treatment_line):
        is_first_line = str(treatment_line) == '1'
        return '%s-%s' % (regimen_code, is_first_line)

    def lookup(self, regimen_code, treatment_line) -> List[DrugTarget]:
        key = self.create_key(regimen_code, treatment_line)
        if key in self.regimen_to_exposures:
            return self.regimen_to_exposures.get(key)

        # Try to find treatment line 1 exists
        key = self.create_key(regimen_code, 1)
        if key in self.regimen_to_exposures:
            return self.regimen_to_exposures.get(key)

        logger.warning(f'Regimen {regimen_code} not found')
        return []


if __name__ == '__main__':
    mapper = RegimenExposureMapper(Path('./resources/mapping_tables/drug_regimen_components.csv'))

    for x in mapper.lookup('180', 1):
        print(x)

    for x in mapper.lookup('187', 2):
        print(x)

    mapper.lookup('999', 1)