from typing import get_origin

import pytest

from hsmodels.schemas.aggregations import (
    FileSetMetadata,
    GeographicFeatureMetadata,
    GeographicRasterMetadata,
    ModelInstanceMetadata,
    ModelProgramMetadata,
    MultidimensionalMetadata,
    ReferencedTimeSeriesMetadata,
    SingleFileMetadata,
    TimeSeriesMetadata,
)
from hsmodels.schemas.rdf.aggregations import (
    FileSetMetadataInRDF,
    GeographicFeatureMetadataInRDF,
    GeographicRasterMetadataInRDF,
    ModelInstanceMetadataInRDF,
    ModelProgramMetadataInRDF,
    MultidimensionalMetadataInRDF,
    ReferencedTimeSeriesMetadataInRDF,
    SingleFileMetadataInRDF,
    TimeSeriesMetadataInRDF,
)
from hsmodels.schemas.rdf.resource import CollectionMetadataInRDF, ResourceMetadataInRDF
from hsmodels.schemas.resource import CollectionMetadata, ResourceMetadata

schema_list_count = [
    (ResourceMetadata, 5),
    (CollectionMetadata, 5),
    (GeographicRasterMetadata, 1),
    (GeographicFeatureMetadata, 2),
    (MultidimensionalMetadata, 2),
    (ReferencedTimeSeriesMetadata, 1),
    (FileSetMetadata, 1),
    (SingleFileMetadata, 1),
    (TimeSeriesMetadata, 2),
    (ModelProgramMetadata, 4),
    (ModelInstanceMetadata, 1),
    (ResourceMetadataInRDF, 8),
    (CollectionMetadataInRDF, 8),
    (GeographicRasterMetadataInRDF, 3),
    (GeographicFeatureMetadataInRDF, 4),
    (MultidimensionalMetadataInRDF, 4),
    (ReferencedTimeSeriesMetadataInRDF, 3),
    (SingleFileMetadataInRDF, 3),
    (TimeSeriesMetadataInRDF, 4),
    (ModelProgramMetadataInRDF, 9),
    (ModelInstanceMetadataInRDF, 3),
    (FileSetMetadataInRDF, 3),
]


@pytest.mark.parametrize("schema_list_count", schema_list_count)
def test_lists_default_empty(schema_list_count):
    schema, number_of_lists = schema_list_count
    list_count = 0
    for f in schema.model_fields.values():
        origin = get_origin(f.annotation)
        if origin is list:
            assert f.default == []
            list_count = list_count + 1
    assert list_count == number_of_lists
