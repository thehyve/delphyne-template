from __future__ import annotations

from sqlalchemy import func, select, join, literal
from sqlalchemy.sql.expression import Insert

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def observation_period_query(wrapper: Wrapper) -> Insert:

    # condition is the only table containing data a.t.m.
    person = wrapper.get_cdm_table('person')
    condition = wrapper.get_cdm_table('condition_occurrence')
    visit = wrapper.get_cdm_table('visit_occurrence')
    drug = wrapper.get_cdm_table('drug_exposure')
    procedure = wrapper.get_cdm_table('procedure_occurrence')
    observation = wrapper.get_cdm_table('observation')
    measurement = wrapper.get_cdm_table('measurement')

    obs_period = wrapper.get_cdm_table('observation_period')

    sel = select([
        condition.c.person_id,
        func.coalesce(condition.c.condition_start_date,
                      condition.c.condition_start_datetime).label('start_date'),
        func.coalesce(condition.c.condition_end_date,
                      condition.c.condition_end_datetime).label('end_date')
    ]).alias('sel_condition')

    sel2 = select([
        person.c.person_id.label('person_id'),
        func.min(sel.c.start_date)
            .label('observation_period_start_date'),
        func.greatest(func.max(sel.c.start_date), func.max(sel.c.end_date))
            .label('observation_period_end_date'),
        # Period covering healthcare encounters)
        literal(44814724).label('period_type_concept_id')
    ]).select_from(
        join(person, sel, person.c.person_id == sel.c.person_id)
    ).group_by(person.c.person_id)

    ins = obs_period.insert().from_select(sel2.columns, sel2)

    return ins
