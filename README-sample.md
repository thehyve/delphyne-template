# PROJECT TITLE
Project description (e.g. PROJECT XYZ ETL to OMOP CDM vX.X).

## Dependencies
Python 3.6+ with the following packages:
- `omop-etl-wrapper == 0.1.0`
- `click >= 7.1.1`
- `...`

The default OMOP CDM vocabulary, additionally including:
- vocabulary XYZ (from Athena or other official source)
- custom XYZ vocabulary (e.g. project-specific 2B+ codes)

## How to execute
```bash
main.py -c <path_to_config.yml>
```
A log of the run will be written to `logs/<timestamp><version>.log`
