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
        condition.columns.person_id,
        func.coalesce(condition.columns.condition_start_date,
                      condition.columns.condition_start_datetime).label('start_date'),
        func.coalesce(condition.columns.condition_end_date,
                      condition.columns.condition_end_datetime).label('end_date')
    ])

    j = join(person, sel, person.columns.person_id == sel.columns.person_id)

    sel2 = select([
        j.columns.person_id.label('person_id'),
        func.min(j.columns.start_date)
            .label('observation_period_start_date'),
        func.max(func.max(j.columns.start_date), func.max(j.columns.end_date))
            .label('observation_period_end_date'),
        # Period covering healthcare encounters)
        literal(44814724).label('period_type_concept_id')
    ]).select_from(j)

    ins = obs_period.insert().from_select(sel2.columns, sel2)

    # stage_w_columns = select(list(stage.columns) + [literal(1).label('IsCurrent'),
    #                                                 literal(datetime(2018, 1, 23)).label(
    #                                                     'FirstObserved'),
    #                                                 literal(datetime(2018, 1, 23)).label(
    #                                                     'LastObserved')])
    # stmt = base.insert().from_select(stage_w_columns.columns, stage_w_columns)

    # ins = obs_period.insert().from_select(sel2.columns, sel2)

    return ins
