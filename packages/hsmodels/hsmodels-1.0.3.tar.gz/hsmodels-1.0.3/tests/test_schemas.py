import pytest

from hsmodels.schemas import (
    CollectionMetadata,
    FileSetMetadata,
    GeographicFeatureMetadata,
    GeographicRasterMetadata,
    ModelInstanceMetadata,
    ModelProgramMetadata,
    MultidimensionalMetadata,
    ReferencedTimeSeriesMetadata,
    ResourceMetadata,
    SingleFileMetadata,
    TimeSeriesMetadata,
)
from hsmodels.schemas.fields import (
    BoxCoverage,
    BoxSpatialReference,
    Contributor,
    Creator,
    PointCoverage,
    PointSpatialReference,
)

read_only_fields = [
    (ResourceMetadata, ['type', 'identifier', 'created', 'modified', 'review_started', 'published', 'url']),
    (CollectionMetadata, ['type', 'identifier', 'created', 'modified', 'review_started', 'published', 'url']),
    (GeographicRasterMetadata, ['type', 'url']),
    (ModelProgramMetadata, ['type', 'url']),
    (ModelInstanceMetadata, ['type', 'url']),
    (GeographicFeatureMetadata, ['type', 'url']),
    (MultidimensionalMetadata, ['type', 'url']),
    (ReferencedTimeSeriesMetadata, ['type', 'url']),
    (FileSetMetadata, ['type', 'url']),
    (SingleFileMetadata, ['type', 'url']),
    (TimeSeriesMetadata, ['type', 'url']),
    (Creator, ['hydroshare_user_id']),
    (Contributor, ['hydroshare_user_id']),
    (BoxCoverage, ['type']),
    (BoxSpatialReference, ['type']),
    (PointSpatialReference, ['type']),
    (PointCoverage, ['type']),
]


@pytest.mark.parametrize("read_only_field", read_only_fields)
def test_readonly(read_only_field):
    clazz, fields = read_only_field
    s = clazz.model_json_schema()["properties"]
    for field in s:
        if field in fields:
            assert "readOnly" in s[field] and s[field]["readOnly"] is True
        else:
            assert "readOnly" not in s[field]


additional_metadata_fields = [
    (ResourceMetadata, ['additional_metadata']),
    (CollectionMetadata, ['additional_metadata']),
    (GeographicRasterMetadata, ['additional_metadata']),
    (GeographicFeatureMetadata, ['additional_metadata']),
    (MultidimensionalMetadata, ['additional_metadata']),
    (ReferencedTimeSeriesMetadata, ['additional_metadata']),
    (FileSetMetadata, ['additional_metadata']),
    (SingleFileMetadata, ['additional_metadata']),
    (TimeSeriesMetadata, ['additional_metadata']),
    (ModelProgramMetadata, ['additional_metadata']),
    (ModelInstanceMetadata, ['additional_metadata']),
]


@pytest.mark.parametrize("additional_metadata_field", additional_metadata_fields)
def test_dictionary_field(additional_metadata_field):
    clazz, fields = additional_metadata_field
    s = clazz.model_json_schema()["properties"]

    for field in fields:
        assert 'additionalProperties' not in s[field]
        assert 'default' not in s[field]
        assert s[field]['items'] == {
            "type": "object",
            "title": "Key-Value",
            "description": "A key-value pair",
            "default": [],
            "properties": {"key": {"type": "string"}, "value": {"type": "string"}},
        }
