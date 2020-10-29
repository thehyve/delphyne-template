from omop_etl_wrapper.cdm.cdm600.clinical_data import BasePersonCdm600
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


class BaseTreatmentLine:
    __tablename__ = 'treatment_line'
    __table_args__ = {'schema': 'cdm_schema'}

    treatment_line_id = Column(Integer, primary_key=True)

    @declared_attr
    def person_id(cls):
        return Column(ForeignKey('cdm_schema.person.person_id'), nullable=False, index=True)

    line_number = Column(Integer, nullable=True)
    total_cycle_number = Column(Integer, nullable=True)
    line_start_date = Column(Date, nullable=True)
    line_end_date = Column(Date, nullable=True)

    @declared_attr
    def drug_concept_id(cls):
        return Column(ForeignKey('vocabulary_schema.concept.concept_id'), index=True)

    drug_era_start_date = Column(Date, nullable=True)
    drug_era_end_date = Column(Date, nullable=True)
    drug_exposure_count = Column(Integer, nullable=True)
    drug_source_value = Column(String(50))
    treatment_type_id = Column(Integer, nullable=True)

    @declared_attr
    def person(cls):
        return relationship('Person')

    @declared_attr
    def drug_concept(cls):
        return relationship('Concept', primaryjoin='TreatmentLine.drug_concept_id == Concept.concept_id')


class CustomPerson(BasePersonCdm600):
    custom_field = Column(Integer)
