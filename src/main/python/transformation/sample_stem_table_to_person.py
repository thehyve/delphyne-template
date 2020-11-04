from __future__ import annotations

from typing import List, TYPE_CHECKING

from src.main.python.custom_tables.custom_tables import Person2


if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def dm_to_person(wrapper: Wrapper) -> List[Wrapper.cdm.Person]:
    records = []
    p = wrapper.cdm.Person(gender_concept_id=2,
               year_of_birth=1940,
               race_concept_id=0,
               ethnicity_concept_id=0,
               gender_source_concept_id=0,
               race_source_concept_id=0,
               ethnicity_source_concept_id=0,
               )
    records.append(p)
    p2 = Person2(gender_concept_id=8532,
                 year_of_birth=1940,
                 race_concept_id=0,
                 ethnicity_concept_id=0,
                 gender_source_concept_id=0,
                 race_source_concept_id=0,
                 ethnicity_source_concept_id=0,
                 )
    records.append(p2)

    return records
