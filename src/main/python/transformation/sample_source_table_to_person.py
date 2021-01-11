from __future__ import annotations

from typing import List, TYPE_CHECKING

# sample functions, remove imports if not used
from src.main.python.util import create_person_id_from_subject_id
from src.main.python.util import get_datetime

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def sample_source_table_to_person(wrapper: Wrapper) -> List[Wrapper.cdm.Person]:

    source = wrapper.source_data.get_source_file('sample_source_table.csv')
    df = source.get_csv_as_df(apply_dtypes=False)

    # The use of DataFrame objects is recommended for:
    # - data filtering
    # - joins between multiple source tables
    # alternatively, you could use the dictionary returned by the wrapper method directly:

    # rows = source.get_csv_as_list_of_dicts()  # Dictionary { row : { variable : value } }
    # for row in rows:
    #     for variable, value in row.items():
    #         r = ...

    records = []
    for _, row in df.iterrows():
        r = wrapper.cdm.Person(
            person_id=create_person_id_from_subject_id(row['subject_id']),
            gender_concept_id=row['sex'],
            year_of_birth=get_datetime(row['date_of_birth']).year,
            race_concept_id=0,
            ethnicity_concept_id=0,
            care_site_id=None,
            person_source_value=row['subject_id'],
            gender_source_value=row['sex'],
            gender_source_concept_id=0,
            race_source_concept_id=0,
            ethnicity_source_concept_id=0
        )
        records.append(r)

    return records
