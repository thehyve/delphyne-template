-- Simple sample transformation

INSERT INTO @cdm_schema.person
(
    person_id,
    gender_concept_id,
    year_of_birth,
    race_concept_id,
    ethnicity_concept_id,
    care_site_id,
    person_source_value,
    gender_source_value,
    gender_source_concept_id,
    race_source_concept_id,
    ethnicity_source_concept_id
) VALUES
(
    999,
    8532,
    1950,
    0,
    0,
    NULL,
    'ID999',
    'F',
    0,
    0,
    0
)
;