# delphyne-template

delphyne-template is an ETL framework for the conversion of source data to the
[OMOP Common Data Model (CDM)](https://www.ohdsi.org/data-standardization/the-common-data-model/).

It complements the functionality of the [delphyne](https://github.com/thehyve/delphyne) Python package
by providing a project structure that satisfies delphyne's assumptions regarding folders and scripts locations,
greatly simplifying the setup process. It also ensures the optimal use of the package
by providing a basic wrapper implementation, a customizable target CDM model, and sample configuration files
for database connection and source data loading, among other features.

To get started with a new ETL project, please click on the `Use this template` button at the top of the page.
A full description and usage instructions are provided on [Read the Docs](https://delphyne.readthedocs.io/en/latest/delphyne_template).

NOTE: This template has been fully tested only with PostgreSQL.

---

:arrow_down: *After creating a new project, make sure to edit the following with information relevant to your ETL!*

# PROJECT TITLE

Project description (e.g. PROJECT XXX ETL to OMOP CDM vX.X.X).

## Dependencies

### Code

- Python 3.7.2+ with packages in `requirements.txt`
- R with packages `yaml` and `DatabaseConnector` *(NOTE: only needed if using R test framework)*

### Vocabularies

The following vocabularies are required in addition to the default download bundle from [Athena](https://athena.ohdsi.org/):
- non-default Athena vocabularies: XXX (code XXX), ...
- custom vocabularies (project-specific 2B+ codes): XXX, ...

## ETL execution

```bash
main.py -c <path_to_config.yml>
```

A log of the run will be written to `logs/<timestamp><version>.log`

## Credits

This OMOP ETL project was created with [delphyne](https://github.com/thehyve/delphyne)
and the [delphyne-template](https://github.com/thehyve/delphyne-template) project template.
