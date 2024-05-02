from datetime import date
from typing import Dict, List, Optional, Union

from pydantic import AnyUrl, ConfigDict, Field, GetJsonSchemaHandler, model_validator, field_validator
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema

from hsmodels.schemas.base_models import BaseMetadata
from hsmodels.schemas.enums import AggregationType
from hsmodels.schemas.fields import (
    BandInformation,
    BoxCoverage,
    BoxSpatialReference,
    CellInformation,
    FieldInformation,
    GeometryInformation,
    ModelProgramFile,
    MultidimensionalBoxSpatialReference,
    MultidimensionalPointSpatialReference,
    PeriodCoverage,
    PointCoverage,
    PointSpatialReference,
    Rights,
    TimeSeriesResult,
    Variable,
)
from hsmodels.schemas.rdf.validators import language_constraint, subjects_constraint
from hsmodels.schemas.root_validators import (
    normalize_additional_metadata,
    parse_abstract,
    parse_additional_metadata,
    parse_file_types,
    parse_url,
    split_coverages,
)
from hsmodels.schemas.validators import (
    parse_multidimensional_spatial_reference,
    parse_spatial_coverage,
    parse_spatial_reference,
)


class BaseAggregationMetadataIn(BaseMetadata):
    title: str = Field(
        default=None,
        title="Aggregation title",
        description="A string containing a descriptive title for the aggregation",
    )
    subjects: List[str] = Field(
        default=[],
        title="Subject keywords",
        description="A list of keyword strings expressing the topic of the aggregation",
    )
    language: str = Field(
        default="eng",
        title="Language",
        description="The 3-character string for the language in which the metadata and content are expressed",
    )
    additional_metadata: Dict[str, str] = Field(
        default={},
        title="Additional metadata",
        description="A dictionary of additional metadata elements expressed as key-value pairs",
    )
    spatial_coverage: Optional[Union[PointCoverage, BoxCoverage]] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing the geospatial coverage for the aggregation expressed as either a bounding box or point",
    )
    period_coverage: Optional[PeriodCoverage] = Field(
        default=None,
        title="Temporal coverage",
        description="An object containing the temporal coverage for a aggregation expressed as a date range",
    )

    _parse_additional_metadata = model_validator(mode='before')(parse_additional_metadata)
    _parse_coverages = model_validator(mode='before')(split_coverages)

    _subjects_constraint = field_validator('subjects')(subjects_constraint)
    _language_constraint = field_validator('language')(language_constraint)
    _parse_spatial_coverage = field_validator("spatial_coverage", mode='before')(parse_spatial_coverage)
    _normalize_additional_metadata = model_validator(mode='before')(normalize_additional_metadata)

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        prop = json_schema['properties']['additional_metadata']
        prop.pop('default', None)
        prop.pop('additionalProperties', None)
        prop['type'] = 'array'
        prop['items'] = {
            "type": "object",
            "title": "Key-Value",
            "description": "A key-value pair",
            "default": [],
            "properties": {"key": {"type": "string"}, "value": {"type": "string"}},
        }

        return json_schema


class GeographicRasterMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a geographic raster aggregation

    A geographic raster aggregation consists of the multiple content files that make up a
    geographic raster dataset to which aggregation-level metadata have been added. Rasters
    may have multiple files and multiple bands and are stored in HydroShare as GeoTIFF files.
    """

    model_config = ConfigDict(title="Geographic Raster Aggregation Metadata")

    band_information: BandInformation = Field(
        title="Band information",
        description="An object containing information about the bands contained in the raster dataset",
    )
    spatial_coverage: Union[PointCoverage, BoxCoverage] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing the geospatial coverage for the aggregation expressed as either a bounding box or point",
    )
    spatial_reference: Union[BoxSpatialReference, PointSpatialReference] = Field(
        default=None,
        title="Spatial reference",
        description="An object containing spatial reference information for the dataset",
    )
    cell_information: CellInformation = Field(
        title="Cell information", description="An object containing information about the raster grid cells"
    )

    _parse_spatial_reference = field_validator("spatial_reference", mode='before')(parse_spatial_reference)


class GeographicRasterMetadata(GeographicRasterMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.GeographicRasterAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class GeographicFeatureMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a geographic feature aggregation

    A geographic feature aggregation consists of the multiple content files that make up an
    ESRI shapefile containing a geographic feature dataset and to which aggregation-level
    metadata have been added.
    """

    model_config = ConfigDict(title="Geographic Feature Aggregation Metadata")

    field_information: List[FieldInformation] = Field(
        default=[],
        title="Field information",
        description="A list of objects containing information about the fields in the dataset attribute table",
    )
    geometry_information: GeometryInformation = Field(
        title="Geometry information",
        description="An object containing information about the geometry of the features in the dataset",
    )
    spatial_coverage: Union[PointCoverage, BoxCoverage] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing the geospatial coverage for the aggregation expressed as either a bounding box or point",
    )
    spatial_reference: Union[BoxSpatialReference, PointSpatialReference] = Field(
        default=None,
        title="Spatial reference",
        description="An object containing spatial reference information for the dataset",
    )

    _parse_spatial_reference = field_validator("spatial_reference", mode='before')(parse_spatial_reference)


class GeographicFeatureMetadata(GeographicFeatureMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.GeographicFeatureAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class MultidimensionalMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a multidimensional space-time aggregation

    A multidimensional aggregation consists of a Network Common Data Form (NetCDF) file that
    makes up a multidimensional space-time dataset to which aggregation-level metadata have
    been added.
    """
    model_config = ConfigDict(title="Multidimensional Aggregation Metadata")

    variables: List[Variable] = Field(
        default=[],
        title="Variables",
        description="A list containing information about the variables for which data are stored in the dataset",
    )
    spatial_coverage: Union[PointCoverage, BoxCoverage] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing the geospatial coverage for the aggregation expressed as either a bounding box or point",
    )
    spatial_reference: Union[MultidimensionalBoxSpatialReference, MultidimensionalPointSpatialReference] = Field(
        default=None,
        title="Spatial reference",
        description="An object containing spatial reference information for the dataset",
    )
    period_coverage: PeriodCoverage = Field(
        default=None,
        title="Temporal coverage",
        description="An object containing the temporal coverage for a aggregation expressed as a date range",
    )
    _parse_spatial_reference = field_validator("spatial_reference", mode='before')(
        parse_multidimensional_spatial_reference
    )


class MultidimensionalMetadata(MultidimensionalMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.MultidimensionalAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class ReferencedTimeSeriesMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a referenced time series aggregation

    A referenced time series aggregation consists of references to specific time series
    datasets hosted on an external web service to which aggregation-level metadata have
    been added.
    """

    model_config = ConfigDict(title="Referenced Time Series Aggregation Metadata")


class ReferencedTimeSeriesMetadata(ReferencedTimeSeriesMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.ReferencedTimeSeriesAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class FileSetMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a file set aggregation

    A file set aggregation consists of an arbitrary collection of files that are logically
    grouped together as an aggregation and to which aggregation-level metadata have been
    added. There may be any number of files in the aggregation, and files may be of any type.
    """

    model_config = ConfigDict(title="File Set Aggregation Metadata")


class FileSetMetadata(FileSetMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.FileSetAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class SingleFileMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a single file aggregation

    A single file aggregation consists of a single content file to which aggregation-level
    metadata have been added.
    """

    model_config = ConfigDict(title="Single File Aggregation Metadata")


class SingleFileMetadata(SingleFileMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.SingleFileAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class TimeSeriesMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a time series aggregation

    A time series aggregation consists of one or more time series datasets to which
    aggregation-level metadata have been added. Time series datasets in HydroShare
    consist of sequences of individual data values that are ordered in time to record
    the changing trend of a certain phenomenon. They are stored in HydroShare using
    ODM2 SQLite database files.
    """

    model_config = ConfigDict(title="Time Series Aggregation Metadata")

    time_series_results: List[TimeSeriesResult] = Field(
        default=[],
        title="Time series results",
        description="A list of time series results contained within the time series aggregation",
    )

    abstract: Optional[str] = Field(default=None, title="Abstract", description="A string containing a summary of a aggregation")
    spatial_coverage: Union[PointCoverage, BoxCoverage] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing the geospatial coverage for the aggregation expressed as either a bounding box or point",
    )
    period_coverage: PeriodCoverage = Field(
        default=None,
        title="Temporal coverage",
        description="An object containing the temporal coverage for a aggregation expressed as a date range",
    )

    _parse_abstract = model_validator(mode='before')(parse_abstract)


class TimeSeriesMetadata(TimeSeriesMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.TimeSeriesAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class ModelProgramMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a model program aggregation
    """

    model_config = ConfigDict(title="Model Program Aggregation Metadata")

    version: Optional[str] = Field(
        default=None, title="Version", description="The software version or build number of the model", max_length=255
    )

    programming_languages: List[str] = Field(
        default=[],
        max_length=100,
        title="Programming Languages",
        description="The programming languages that the model is written in",
    )

    operating_systems: List[str] = Field(
        default=[],
        max_length=100,
        title="Operating Systems",
        description="Compatible operating systems to setup and run the model",
    )

    release_date: Optional[date] = Field(
        default=None, title="Release Date", description="The date that this version of the model was released"
    )

    website: Optional[AnyUrl] = Field(
        default=None,
        title='Website',
        description='A URL to a website describing the model that is maintained by the model developers',
    )

    code_repository: Optional[AnyUrl] = Field(
        default=None,
        title='Software Repository',
        description='A URL to the source code repository for the model code (e.g., git, mercurial, svn, etc.)',
    )

    file_types: List[ModelProgramFile] = Field(
        default=[], title='File Types', description='File types used by the model program'
    )

    program_schema_json: Optional[AnyUrl] = Field(
        default=None,
        title='Model program schema',
        description='A url to the JSON metadata schema for the model program',
    )

    _parse_file_types = model_validator(mode='before')(parse_file_types)


class ModelProgramMetadata(ModelProgramMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.ModelProgramAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)


class ModelInstanceMetadataIn(BaseAggregationMetadataIn):
    """
    A class used to represent the metadata associated with a model instance aggregation
    """

    model_config = ConfigDict(title="Model Instance Aggregation Metadata")

    includes_model_output: bool = Field(
        title="Includes Model Output",
        description="Indicates whether model output files are included in the aggregation",
    )

    executed_by: Optional[AnyUrl] = Field(
        default=None,
        title="Executed By",
        description="A URL to the Model Program that can be used to execute this model instance",
    )

    program_schema_json: Optional[AnyUrl] = Field(
        default=None,
        title="JSON Metadata schema URL",
        description="A URL to the JSON metadata schema for the related model program",
    )

    program_schema_json_values: Optional[AnyUrl] = Field(
        default=None,
        title="JSON metadata schema values URL",
        description="A URL to a JSON file containing the metadata values conforming to the JSON metadata schema for the related model program",
    )


class ModelInstanceMetadata(ModelInstanceMetadataIn):
    type: AggregationType = Field(
        frozen=True,
        default=AggregationType.ModelInstanceAggregation,
        title="Aggregation type",
        description="A string expressing the aggregation type from the list of HydroShare aggregation types",
        json_schema_extra={"readOnly": True},
    )

    url: AnyUrl = Field(
        title="Aggregation URL", description="An object containing the URL of the aggregation", frozen=True,
        json_schema_extra={"readOnly": True},
    )

    rights: Optional[Rights] = Field(
        default=None,
        title="Rights statement",
        description="An object containing information about the rights held in and over the aggregation and the license under which a aggregation is shared",
    )

    _parse_url = model_validator(mode='before')(parse_url)
