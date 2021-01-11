library(DatabaseConnector)
library(yaml)
config <- yaml.load_file('config.yml')
options(width=150)  # Preventing wrapping when printing dataframe

source('TestFramework.R')

# Run and output test queries ---------------------------------------------
connectionConfig <- config$connectionDetails
connectionDetails <- createConnectionDetails(dbms = connectionConfig$dbms,
                                             user = connectionConfig$user,
                                             password = connectionConfig$password,
                                             server = connectionConfig$server,
                                             port = connectionConfig$port)
connection <- connect(connectionDetails)

testSql <- readLines(config$testQueryFileName)
testSql[1] <- sprintf('DROP TABLE IF EXISTS %s.test_results;', config$cdmSchema) # Replace existing SQL server specific table drop
executeSql(connection, paste(testSql, collapse='\n'))

# Display test results ----------------------------------------------------
outputTestResultsSummary(connection, config$cdmSchema)

# Write full test results to file ---------------------------------------
df_results <- DatabaseConnector::querySql(connection, gsub('@cdm_database_schema', config$cdmSchema, 'SELECT * FROM @cdm_database_schema.test_results;'))
write.csv(df_results, "unittest_results.csv", row.names = FALSE, quote = c(1))
disconnect(connection)
