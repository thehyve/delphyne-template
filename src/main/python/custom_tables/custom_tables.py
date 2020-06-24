# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from omop_etl_wrapper import Base


# TODO: how to overrire {'schema' : 'cdm'} with schema provided by

class Person2(Base):
    __tablename__ = 'person2'
    __table_args__ = {'schema': 'cdm600'}

    person_id = Column(BigInteger, primary_key=True, unique=True)
    gender_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    month_of_birth = Column(Integer)
    day_of_birth = Column(Integer)
    birth_datetime = Column(DateTime)
    death_datetime = Column(DateTime)
    race_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), nullable=False)
    ethnicity_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), nullable=False)
    location_id = Column(ForeignKey('cdm_schema.location.location_id'))
    provider_id = Column(ForeignKey('cdm_schema.provider.provider_id'))
    care_site_id = Column(ForeignKey('cdm_schema.care_site.care_site_id'))
    person_source_value = Column(String(50))
    gender_source_value = Column(String(50))
    gender_source_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), nullable=False)
    race_source_value = Column(String(50))
    race_source_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), nullable=False)
    ethnicity_source_value = Column(String(50))
    ethnicity_source_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), nullable=False)


class TreatmentLine(Base):
    __tablename__ = 'treatment_line'
    __table_args__ = {'schema': 'cdm600'}

    treatment_line_id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('cdm_schema.person.person_id'), nullable=False, index=True)
    line_number = Column(Integer, nullable=True)
    total_cycle_number = Column(Integer, nullable=True)
    line_start_date = Column(Date, nullable=True)
    line_end_date = Column(Date, nullable=True)
    drug_concept_id = Column(ForeignKey('vocabulary_schema.concept.concept_id'), index=True)
    drug_era_start_date = Column(Date, nullable=True)
    drug_era_end_date = Column(Date, nullable=True)
    drug_exposure_count = Column(Integer, nullable=True)
    drug_source_value = Column(String(50))
    treatment_type_id = Column(Integer, nullable=True)

    person = relationship('Person')
    drug_concept = relationship('Concept', primaryjoin='TreatmentLine.drug_concept_id == Concept.concept_id')
