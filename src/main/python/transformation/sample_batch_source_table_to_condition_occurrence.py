from __future__ import annotations

from typing import Generator, TYPE_CHECKING

# sample functions, remove imports if not used
from src.main.python.util import create_person_id_from_subject_id
from src.main.python.util import get_datetime

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def sample_batch_source_table_to_condition_occurrence(wrapper: Wrapper) -> Generator[Wrapper.cdm.ConditionOccurrence]:
    # Memory efficient inserting.
    # 1. iterate through source data with a generator
    # 2. return transformed records as a generator
    # 3. this function has to be called with wrapper.execute_batch_transformation,
    #    which handles inserting records in small batches of records
    source = wrapper.source_data.get_source_file('sample_source_table.csv')
    data = source.get_csv_as_generator_of_dicts()

    for row in data:
        yield wrapper.cdm.ConditionOccurrence(
            person_id=create_person_id_from_subject_id(row['subject_id']),
            condition_start_datetime=get_datetime(),
            condition_concept_id=0,
            condition_source_concept_id=0,
            condition_status_concept_id=0,
            condition_type_concept_id=0
        )
