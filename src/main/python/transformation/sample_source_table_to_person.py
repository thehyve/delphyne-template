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

from typing import List
import pandas as pd

from ohdsi_etl_wrapper.cdm import Person # TODO: check dependency location
from ..util import create_person_id_from_subject_id # sample general function
from ..util import get_datetime # sample date function


def sample_source_table_to_person(wrapper) -> List[Person]:

    source = pd.DataFrame(wrapper.get_sample_source_table())

    # alternatively, you could use the dictionary retrieved by the wrapper method directly;
    # however, the use of DataFrame objects is recommended for:
    # - data filtering
    # - joins between multiple source tables

    # source = wrapper.get_sample_source_table() -> Dictionary { row : { variable : value} }
    #
    # for row in source:
    #     for variable, value in row.items():
    #         r = ...

    records = []
    for _, row in source.iterrows():
        r = Person(
            person_id=create_person_id_from_subject_id(row['subject_id']),
            gender_concept_id=row['sex'],
            year_of_birth=get_datetime(['date_of_birth']).year,
            race_concept_id=0,
            ethnicity_concept_id=0,
            care_site_id=row['care_site'],
            person_source_value=row['subject_id'],
            gender_source_value=row['sex'],
            gender_source_concept_id=0,
            race_source_concept_id=0,
            ethnicity_source_concept_id=0
        )

        records.append(r)

    return records