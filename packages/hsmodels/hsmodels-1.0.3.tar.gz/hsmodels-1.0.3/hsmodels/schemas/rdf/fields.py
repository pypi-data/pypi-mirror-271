from typing import Any, Callable, Optional

from pydantic.json_schema import JsonSchemaValue
from typing_extensions import Annotated

from datetime import datetime

from pydantic_core import core_schema
from pydantic import AnyUrl, BaseModel, EmailStr, Field, GetJsonSchemaHandler, HttpUrl, PositiveInt, \
    model_validator
from rdflib import BNode
from rdflib.term import Identifier as RDFIdentifier

from hsmodels.namespaces import DCTERMS, HSTERMS, RDF, RDFS
from hsmodels.schemas.enums import CoverageType, DateType, MultidimensionalSpatialReferenceType, SpatialReferenceType
from hsmodels.schemas.rdf.root_validators import parse_relation_rdf, rdf_parse_utc_offset, split_user_identifiers


class _RDFIdentifierTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """
        Reference: https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types
        """

        def validate_identifier(value: str) -> RDFIdentifier:
            result = RDFIdentifier(value)
            return result

        from_int_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_identifier),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_int_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(RDFIdentifier),
                    from_int_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.toPython()
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for RDFIdentifier
        return handler(_core_schema)


def get_RDF_IdentifierType(field: Field):
    return Annotated[RDFIdentifier, _RDFIdentifierTypePydanticAnnotation, field]


class RDFBaseModel(BaseModel):
    rdf_subject: get_RDF_IdentifierType(Field(default_factory=BNode))


class DCTypeInRDF(RDFBaseModel):
    is_defined_by: AnyUrl = Field(json_schema_extra={"rdf_predicate": RDFS.isDefinedBy})
    label: str = Field(json_schema_extra={"rdf_predicate": RDFS.label})


class RelationInRDF(RDFBaseModel):
    isExecutedBy: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.isExecutedBy}, default=None)
    isCreatedBy: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.isCreatedBy}, default=None)
    isDescribedBy: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.isDescribedBy}, default=None)
    isSimilarTo: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.isSimilarTo}, default=None)

    isPartOf: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.isPartOf}, default=None)
    hasPart: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.hasPart}, default=None)
    isVersionOf: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.isVersionOf}, default=None)
    isReplacedBy: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.isReplacedBy}, default=None)
    conformsTo: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.conformsTo}, default=None)
    hasFormat: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.hasFormat}, default=None)
    isFormatOf: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.isFormatOf}, default=None)
    isRequiredBy: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.isRequiredBy}, default=None)
    requires: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.requires}, default=None)
    isReferencedBy: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.isReferencedBy}, default=None)
    references: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.references}, default=None)
    replaces: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.replaces}, default=None)
    source: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.source}, default=None)

    _parse_relation = model_validator(mode='before')(parse_relation_rdf)


class DescriptionInRDF(RDFBaseModel):
    abstract: str = Field(json_schema_extra={"rdf_predicate": DCTERMS.abstract}, default=None)


class IdentifierInRDF(RDFBaseModel):
    hydroshare_identifier: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.hydroShareIdentifier})


class ExtendedMetadataInRDF(RDFBaseModel):
    value: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.value}, default="")
    key: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.key})


class CellInformationInRDF(RDFBaseModel):
    name: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.name})
    rows: int = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.rows})
    columns: int = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.columns})
    cell_size_x_value: float = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.cellSizeXValue})
    cell_size_y_value: float = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.cellSizeYValue})
    cell_data_type: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.cellDataType})


class DateInRDF(RDFBaseModel):
    type: DateType = Field(json_schema_extra={"rdf_predicate": RDF.type})
    value: datetime = Field(json_schema_extra={"rdf_predicate": RDF.value})


class RightsInRDF(RDFBaseModel):
    statement: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.rightsStatement})
    url: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.URL})


class CreatorInRDF(RDFBaseModel):
    creator_order: Optional[PositiveInt] = Field(
        default=None, json_schema_extra={"rdf_predicate": HSTERMS.creatorOrder}
    )
    name: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.name})
    phone: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.phone})
    address: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.address})
    organization: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.organization})
    email: EmailStr = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.email})
    homepage: HttpUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.homepage})
    hydroshare_user_id: int = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.hydroshare_user_id})
    ORCID: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.ORCID})
    google_scholar_id: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.GoogleScholarID})
    research_gate_id: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.ResearchGateID})

    _group_identifiers = model_validator(mode='before')(split_user_identifiers)


class ContributorInRDF(RDFBaseModel):
    name: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.name})
    phone: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.phone})
    address: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.address})
    organization: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.organization})
    email: EmailStr = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.email})
    homepage: HttpUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.homepage})
    hydroshare_user_id: int = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.hydroshare_user_id})
    ORCID: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.ORCID})
    google_scholar_id: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.GoogleScholarID})
    research_gate_id: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.ResearchGateID})

    _group_identifiers = model_validator(mode='before')(split_user_identifiers)


class AwardInfoInRDF(RDFBaseModel):
    funding_agency_name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.fundingAgencyName})
    title: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.awardTitle})
    number: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.awardNumber})
    funding_agency_url: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.fundingAgencyURL})


class BandInformationInRDF(RDFBaseModel):
    name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.name})
    variable_name: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.variableName})
    variable_unit: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.variableUnit})
    no_data_value: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.noDataValue})
    maximum_value: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.maximumValue})
    comment: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.comment})
    method: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.method})
    minimum_value: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.minimumValue})


class CoverageInRDF(RDFBaseModel):
    type: CoverageType = Field(json_schema_extra={"rdf_predicate": RDF.type})
    value: str = Field(json_schema_extra={"rdf_predicate": RDF.value})


class SpatialReferenceInRDF(RDFBaseModel):
    type: SpatialReferenceType = Field(json_schema_extra={"rdf_predicate": RDF.type})
    value: str = Field(json_schema_extra={"rdf_predicate": RDF.value})


class MultidimensionalSpatialReferenceInRDF(RDFBaseModel):
    type: MultidimensionalSpatialReferenceType = Field(json_schema_extra={"rdf_predicate": RDF.type})
    value: str = Field(json_schema_extra={"rdf_predicate": RDF.value})


class FieldInformationInRDF(RDFBaseModel):
    field_name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.fieldName})
    field_type: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.fieldType})
    field_type_code: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.fieldTypeCode})
    field_width: int = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.fieldWidth})
    field_precision: int = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.fieldPrecision})


class GeometryInformationInRDF(RDFBaseModel):
    feature_count: int = Field(default=0, json_schema_extra={"rdf_predicate": HSTERMS.featureCount})
    geometry_type: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.geometryType})


class VariableInRDF(RDFBaseModel):
    name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.name})
    unit: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.unit})
    type: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.type})
    shape: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.shape})
    descriptive_name: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.descriptive_name})
    method: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.method})
    missing_value: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.missing_value})


class PublisherInRDF(RDFBaseModel):
    name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.publisherName})
    url: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.publisherURL})


class TimeSeriesVariableInRDF(RDFBaseModel):
    variable_code: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.VariableCode})
    variable_name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.VariableName})
    variable_type: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.VariableType})
    no_data_value: int = Field(json_schema_extra={"rdf_predicate": HSTERMS.NoDataValue})
    variable_definition: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.VariableDefinition})
    speciation: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.Speciation})
    

class TimeSeriesSiteInRDF(RDFBaseModel):
    site_code: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.SiteCode})
    site_name: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.SiteName})
    elevation_m: float = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.Elevation_m})
    elevation_datum: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.ElevationDatum})
    site_type: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.SiteType})
    latitude: float = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.Latitude})
    longitude: float = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.Longitude})


class TimeSeriesMethodInRDF(RDFBaseModel):
    method_code: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.MethodCode})
    method_name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.MethodName})
    method_type: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.MethodType})
    method_description: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.MethodDescription})
    method_link: AnyUrl = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.MethodLink})


class ProcessingLevelInRDF(RDFBaseModel):
    processing_level_code: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.ProcessingLevelCode})
    definition: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.Definition})
    explanation: str = Field(default=None, json_schema_extra={"rdf_predicate": HSTERMS.Explanation})


class UnitInRDF(RDFBaseModel):
    type: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.UnitsType})
    name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.UnitsName})
    abbreviation: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.UnitsAbbreviation})


class UTCOffSetInRDF(RDFBaseModel):
    value: float = Field(json_schema_extra={"rdf_predicate": HSTERMS.value})


class TimeSeriesResultInRDF(RDFBaseModel):
    series_id: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.timeSeriesResultUUID})
    unit: UnitInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.unit}, default=None)
    status: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.Status}, default=None)
    sample_medium: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.SampleMedium})
    value_count: int = Field(json_schema_extra={"rdf_predicate": HSTERMS.ValueCount})
    aggregation_statistic: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.AggregationStatistic})
    series_label: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.SeriesLabel}, default=None)
    site: TimeSeriesSiteInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.site})
    variable: TimeSeriesVariableInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.variable})
    method: TimeSeriesMethodInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.method})
    processing_level: ProcessingLevelInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.processingLevel})
    utc_offset: UTCOffSetInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.UTCOffSet}, default=None)

    _parse_utc_offset = model_validator(mode='before')(rdf_parse_utc_offset)
