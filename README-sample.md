# PROJECT TITLE
Project description (e.g. PROJECT ETL to OMOP CDM vX.X).

## Dependencies
Python X.X with the following packages:
- `package1`
- `package2`
- `package3`

The default OMOP CDM vocabulary, additionally including:
- vocabulary1
- vocabulary2
- Custom PROJECT vocabulary (e.g. 2B+ codes)

## How to execute
```bash
main.py -s <path_to_source_data> -h <host> -p <port> -d <target_db> -u <user_name> -w <password>
```
A log of the run will be written to `logs/<timestamp><version>.log`
