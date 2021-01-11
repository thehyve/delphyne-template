# PROJECT TITLE
Project description (e.g. PROJECT XXX ETL to OMOP CDM vX.X).

## Dependencies

### Code
- Python 3.X with packages in `requirements.txt`
- R with packages `yaml` and `DatabaseConnector` *(NOTE: only needed if using R test framework)*

### Vocabularies
- default OMOP vocabularies from [Athena](https://athena.ohdsi.org/)
- additional Athena vocabularies: XXX (code XXX), ...
- custom vocabularies (e.g. project-specific 2B+ codes): XXX, ...

## How to execute
```bash
main.py -c <path_to_config.yml>
```
A log of the run will be written to `logs/<timestamp><version>.log`
