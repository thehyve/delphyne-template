from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.sql.expression import Insert

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def death_and_person_to_person(wrapper: Wrapper) -> Insert:

    person = wrapper.get_source_table('person')
    death = wrapper.get_source_table('death')

    target = wrapper.get_target_table('person')

    sel = person.join(
        death,
        person.columns['person_id'] == death.columns['person_id'],
        isouter=True)

    sel = select([
        person.columns['person_id'],
        person.columns['year_of_birth'],
        person.columns['month_of_birth'],
        person.columns['day_of_birth'],
        person.columns['birth_datetime'],
        person.columns['gender_concept_id'],
        person.columns['race_concept_id'],
        person.columns['ethnicity_concept_id'],
        person.columns['person_source_value'],
        person.columns['gender_source_value'],
        person.columns['race_source_value'],
        person.columns['ethnicity_source_value'],
        person.columns['provider_id'],
        person.columns['care_site_id'],
        func.coalesce(person.columns['gender_source_concept_id'], 0)
            .label('gender_source_concept_id'),
        func.coalesce(person.columns['race_source_concept_id'], 0)
            .label('race_source_concept_id'),
        func.coalesce(person.columns['ethnicity_source_concept_id'], 0)
            .label('ethnicity_source_concept_id'),
        func.coalesce(death.columns['death_datetime'], death.columns['death_date'])
            .label('death_datetime')]) \
        .select_from(sel)

    ins = target.insert().from_select(sel.columns, sel)

    return ins
