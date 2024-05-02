import json
import os

import pytest

from hsmodels.schemas.aggregations import (
    FileSetMetadataIn,
    GeographicFeatureMetadataIn,
    GeographicRasterMetadataIn,
    ModelInstanceMetadataIn,
    ModelProgramMetadataIn,
    MultidimensionalMetadataIn,
    ReferencedTimeSeriesMetadataIn,
    SingleFileMetadataIn,
    TimeSeriesMetadataIn,
)
from hsmodels.schemas.resource import ResourceMetadataIn


def sorting(item):
    if isinstance(item, dict):
        return sorted((key, sorting(values)) for key, values in item.items())
    if isinstance(item, list):
        return sorted(sorting(x) for x in item)
    else:
        return item


@pytest.fixture()
def res_md():
    with open("data/json/resource.json", 'r') as f:
        return ResourceMetadataIn(**json.loads(f.read()))


def test_resource_additional_metadata_dictionary(res_md):
    assert res_md.additional_metadata == {"key1": "value1", "key2": "value2", "key_empty": ""}
    res_md_in = ResourceMetadataIn(**res_md.model_dump())
    assert res_md_in.additional_metadata == {"key1": "value1", "key2": "value2", "key_empty": ""}

    assert res_md_in.model_dump()["additional_metadata"] == {"key1": "value1", "key2": "value2", "key_empty": ""}


metadata_json_input = [
    (ResourceMetadataIn, 'resource.json'),
    (GeographicRasterMetadataIn, 'geographicraster.json'),
    (GeographicFeatureMetadataIn, 'geographicfeature.json'),
    (MultidimensionalMetadataIn, 'multidimensional.json'),
    (ReferencedTimeSeriesMetadataIn, 'referencedtimeseries.refts.json'),
    (FileSetMetadataIn, 'fileset.json'),
    (SingleFileMetadataIn, 'singlefile.json'),
    (TimeSeriesMetadataIn, 'timeseries.json'),
    (ModelProgramMetadataIn, 'modelprogram.json'),
    (ModelInstanceMetadataIn, 'modelinstance.json'),
    (ResourceMetadataIn, 'collection.json'),
]


@pytest.mark.parametrize("metadata_json_input", metadata_json_input)
def test_metadata_json_serialization(metadata_json_input):
    in_schema, metadata_file = metadata_json_input
    metadata_file = os.path.join('data', 'json', metadata_file)
    with open(metadata_file, 'r') as f:
        json_file_str = f.read()
    md = in_schema.model_validate_json(json_file_str)
    from_schema = sorting(json.loads(md.model_dump_json()))
    from_file = sorting(json.loads(json_file_str))
    for i in range(1, len(from_file)):
        assert from_file[i] == from_schema[i]


def test_optional_fields_resource():
    with open("data/json/resource.json", 'r') as f:
        md = ResourceMetadataIn(**json.loads(f.read()))
    # test period_coverage is optional
    md.period_coverage = None
    # test spatial_coverage is optional
    md.spatial_coverage = None
    # test contributor is optional
    md.contributors = []
    # test relation is optional
    md.relations = []
    # test additional_metadata is optional
    md.additional_metadata = {}
    # test awards is optional
    md.awards = []
    # test subjects is optional
    md.subjects = []


def test_optional_fields_raster_aggr():
    with open("data/json/geographicraster.json", 'r') as f:
        md = GeographicRasterMetadataIn(**json.loads(f.read()))
    # test period_coverage is optional
    md.period_coverage = None
    # test some of the fields of the band_information are optional
    md.band_information.variable_name = None
    md.band_information.variable_unit = None
    md.band_information.maximum_value = None
    md.band_information.minimum_value = None
    md.band_information.no_data_value = None
    md.band_information.comment = None
    md.band_information.method = None


def test_optional_fields_geo_feature_aggr():
    with open("data/json/geographicfeature.json", 'r') as f:
        md = GeographicFeatureMetadataIn(**json.loads(f.read()))
    # test period_coverage is optional
    md.period_coverage = None

    # test some of the fields of the field_information are optional
    md.field_information[0].field_type_code = None
    md.field_information[0].field_width = None
    md.field_information[0].field_precision = None


def test_optional_fields_multidimensional_aggr():
    with open("data/json/multidimensional.json", 'r') as f:
        md = MultidimensionalMetadataIn(**json.loads(f.read()))
    # test variable optional attributes
    md.variables[0].method = None
    md.variables[0].descriptive_name = None
    md.variables[0].missing_value = None


def test_optional_fields_fileset_aggr():
    with open("data/json/fileset.json", 'r') as f:
        md = FileSetMetadataIn(**json.loads(f.read()))
    # test spatial_coverage is optional
    md.spatial_coverage = None
    # test period_coverage is optional
    md.period_coverage = None


def test_optional_fields_singlefile_aggr():
    with open("data/json/singlefile.json", 'r') as f:
        md = SingleFileMetadataIn(**json.loads(f.read()))
    # test spatial_coverage is optional
    md.spatial_coverage = None
    # test period_coverage is optional
    md.period_coverage = None


def test_optional_fields_timeseries_aggr():
    with open("data/json/timeseries.json", 'r') as f:
        md = TimeSeriesMetadataIn(**json.loads(f.read()))

    # test some of the fields of the variable are optional
    md.time_series_results[0].variable.variable_definition = None
    md.time_series_results[0].variable.speciation = None

    # test some of the fields of the site are optional
    md.time_series_results[0].site.site_name = None
    md.time_series_results[0].site.elevation_m = None
    md.time_series_results[0].site.elevation_datum = None
    md.time_series_results[0].site.site_type = None
    md.time_series_results[0].site.latitude = None
    md.time_series_results[0].site.longitude = None

    # test some of the fields of the method are optional
    md.time_series_results[0].method.method_description = None
    md.time_series_results[0].method.method_link = None

    # test some of the fields of the processing_level are optional
    md.time_series_results[0].processing_level.definition = None
    md.time_series_results[0].processing_level.explanation = None


def test_optional_fields_modelprogram_aggr():
    with open("data/json/modelprogram.json", 'r') as f:
        md = ModelProgramMetadataIn(**json.loads(f.read()))
    # test version is optional
    md.version = None
    # test release_date is optional
    md.release_date = None
    # test website is optional
    md.website = None
    # test code_repository is optional
    md.code_repository = None
    # test program_schema_json is optional
    md.program_schema_json = None


def test_optional_fields_modelinstance_aggr():
    with open("data/json/modelinstance.json", 'r') as f:
        md = ModelInstanceMetadataIn(**json.loads(f.read()))
    # test executed_by is optional
    md.executed_by = None
    # test program_schema_json is optional
    md.program_schema_json = None
    # test program_schema_json_values is optional
    md.program_schema_json_values = None
