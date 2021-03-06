from __future__ import annotations

from sqlalchemy import func, select, join, union, literal
from sqlalchemy.sql.expression import Insert

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.main.python.wrapper import Wrapper


def observation_period_query(wrapper: Wrapper) -> Insert:

    person = wrapper.cdm.Person.__table__
    condition = wrapper.cdm.ConditionOccurrence.__table__
    visit = wrapper.cdm.VisitOccurrence.__table__
    drug = wrapper.cdm.DrugExposure.__table__
    procedure = wrapper.cdm.ProcedureOccurrence.__table__
    observation = wrapper.cdm.Observation.__table__
    measurement = wrapper.cdm.Measurement.__table__
    obs_period = wrapper.cdm.ObservationPeriod.__table__

    sel_condition = select([
        condition.c.person_id,
        func.coalesce(condition.c.condition_start_date,
                      condition.c.condition_start_datetime).label('start_date'),
        func.coalesce(condition.c.condition_end_date,
                      condition.c.condition_end_datetime).label('end_date')
    ])

    sel_drug = select([
        drug.c.person_id,
        func.coalesce(drug.c.drug_exposure_start_date,
                      drug.c.drug_exposure_start_datetime).label('start_date'),
        func.coalesce(drug.c.drug_exposure_end_date,
                      drug.c.drug_exposure_end_datetime).label('end_date')
    ])

    sel_measurement = select([
        measurement.c.person_id,
        func.coalesce(measurement.c.measurement_date,
                      measurement.c.measurement_datetime).label('start_date'),
        literal(None).label('end_date')
    ])

    sel_observation = select([
        observation.c.person_id,
        func.coalesce(observation.c.observation_date,
                      observation.c.observation_datetime).label('start_date'),
        literal(None).label('end_date')
    ])

    sel_procedure = select([
        procedure.c.person_id,
        func.coalesce(procedure.c.procedure_date,
                      procedure.c.procedure_datetime).label('start_date'),
        literal(None).label('end_date')
    ])

    sel_visit = select([
        visit.c.person_id,
        func.coalesce(visit.c.visit_start_date,
                      visit.c.visit_start_datetime).label('start_date'),
        func.coalesce(visit.c.visit_end_date,
                      visit.c.visit_end_datetime).label('end_date')
    ])

    # CDM 5.3.1
    try:
        death = wrapper.cdm.Death.__table__

        sel_death = select([
            death.c.person_id,
            func.coalesce(death.c.death_date,
                          death.c.death_datetime).label('start_date'),
            literal(None).label('end_date')
        ])

    except AttributeError:
        sel_death = None

    sels = [
        sel_condition,
        sel_drug,
        sel_measurement,
        sel_observation,
        sel_procedure,
        sel_visit,
        sel_death
    ]

    include_sels = [sel for sel in sels if sel is not None]
    all_periods = union(*include_sels).alias('all_periods')

    sel = select([
        person.c.person_id.label('person_id'),
        func.min(all_periods.c.start_date)
            .label('observation_period_start_date'),
        func.greatest(func.max(all_periods.c.start_date), func.max(all_periods.c.end_date))
            .label('observation_period_end_date'),
        # Period covering healthcare encounters)
        literal(44814724).label('period_type_concept_id')
    ]).select_from(
        join(person, all_periods, person.c.person_id == all_periods.c.person_id)
    )\
        .where(all_periods.c.start_date > '1970-01-01')\
        .group_by(person.c.person_id)

    ins = obs_period.insert().from_select(sel.columns, sel)

    return ins
