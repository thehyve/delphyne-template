# Here you define the specifics of your CDM
# Currently the standard OMOP CDM v6 is specified, but you can customize
# if needed. See the documentation on defining your CDM for more info.
# TODO: add documentation (read the docs?) on how to customize

from sqlalchemy.ext.declarative import declarative_base

from omop_etl_wrapper.cdm.cdm600.clinical_data import (
    BasePersonCdm600,
    BaseNoteCdm600,
    BaseMeasurementCdm600,
    BaseNoteNlpCdm600,
    BaseObservationCdm600,
    BaseSpecimenCdm600,
    BaseStemTableCdm600,
    BaseVisitDetailCdm600,
    BaseConditionOccurrenceCdm600,
    BaseDeviceExposureCdm600,
    BaseDrugExposureCdm600,
    BaseFactRelationshipCdm600,
    BaseObservationPeriodCdm600,
    BaseProcedureOccurrenceCdm600,
    BaseSurveyConductCdm600,
    BaseVisitOccurrenceCdm600,
)

from omop_etl_wrapper.cdm.cdm600.health_system_data import (
    BaseCareSiteCdm600,
    BaseLocationCdm600,
    BaseProviderCdm600,
    BaseLocationHistoryCdm600,
)

from omop_etl_wrapper.cdm.cdm600.health_economics import (
    BaseCostCdm600,
    BasePayerPlanPeriodCdm600,
)

from omop_etl_wrapper.cdm.cdm600.derived_elements import (
    BaseDoseEraCdm600,
    BaseDrugEraCdm600,
    BaseConditionEraCdm600,
)

from omop_etl_wrapper.cdm.cdm531.metadata import (
    BaseCdmSourceCdm531,
    BaseMetadataCdm531,
)

from omop_etl_wrapper.cdm.vocabularies import (
    BaseVocabulary,
    BaseSourceToConceptMap,
    BaseConcept,
    BaseConceptAncestor,
    BaseConceptClass,
    BaseConceptRelationship,
    BaseConceptSynonym,
    BaseDomain,
    BaseDrugStrength,
    BaseRelationship,
)


Base_cdm_600 = declarative_base()


class Person(BasePersonCdm600, Base_cdm_600):
    pass


class Note(BaseNoteCdm600, Base_cdm_600):
    pass


class Measurement(BaseMeasurementCdm600, Base_cdm_600):
    pass


class NoteNlp(BaseNoteNlpCdm600, Base_cdm_600):
    pass


class Observation(BaseObservationCdm600, Base_cdm_600):
    pass


class Specimen(BaseSpecimenCdm600, Base_cdm_600):
    pass


class StemTable(BaseStemTableCdm600, Base_cdm_600):
    pass


class VisitDetail(BaseVisitDetailCdm600, Base_cdm_600):
    pass


class ConditionOccurrence(BaseConditionOccurrenceCdm600, Base_cdm_600):
    pass


class DeviceExposure(BaseDeviceExposureCdm600, Base_cdm_600):
    pass


class DrugExposure(BaseDrugExposureCdm600, Base_cdm_600):
    pass


class FactRelationship(BaseFactRelationshipCdm600, Base_cdm_600):
    pass


class ObservationPeriod(BaseObservationPeriodCdm600, Base_cdm_600):
    pass


class ProcedureOccurrence(BaseProcedureOccurrenceCdm600, Base_cdm_600):
    pass


class SurveyConduct(BaseSurveyConductCdm600, Base_cdm_600):
    pass


class VisitOccurrence(BaseVisitOccurrenceCdm600, Base_cdm_600):
    pass


class Cost(BaseCostCdm600, Base_cdm_600):
    pass


class PayerPlanPeriod(BasePayerPlanPeriodCdm600, Base_cdm_600):
    pass


class CdmSource(BaseCdmSourceCdm531, Base_cdm_600):
    pass


class Metadata(BaseMetadataCdm531, Base_cdm_600):
    pass


class DoseEra(BaseDoseEraCdm600, Base_cdm_600):
    pass


class DrugEra(BaseDrugEraCdm600, Base_cdm_600):
    pass


class ConditionEra(BaseConditionEraCdm600, Base_cdm_600):
    pass


class Location(BaseLocationCdm600, Base_cdm_600):
    pass


class CareSite(BaseCareSiteCdm600, Base_cdm_600):
    pass


class Provider(BaseProviderCdm600, Base_cdm_600):
    pass


class LocationHistory(BaseLocationHistoryCdm600, Base_cdm_600):
    pass


class Concept(BaseConcept, Base_cdm_600):
    pass


class ConceptAncestor(BaseConceptAncestor, Base_cdm_600):
    pass


class ConceptClass(BaseConceptClass, Base_cdm_600):
    pass


class ConceptRelationship(BaseConceptRelationship, Base_cdm_600):
    pass


class ConceptSynonym(BaseConceptSynonym, Base_cdm_600):
    pass


class DrugStrength(BaseDrugStrength, Base_cdm_600):
    pass


class Relationship(BaseRelationship, Base_cdm_600):
    pass


class SourceToConceptMap(BaseSourceToConceptMap, Base_cdm_600):
    pass


class Vocabulary(BaseVocabulary, Base_cdm_600):
    pass


class Domain(BaseDomain, Base_cdm_600):
    pass


from sqlalchemy import (BigInteger, Column, Date, DateTime, ForeignKey,
                        Integer, String)


class Person2(Base_cdm_600):
    __tablename__ = 'person2'
    __table_args__ = {'schema': 'cdm_schema'}

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
