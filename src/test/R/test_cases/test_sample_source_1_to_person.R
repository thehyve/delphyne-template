source('TestFramework.R')

declareTest(1, 'Add 1 person to Person table') # test ID range 1-99
add_sample_source_table(subject_id = '0000001')
expect_count_person(person_id = 1, rowCount = 1)
