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
    ICD10CM_codes = list(df['condition_ICD10CM'].values)
    ICD10CM_mapper = wrapper.code_mapper.generate_code_mapping_dictionary(
        vocabulary_id='ICD10CM',
        restrict_to_codes=ICD10CM_codes
    )

    records = []
    for _, row in df.iterrows():

        condition_mapping = ICD10CM_mapper.lookup(source_code=row['condition_ICD10CM'], first_only=True)

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
