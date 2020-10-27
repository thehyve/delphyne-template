import omop_etl_wrapper.cdm.cdm600 as cdm600
import omop_etl_wrapper.cdm.cdm531 as cdm531
import src.main.python.custom_tables.custom_cdm as custom_cdm

from src.main.python.cdm.base import Base


class LoadCdmTables():

    def __init__(self, table_config):
        self.load_person(table_config['person'])
        self.load_location(table_config['location'])
        self.load_provider(table_config['provider'])
        self.load_care_site(table_config['care_site'])


    def load_person(self, cdm):
        if cdm == 'cdm600':
            class Person(cdm600.clinical_data.BasePersonCdm600, Base):
                pass
        elif cdm == 'cdm531':
            class Person(cdm531.clinical_data.BasePersonCdm531, Base):
                pass
        elif cdm == 'custom':
            class Person(custom_cdm.BasePersonCustom, Base):
                pass

    def load_location(self, cdm):
        if cdm == 'cdm600':
            class Location(cdm600.health_system_data.BaseLocationCdm600, Base):
                pass
        elif cdm == 'cdm531':
            class Location(cdm531.health_system_data.BaseLocationCdm531, Base):
                pass
        elif cdm == 'custom':
            class Location(custom_cdm.BaseLocationCustom, Base):
                pass

    def load_provider(self, cdm):
        if cdm == 'cdm600':
            class Provider(cdm600.health_system_data.BaseProviderCdm600, Base):
                pass
        elif cdm == 'cdm531':
            class Provider(cdm531.health_system_data.BaseProviderCdm531, Base):
                pass
        elif cdm == 'custom':
            class Provider(custom_cdm.BaseProviderCustom, Base):
                pass

    def load_care_site(self, cdm):
        if cdm == 'cdm600':
            class CareSite(cdm600.health_system_data.BaseCareSiteCdm600, Base):
                pass
        elif cdm == 'cdm531':
            class CareSite(cdm531.health_system_data.BaseCareSiteCdm531, Base):
                pass
        elif cdm == 'custom':
            class CareSite(custom_cdm.BaseCareSiteCustom, Base):
                pass

