from __future__ import annotations

from typing import List, TYPE_CHECKING

from omop_etl_wrapper.cdm.hybrid import Person
# from omop_etl_wrapper.cdm.cdm531 import Person
# from omop_etl_wrapper.cdm.cdm600 import Person

from src.main.python.custom_tables.my_tables import Person2

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def dm_to_person(wrapper: Wrapper) -> List[Person]:
    records = []
    p = Person(gender_concept_id=2,
               year_of_birth=1940,
               race_concept_id=0,
               ethnicity_concept_id=0,
               gender_source_concept_id=0,
               race_source_concept_id=0,
               ethnicity_source_concept_id=0,
               )
    records.append(p)
    p2 = Person2(gender_concept_id=2,
                 year_of_birth=1940,
                 race_concept_id=0,
                 ethnicity_concept_id=0,
                 gender_source_concept_id=0,
                 race_source_concept_id=0,
                 ethnicity_source_concept_id=0,
                 )
    records.append(p2)

    return records