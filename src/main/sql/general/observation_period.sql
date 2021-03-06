-- Look into all CDM tables to derive observation_period

INSERT INTO @cdm_schema.observation_period
(
   person_id,
   observation_period_start_date,
   observation_period_end_date,
   period_type_concept_id
)
with events as (
    SELECT
        'Visit' AS domain_name, person_id, visit_start_date AS start_date, visit_end_date AS end_date,
        visit_concept_id AS concept_id, visit_type_concept_id as type_concept_id, visit_source_value AS source_value,
        visit_occurrence_id
    FROM @cdm_schema.visit_occurrence

    UNION
    SELECT
        'Condition' AS domain_name, person_id, condition_start_date AS start_date, condition_end_date AS end_date,
        condition_concept_id AS concept_id, condition_type_concept_id as type_concept_id, condition_source_value AS source_value,
        visit_occurrence_id
    FROM @cdm_schema.condition_occurrence

    UNION

    SELECT
        'Drug' AS domain_name, person_id, drug_exposure_start_date AS start_date, drug_exposure_end_date AS end_date,
        drug_concept_id AS concept_id, drug_type_concept_id as type_concept_id, drug_source_value AS source_value,
        visit_occurrence_id
    FROM @cdm_schema.drug_exposure

    UNION

    SELECT
        'Procedure' AS domain_name, person_id, procedure_date AS start_date, NULL AS end_date,
        procedure_concept_id AS concept_id, procedure_type_concept_id as type_concept_id, procedure_source_value AS source_value,
        visit_occurrence_id
    FROM @cdm_schema.procedure_occurrence

    UNION

    SELECT
        'Observation' AS domain_name, person_id, observation_date AS start_date, NULL AS end_date,
        observation_concept_id AS concept_id, observation_type_concept_id as type_concept_id, observation_source_value AS source_value,
        visit_occurrence_id
    FROM @cdm_schema.observation

    UNION

    SELECT
        'Measurement' AS domain_name, person_id, measurement_date AS start_date, NULL AS end_date,
        measurement_concept_id AS concept_id, measurement_type_concept_id as type_concept_id, measurement_source_value AS source_value,
        visit_occurrence_id
    FROM @cdm_schema.measurement

-- uncomment the following if using CDM v5.3.1
--     UNION
--
--     SELECT
--         'Death' AS domain_name, person_id, death_date AS start_date, NULL AS end_date,
--         cause_concept_id AS concept_id, death_type_concept_id as type_concept_id, cause_source_value AS source_value,
--         NULL as visit_occurrence_id
--     FROM @cdm_schema.death
)
select
    person.person_id,
    min(start_date) AS observation_start_date,
    greatest(max(start_date), max(end_date)) AS observation_end_date,
    44814724 as observation_type_concept_id  -- Period covering healthcare encounters
from @cdm_schema.person
left join events on @cdm_schema.person.person_id = events.person_id
where start_date > '1970-01-01'
group by @cdm_schema.person.person_id
;