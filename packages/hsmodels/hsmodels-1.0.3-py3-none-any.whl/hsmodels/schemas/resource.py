from datetime import datetime
from typing import Dict, List, Union, Literal, Optional

from pydantic import AnyUrl, ConfigDict, Field, GetJsonSchemaHandler, field_validator, model_validator
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema

from hsmodels.schemas.base_models import BaseMetadata
from hsmodels.schemas.fields import (
    AwardInfo,
    BoxCoverage,
    Contributor,
    Creator,
    PeriodCoverage,
    PointCoverage,
    Publisher,
    Relation,
    Rights,
)
from hsmodels.schemas.rdf.validators import language_constraint, subjects_constraint
from hsmodels.schemas.root_validators import (
    normalize_additional_metadata,
    parse_abstract,
    parse_additional_metadata,
    parse_url,
    split_coverages,
    split_dates,
)
from hsmodels.schemas.validators import list_not_empty, parse_identifier, parse_spatial_coverage


class ResourceMetadataIn(BaseMetadata):
    """
    A class used to represent the metadata for a resource
    """

    model_config = ConfigDict(title="Resource Metadata")

    title: str = Field(
        max_length=300, title="Title", description="A string containing the name given to a resource"
    )
    abstract: str = Field(default=None, title="Abstract", description="A string containing a summary of a resource")
    language: str = Field(
        default="eng",
        title="Language",
        description="A 3-character string for the language in which the metadata and content of a resource are expressed",
    )
    subjects: List[str] = Field(
        default=[], title="Subject keywords", description="A list of keyword strings expressing the topic of a resource"
    )
    creators: List[Creator] = Field(
        default=[],
        title="Creators",
        description="A list of Creator objects indicating the entities responsible for creating a resource",
    )
    contributors: List[Contributor] = Field(
        default=[],
        title="Contributors",
        description="A list of Contributor objects indicating the entities that contributed to a resource",
    )
    relations: List[Relation] = Field(
        default=[],
        title="Related resources",
        description="A list of Relation objects representing resources related to a described resource",
    )
    additional_metadata: Dict[str, str] = Field(
        default={},
        title="Additional metadata",
        description="A dictionary containing key-value pair metadata associated with a resource",
    )
    rights: Rights = Field(
        default_factory=Rights.Creative_Commons_Attribution_CC_BY,
        title="Rights",
        description="An object containing information about rights held in an over a resource",
    )
    awards: List[AwardInfo] = Field(
        default=[],
        title="Funding agency information",
        description="A list of objects containing information about the funding agencies and awards associated with a resource",
    )
    spatial_coverage: Optional[Union[PointCoverage, BoxCoverage]] = Field(
        default=None,
        title="Spatial coverage",
        description="An object containing information about the spatial topic of a resource, the spatial applicability of a resource, or jurisdiction under with a resource is relevant",
    )
    period_coverage: Optional[PeriodCoverage] = Field(
        default=None,
        title="Temporal coverage",
        description="An object containing information about the temporal topic or applicability of a resource",
    )
    publisher: Publisher = Field(
        default=None,
        title="Publisher",
        description="An object containing information about the publisher of a resource",
    )
    citation: str = Field(
        default=None, title="Citation", description="A string containing the biblilographic citation for a resource"
    )

    _parse_coverages = model_validator(mode='before')(split_coverages)
    _parse_additional_metadata = model_validator(mode='before')(parse_additional_metadata)
    _parse_abstract = model_validator(mode='before')(parse_abstract)

    _parse_spatial_coverage = field_validator("spatial_coverage", mode='before')(parse_spatial_coverage)

    _normalize_additional_metadata = model_validator(mode='before')(normalize_additional_metadata)

    _subjects_constraint = field_validator('subjects')(subjects_constraint)
    _language_constraint = field_validator('language')(language_constraint)
    _creators_constraint = field_validator('creators')(list_not_empty)

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


class BaseResourceMetadata(ResourceMetadataIn):
    url: AnyUrl = Field(
        title="URL",
        description="An object containing the URL for a resource",
        frozen=True, json_schema_extra={"readOnly": True},
    )

    identifier: AnyUrl = Field(
        title="Identifier",
        description="An object containing the URL-encoded unique identifier for a resource",
        frozen=True,
        json_schema_extra={"readOnly": True},
    )
    created: datetime = Field(
        default_factory=datetime.now,
        title="Creation date",
        description="A datetime object containing the instant associated with when a resource was created",
        frozen=True,
        json_schema_extra={"readOnly": True},
    )
    modified: datetime = Field(
        default_factory=datetime.now,
        title="Modified date",
        description="A datetime object containing the instant associated with when a resource was last modified",
        frozen=True,
        json_schema_extra={"readOnly": True},
    )
    review_started: datetime = Field(
        default=None,
        title="Review started date",
        description="A datetime object containing the instant associated with when metadata review started on a resource",
        frozen=True,
        json_schema_extra={"readOnly": True},
    )
    published: datetime = Field(
        default=None,
        title="Published date",
        description="A datetime object containing the instant associated with when a resource was published",
        frozen=True,
        json_schema_extra={"readOnly": True},
    )

    _parse_dates = model_validator(mode='before')(split_dates)
    _parse_url = model_validator(mode='before')(parse_url)

    _parse_identifier = field_validator("identifier", mode='before')(parse_identifier)


class ResourceMetadata(BaseResourceMetadata):
    type: Literal['CompositeResource'] = Field(
        frozen=True,
        default="CompositeResource",
        title="Resource Type",
        description="An object containing a URL that points to the HydroShare resource type selected from the hsterms namespace",
        json_schema_extra={"readOnly": True},
    )


class CollectionMetadata(BaseResourceMetadata):
    type: Literal['CollectionResource'] = Field(
        frozen=True,
        default="CollectionResource",
        title="Resource Type",
        description="An object containing a URL that points to the HydroShare resource type selected from the hsterms namespace",
        json_schema_extra={"readOnly": True},
    )
