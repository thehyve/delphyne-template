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

from __future__ import annotations

from typing import List, TYPE_CHECKING

from ..util import create_person_id_from_subject_id
from ..util import get_datetime

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def sample_source_table_to_condition_occurrence(wrapper: Wrapper) -> List[Wrapper.cdm.ConditionOccurrence]:

    source = wrapper.source_data.get_source_file('sample_source_table.csv')
    df = source.get_csv_as_df(apply_dtypes=False)

    # sample use of CodeMapper
    ICD10_codes = list(df['condition_ICD10'].values)
    ICD10_mapper = wrapper.code_mapper.generate_code_mapping_dictionary(
        vocabulary_id='ICD10',
        restrict_to_codes=ICD10_codes
    )

    records = []
    for _, row in df.iterrows():

        condition_mapping = ICD10_mapper.lookup(code=row['condition_ICD10'], first_only=True)

        r = wrapper.cdm.ConditionOccurrence()
        r.person_id=create_person_id_from_subject_id(row['subject_id'])
        r.condition_source_value = condition_mapping.source_concept_code
        r.condition_source_concept_id = condition_mapping.source_concept_id
        r.condition_concept_id = condition_mapping.target_concept_id
        r.condition_start_datetime = get_datetime()  # default date
        r.condition_type_concept_id = 0
        r.condition_status_concept_id = 0
        records.append(r)

    return records
