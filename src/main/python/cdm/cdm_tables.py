from pathlib import Path
from omop_etl_wrapper.util.io import read_yaml_file

from src.main.python.cdm.base import Base

from omop_etl_wrapper.cdm.vocabularies import *
import src.main.python.cdm.custom_tables.custom_cdm as custom_cdm
# TODO: refactor __init__.py in wrapper to enable bulk import statements
from omop_etl_wrapper.cdm.cdm600.clinical_data import *
from omop_etl_wrapper.cdm.cdm600.health_system_data import *
from omop_etl_wrapper.cdm.cdm531.clinical_data import *
from omop_etl_wrapper.cdm.cdm531.health_system_data import *



config = read_yaml_file(Path('config/tables-sample.yml'))
tables_config = config['standard_tables']


# CLINICAL TABLES

if tables_config['person'] == 'cdm600':
    class Person(BasePersonCdm600, Base):
        pass
elif tables_config['person'] == 'cdm531':
    class Person(BasePersonCdm531, Base):
        pass
elif tables_config['person'] == 'custom':
    class Person(custom_cdm.BasePersonCustom, Base):
        pass

if tables_config['death'] == 'cdm531':
    class Death(BaseDeathCdm531, Base):
        pass
elif tables_config['death'] == 'custom':
    class Death(custom_cdm.BaseDeathCustom, Base):
        pass

# HEALTH SYSTEM TABLES

if tables_config['location'] == 'cdm600':
    class Location(BaseLocationCdm600, Base):
        pass
elif tables_config['location'] == 'cdm531':
    class Location(BaseLocationCdm531, Base):
        pass
elif tables_config['location'] == 'custom':
    class Location(custom_cdm.BaseLocationCuston, Base):
        pass

if tables_config['provider'] == 'cdm600':
    class Provider(BaseProviderCdm600, Base):
        pass
elif tables_config['provider'] == 'cdm531':
    class Provider(BaseProviderCdm531, Base):
        pass
elif tables_config['provider'] == 'custom':
    class Provider(custom_cdm.BaseProviderCustom, Base):
        pass

if tables_config['care_site'] == 'cdm600':
    class CareSite(BaseCareSiteCdm600, Base):
        pass
elif tables_config['care_site'] == 'cdm531':
    class CareSite(BaseCareSiteCdm531, Base):
        pass
elif tables_config['care_site'] == 'custom':
    class CareSite(custom_cdm.BaseCareSiteCustom, Base):
        pass

# VOCABULARY TABLES

class Vocabulary(BaseVocabulary, Base):
    pass

class SourceToConceptMap(BaseSourceToConceptMap, Base):
    pass

class Concept(BaseConcept, Base):
    pass

class ConceptAncestor(BaseConceptAncestor, Base):
    pass

class ConceptClass(BaseConceptClass, Base):
    pass

class ConceptRelationship(BaseConceptRelationship, Base):
    pass

class ConceptSynonym(BaseConceptSynonym, Base):
    pass

class Domain(BaseDomain, Base):
    pass

class DrugStrength(BaseDrugStrength, Base):
    pass

class Relationship(BaseRelationship, Base):
    pass
