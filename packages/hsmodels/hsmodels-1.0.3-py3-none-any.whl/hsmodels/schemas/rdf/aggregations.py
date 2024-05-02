from datetime import date
from typing import List, Literal

from pydantic import AnyUrl, Field, field_serializer, model_validator
from rdflib import URIRef

from hsmodels.namespaces import DC, HSTERMS, RDF
from hsmodels.schemas.rdf.fields import (
    BandInformationInRDF,
    CellInformationInRDF,
    CoverageInRDF,
    DescriptionInRDF,
    ExtendedMetadataInRDF,
    FieldInformationInRDF,
    GeometryInformationInRDF,
    MultidimensionalSpatialReferenceInRDF,
    RDFBaseModel,
    RightsInRDF,
    SpatialReferenceInRDF,
    TimeSeriesResultInRDF,
    VariableInRDF,
)
from hsmodels.schemas.rdf.root_validators import (
    parse_coverages,
    parse_rdf_extended_metadata,
    parse_rdf_multidimensional_spatial_reference,
    parse_rdf_spatial_reference,
    rdf_parse_description,
    rdf_parse_file_types,
    rdf_parse_rdf_subject,
)


class BaseAggregationMetadataInRDF(RDFBaseModel):
    _parse_rdf_subject = model_validator(mode='before')(rdf_parse_rdf_subject)

    title: str = Field(json_schema_extra={"rdf_predicate": DC.title})
    subjects: List[str] = Field(json_schema_extra={"rdf_predicate": DC.subject}, default=[])
    language: str = Field(json_schema_extra={"rdf_predicate": DC.language}, default="eng")
    extended_metadata: List[ExtendedMetadataInRDF] = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.extendedMetadata}, default=[]
    )
    coverages: List[CoverageInRDF] = Field(json_schema_extra={"rdf_predicate": DC.coverage}, default=[])
    rights: RightsInRDF = Field(json_schema_extra={"rdf_predicate": DC.rights}, default=[])

    _parse_coverages = model_validator(mode='before')(parse_coverages)

    _parse_extended_metadata = model_validator(mode='before')(parse_rdf_extended_metadata)


class GeographicRasterMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.GeographicRasterAggregation)
    _label_literal = Literal["Geographic Raster Content: A geographic grid represented by a virtual raster tile (.vrt) file and one or more geotiff (.tif) files"]
    label: _label_literal = Field(
        frozen=True,
        default="Geographic Raster Content: A geographic grid represented by a virtual "
        "raster tile (.vrt) file and one or more geotiff (.tif) files",
    )
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.GeographicRasterAggregation, frozen=True
    )

    band_information: BandInformationInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.BandInformation})
    spatial_reference: SpatialReferenceInRDF = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.spatialReference}, default=None
    )
    cell_information: CellInformationInRDF = Field(json_schema_extra={"rdf_predicate": HSTERMS.CellInformation})

    _parse_spatial_reference = model_validator(mode='before')(parse_rdf_spatial_reference)

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class GeographicFeatureMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.GeographicFeatureAggregation
    )

    _label_literal = Literal["Geographic Feature Content: The multiple files that are part of a geographic shapefile"]
    label: _label_literal = Field(
        frozen=True, default="Geographic Feature Content: The multiple files that are part of a " "geographic shapefile"
    )
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.GeographicFeatureAggregation, frozen=True
    )

    field_information: List[FieldInformationInRDF] = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.FieldInformation}, default=[]
    )
    geometry_information: GeometryInformationInRDF = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.GeometryInformation}
    )
    spatial_reference: SpatialReferenceInRDF = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.spatialReference}, default=None
    )

    _parse_spatial_reference = model_validator(mode='before')(parse_rdf_spatial_reference)

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class MultidimensionalMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.MultidimensionalAggregation
    )
    _label_literal = Literal['Multidimensional Content: A multidimensional dataset represented by a NetCDF file (.nc) and text file giving its NetCDF header content']
    label: _label_literal = Field(
        frozen=True,
        default="Multidimensional Content: A multidimensional dataset represented by a "
        "NetCDF file (.nc) and text file giving its NetCDF header content",
    )
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.MultidimensionalAggregation, frozen=True
    )

    variables: List[VariableInRDF] = Field(json_schema_extra={"rdf_predicate": HSTERMS.Variable}, default=[])
    spatial_reference: MultidimensionalSpatialReferenceInRDF = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.spatialReference}, default=None
    )

    _parse_spatial_reference = model_validator(mode='before')(parse_rdf_multidimensional_spatial_reference)

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class TimeSeriesMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.TimeSeriesAggregation
    )

    _label_literal = Literal["Time Series Content: One or more time series held in an ODM2 format SQLite file and optional source comma separated (.csv) files"]
    label: _label_literal = Field(
        frozen=True,
        default="Time Series Content: One or more time series held in an ODM2 format "
        "SQLite file and optional source comma separated (.csv) files",
    )
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.TimeSeriesAggregation, frozen=True
    )
    description: DescriptionInRDF = Field(
        json_schema_extra={"rdf_predicate": DC.description}, default_factory=DescriptionInRDF
    )

    time_series_results: List[TimeSeriesResultInRDF] = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.timeSeriesResult}, default=[]
    )

    _parse_description = model_validator(mode='before')(rdf_parse_description)

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class ReferencedTimeSeriesMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.ReferencedTimeSeriesAggregation
    )

    _label_literal = Literal["Referenced Time Series Content: A reference to one or more time series served from HydroServers outside of HydroShare in WaterML format"]
    label: _label_literal = Field(
        frozen=True,
        default="Referenced Time Series Content: A reference to one or more time series "
        "served from HydroServers outside of HydroShare in WaterML format",
    )
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.ReferencedTimeSeriesAggregation, frozen=True
    )

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class FileSetMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.FileSetAggregation
    )
    _label_literal = Literal["File Set Content: One or more files with specific metadata"]
    label: _label_literal = Field(frozen=True, default="File Set Content: One or more files with specific metadata")
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.FileSetAggregation, frozen=True
    )

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class SingleFileMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.SingleFileAggregation
    )

    _label_literal = Literal["Single File Content: A single file with file specific metadata"]
    label: _label_literal = Field(frozen=True, default="Single File Content: A single file with file specific metadata")
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.SingleFileAggregation, frozen=True
    )

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class ModelProgramMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.ModelProgramAggregation
    )

    _label_literal = Literal["Model Program Content: One or more files with specific metadata"]
    label: _label_literal = Field(frozen=True, default="Model Program Content: One or more files with specific metadata")
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.ModelProgramAggregation, frozen=True
    )

    name: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelProgramName}, default=None)
    version: str = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelVersion}, default=None)
    programming_languages: List[str] = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.modelProgramLanguage}, default=[]
    )
    operating_systems: List[str] = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.modelOperatingSystem}, default=[]
    )
    release_date: date = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.modelReleaseDate}, default=None
    )
    website: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.modelWebsite}, default=None
    )
    code_repository: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelCodeRepository}, default=None)
    program_schema_json: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelProgramSchema}, default=None)

    release_notes: List[AnyUrl] = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelReleaseNotes}, default=[])
    documentation: List[AnyUrl] = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelDocumentation}, default=[])
    software: List[AnyUrl] = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelSoftware}, default=[])
    engine: List[AnyUrl] = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelEngine}, default=[])

    _parse_file_types = model_validator(mode='before')(rdf_parse_file_types)

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)


class ModelInstanceMetadataInRDF(BaseAggregationMetadataInRDF):
    rdf_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": RDF.type}, frozen=True, default=HSTERMS.ModelInstanceAggregation
    )

    _label_literal = Literal["Model Instance Content: One or more files with specific metadata"]
    label: _label_literal = Field(frozen=True, default="Model Instance Content: One or more files with specific metadata")
    dc_type: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": DC.type}, default=HSTERMS.ModelInstanceAggregation, frozen=True
    )

    includes_model_output: bool = Field(json_schema_extra={"rdf_predicate": HSTERMS.includesModelOutput})
    executed_by: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.executedByModelProgram}, default=None)
    program_schema_json: AnyUrl = Field(json_schema_extra={"rdf_predicate": HSTERMS.modelProgramSchema}, default=None)
    program_schema_json_values: AnyUrl = Field(
        json_schema_extra={"rdf_predicate": HSTERMS.modelProgramSchemaValues}, default=None
    )

    @field_serializer('dc_type', 'rdf_type')
    def serialize_url(self, _type: URIRef, _info):
        return AnyUrl(_type)
