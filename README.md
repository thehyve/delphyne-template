# ohdsi-etl-master-framework
An ETL template for future OHDSI projects

## Discussion items

Examples of things to clarify, feel free to add more!

#### General goal:
- Should we aim to create an ORM-based reference ETL since more generally applicable than one based on PostgreSQL queries only? (e.g. Prias vs Caliber)

#### Repo structure:
- Quite consistent across projects already, anything that still need clarification? (e.g. where do I put logging scripts, or data pre-processing scripts/notebooks that are not executed during the ETL..)

#### Test framework:
- Conventions for using RiaH auto-generated test framework (e.g. separate test files for each source / target table combination, assign test IDs within specific numeric ranges..)
- Bets strategy for running the tests (e.g. run one after the other script to create tests, ETL, script to evaluate tests vs automatically executing using IDE settings)
- ..or shall we completely change strategy and go for completely isolated unit tests that can be run independently (e.g. switch fully to Python)?
- How to integrate with Data Quality Dashboard?
