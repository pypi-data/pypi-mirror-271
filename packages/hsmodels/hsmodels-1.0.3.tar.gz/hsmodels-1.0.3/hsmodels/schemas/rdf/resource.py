import uuid
from typing import List, Literal

from pydantic import AnyUrl, BaseModel, Field, field_serializer, field_validator, model_validator
from rdflib import URIRef

from hsmodels.namespaces import CITOTERMS, DC, DCTERMS, HSRESOURCE, HSTERMS, ORE, RDF
from hsmodels.schemas.rdf.fields import (
    AwardInfoInRDF,
    ContributorInRDF,
    CoverageInRDF,
    CreatorInRDF,
    DateInRDF,
    DescriptionInRDF,
    ExtendedMetadataInRDF,
    IdentifierInRDF,
    PublisherInRDF,
    RelationInRDF,
    RightsInRDF,
    get_RDF_IdentifierType,
)
from hsmodels.schemas.rdf.root_validators import (
    parse_coverages,
    parse_rdf_dates,
    parse_rdf_extended_metadata,
    rdf_parse_description,
    rdf_parse_rdf_subject,
)
from hsmodels.schemas.rdf.validators import (
    coverages_constraint,
    coverages_spatial_constraint,
    dates_constraint,
    language_constraint,
    rdf_parse_identifier,
    sort_creators,
)


def hs_uid():
    return getattr(HSRESOURCE, uuid.uuid4().hex)


class FileMap(BaseModel):
    rdf_subject: get_RDF_IdentifierType(Field(default_factory=hs_uid))
    rdf_type: AnyUrl = Field(json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=ORE.Aggregation)

    is_documented_by: AnyUrl = Field(json_schema_extra={"rdf_predicate": CITOTERMS.isDocumentedBy})
    files: List[AnyUrl] = Field(json_schema_extra={"rdf_predicate": ORE.aggregates}, default=[])
    title: str = Field(json_schema_extra={"rdf_predicate": DC.title})
    is_described_by: AnyUrl = Field(json_schema_extra={"rdf_predicate": ORE.isDescribedBy})


class ResourceMap(BaseModel):
    rdf_subject: get_RDF_IdentifierType(Field(default_factory=hs_uid))
    rdf_type: AnyUrl = Field(json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=ORE.ResourceMap)

    describes: FileMap = Field(json_schema_extra={"rdf_predicate": ORE.describes})
    identifier: str = Field(json_schema_extra={"rdf_predicate": DC.identifier}, default=None)
    # modified: datetime = Field(rdf_predicate=DCTERMS.modified)
    creator: str = Field(json_schema_extra={"rdf_predicate": DC.creator}, default=None)


class BaseResource(BaseModel):
    rdf_subject: get_RDF_IdentifierType(Field(default_factory=hs_uid, alias='rdf_subject'))

    title: str = Field(json_schema_extra={"rdf_predicate": DC.title})
    description: DescriptionInRDF = Field(
        json_schema_extra={"rdf_predicate": DC.description}, default_factory=DescriptionInRDF
    )
    language: str = Field(json_schema_extra={"rdf_predicate": DC.language}, default='eng')
    subjects: List[str] = Field(json_schema_extra={"rdf_predicate": DC.subject}, default=[])
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.CompositeResource, frozen=True
    )
    identifier: IdentifierInRDF = Field(json_schema_extra={"rdf_predicate": DC.identifier}, frozen=True)
    creators: List[CreatorInRDF] = Field(json_schema_extra={"rdf_predicate": DC.creator}, default=[])

    contributors: List[ContributorInRDF] = Field(json_schema_extra={"rdf_predicate": DC.contributor}, default=[])
    relations: List[RelationInRDF] = Field(json_schema_extra={"rdf_predicate": DC.relation}, default=[])
    extended_metadata: List[ExtendedMetadataInRDF] = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.extendedMetadata}, default=[]
    )
    rights: RightsInRDF = Field(json_schema_extra={"rdf_predicate": DC.rights}, default=None)
    dates: List[DateInRDF] = Field(json_schema_extra={"rdf_predicate": DC.date}, default=[])
    awards: List[AwardInfoInRDF] = Field(json_schema_extra={"rdf_predicate": HSTERMS.awardInfo}, default=[])
    coverages: List[CoverageInRDF] = Field(json_schema_extra={"rdf_predicate": DC.coverage}, default=[])
    publisher: PublisherInRDF = Field(json_schema_extra={"rdf_predicate": DC.publisher}, default=None)
    citation: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.bibliographicCitation})

    _parse_rdf_subject = model_validator(mode='before')(rdf_parse_rdf_subject)
    _parse_coverages = model_validator(mode='before')(parse_coverages)
    _parse_extended_metadata = model_validator(mode='before')(parse_rdf_extended_metadata)
    _parse_rdf_dates = model_validator(mode='before')(parse_rdf_dates)
    _parse_description = model_validator(mode='before')(rdf_parse_description)

    _parse_identifier = field_validator("identifier", mode='before')(rdf_parse_identifier)
    _language_constraint = field_validator('language')(language_constraint)
    _dates_constraint = field_validator('dates')(dates_constraint)
    _coverages_constraint = field_validator('coverages')(coverages_constraint)
    _coverages_spatial_constraint = field_validator('coverages')(coverages_spatial_constraint)
    _sort_creators = field_validator("creators")(sort_creators)


class ResourceMetadataInRDF(BaseResource):
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.CompositeResource, frozen=True
    )
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.CompositeResource
    )

    _label_literal = Literal["Composite Resource"]
    label: _label_literal = Field(default="Composite Resource", frozen=True, alias='label')

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class CollectionMetadataInRDF(BaseResource):
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.CollectionResource, frozen=True
    )
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.CollectionResource
    )
    _label_literal = Literal["Collection Resource"]
    label: _label_literal = Field(default="Collection Resource", frozen=True, alias='label')

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)
