from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from hsmodels.namespaces import DCTERMS
from hsmodels.schemas import GeographicRasterMetadata, load_rdf
from hsmodels.schemas.enums import AggregationType, DateType, VariableType
from hsmodels.schemas.fields import BoxCoverage, Contributor, Creator, PeriodCoverage, Rights, Variable
from hsmodels.schemas.rdf.fields import DateInRDF, ExtendedMetadataInRDF
from hsmodels.schemas.resource import ResourceMetadata


@pytest.fixture()
def res_md():
    with open("data/metadata/resourcemetadata.xml", 'r') as f:
        return load_rdf(f.read())


@pytest.fixture()
def agg_md():
    with open("data/metadata/geographicraster_meta.xml", 'r') as f:
        return load_rdf(f.read())


def test_resource_metadata_language(res_md):
    try:
        res_md.language = "badcode"
        assert False, "language validator must not be working"
    except ValueError as ve:
        assert "language 'badcode' must be a 3 letter iso language code" in str(ve)


def test_extended_metadata():
    em = ExtendedMetadataInRDF(key='key1', value='value1')
    assert em.key == 'key1'
    assert em.value == 'value1'
    try:
        ExtendedMetadataInRDF()
        assert False, "ExtendedMetadata key/value are required"
    except ValueError as ve:
        assert "Field required" in str(ve)


def test_dates():
    now = datetime.now()
    d = DateInRDF(type=str(DCTERMS.modified), value=now)
    assert d.type == DateType.modified
    assert d.value == now
    try:
        DateInRDF()
        assert False, "Date type/value are required"
    except ValidationError as ve:
        assert "2 validation errors for Date" in str(ve)


def test_variables():
    variable = Variable(
        name="name",
        type=VariableType.Byte,
        unit="unit",
        shape="shape",
        descriptive_name="descriptive_name",
        method="method",
        missing_value="missing_value",
    )
    assert variable.name == "name"
    assert variable.type == VariableType.Byte
    assert variable.unit == "unit"
    assert variable.shape == "shape"
    assert variable.descriptive_name == "descriptive_name"
    assert variable.method == "method"
    assert variable.missing_value == "missing_value"

    try:
        Variable()
        assert False, "Some Variable fields should be required"
    except ValidationError as ve:
        assert "4 validation errors for Multidimensional Variable" in str(ve)
        assert "name" in str(ve)
        assert "unit" in str(ve)
        assert "type" in str(ve)
        assert "shape" in str(ve)


def test_rights():
    assert Rights.Creative_Commons_Attribution_CC_BY() == Rights(
        statement="This resource is shared under the Creative Commons Attribution CC BY.",
        url="http://creativecommons.org/licenses/by/4.0/",
    )

    assert Rights.Creative_Commons_Attribution_ShareAlike_CC_BY() == Rights(
        statement="This resource is shared under the Creative Commons Attribution-ShareAlike CC BY-SA.",
        url="http://creativecommons.org/licenses/by-sa/4.0/",
    )

    assert Rights.Creative_Commons_Attribution_NoDerivs_CC_BY_ND() == Rights(
        statement="This resource is shared under the Creative Commons Attribution-ShareAlike CC BY-SA.",
        url="http://creativecommons.org/licenses/by-nd/4.0/",
    )

    assert Rights.Creative_Commons_Attribution_NoCommercial_ShareAlike_CC_BY_NC_SA() == Rights(
        statement="This resource is shared under the Creative Commons Attribution-NoCommercial-ShareAlike"
        " CC BY-NC-SA.",
        url="http://creativecommons.org/licenses/by-nc-sa/4.0/",
    )

    assert Rights.Creative_Commons_Attribution_NoCommercial_CC_BY_NC() == Rights(
        statement="This resource is shared under the Creative Commons Attribution-NoCommercial CC BY-NC.",
        url="http://creativecommons.org/licenses/by-nc/4.0/",
    )

    assert Rights.Creative_Commons_Attribution_NoCommercial_NoDerivs_CC_BY_NC_ND() == Rights(
        statement="This resource is shared under the Creative Commons Attribution-NoCommercial-NoDerivs "
        "CC BY-NC-ND.",
        url="http://creativecommons.org/licenses/by-nc-nd/4.0/",
    )

    assert Rights.Other("a statement", "https://www.hydroshare.org") == Rights(
        statement="a statement", url="https://www.hydroshare.org"
    )


def test_period_constraints_error():
    start = datetime.now()
    end = datetime.now() - timedelta(seconds=1)
    try:
        PeriodCoverage(start=start, end=end)
        assert False, "Should have raised error"
    except ValueError as e:
        assert f"start date [{start}] is after end date [{end}]" in str(e)


def test_period_constraint_happy_path():
    start = datetime.now()
    end = datetime.now() + timedelta(seconds=1)
    pc = PeriodCoverage(name="hello", start=start, end=end)
    assert pc.start == start
    assert pc.end == end
    assert pc.name == "hello"


def test_box_constraints_north_south():
    box_coverage = BoxCoverage(
        name="asdfsadf",
        northlimit=42.1505,
        eastlimit=-84.5739,
        projection='WGS 84 EPSG:4326',
        southlimit=30.282,
        units='Decimal Degrees',
        westlimit=-104.7887,
    )

    try:
        box_coverage.northlimit = 29
        assert False, "Should have thrown error"
    except ValueError as e:
        assert "North latitude [29.0] must be greater than or equal to South latitude [30.282]" in str(e)


def test_invalid_email():
    try:
        _ = Creator(email="bad")
        assert False, "Should have thrown error"
    except ValueError as e:
        assert "value is not a valid email address" in str(e)


def test_creator_readonly():
    creator = Creator(hydroshare_user_id=5)
    try:
        creator.hydroshare_user_id = 6
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'hydroshare_user_id' in str(e)
        assert 'Field is frozen' in str(e)


def test_contributor_readonly():
    contributor = Contributor(hydroshare_user_id=5)
    try:
        contributor.hydroshare_user_id = 6
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'hydroshare_user_id' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_created_readonly(res_md):
    try:
        res_md.created = datetime.now()
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'created' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_modified_readonly(res_md):
    try:
        res_md.modified = datetime.now()
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'modified' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_review_readonly(res_md):
    try:
        res_md.review_started = datetime.now()
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'review_started' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_published_readonly(res_md):
    try:
        res_md.published = datetime.now()
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'published' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_type_readonly(res_md):
    try:
        res_md.type = "http://www.hydroshare.org/"
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'type' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_identifier_readonly(res_md):
    try:
        res_md.identifier = "identifier"
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'identifier' in str(e)
        assert 'Field is frozen' in str(e)


metadata_files = [
    'geographicraster_meta.xml',
    'fileset_meta.xml',
    'referencedtimeseries.refts_meta.xml',
    'multidimensional_meta.xml',
    'singlefile_meta.xml',
    'geographicfeature_meta.xml',
    'timeseries_meta.xml',
]


@pytest.mark.parametrize("metadata_file", metadata_files)
def test_aggregation_url_readonly(change_test_dir, metadata_file):
    with open(f"data/metadata/{metadata_file}", 'r') as f:
        md = load_rdf(f.read())
    try:
        md.url = "changed"
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'url' in str(e)
        assert 'Field is frozen' in str(e)


@pytest.mark.parametrize("metadata_file", metadata_files)
def test_aggregation_type_readonly(change_test_dir, metadata_file):
    with open(f"data/metadata/{metadata_file}", 'r') as f:
        md = load_rdf(f.read())
    try:
        md.type = AggregationType.TimeSeriesAggregation
        assert False, "Should have thrown error"
    except ValidationError as e:
        assert 'type' in str(e)
        assert 'Field is frozen' in str(e)


def test_resource_metadata_from_form():
    """Tests excluded, non-required fields that have validators (split_dates, split_coverages)"""
    md = {
        "type": "CompositeResource",
        "url": "http://www.hydroshare.org/resource/5885512838ab4faabbbdafcea0f9dbd1",
        "identifier": "http://www.hydroshare.org/resource/5885512838ab4faabbbdafcea0f9dbd1",
        "title": "asdf",
        "language": "eng",
        "subjects": ["asdf"],
        "creators": [
            {
                "name": "Black, Scott Steven",
                "organization": "USU",
                "email": "scott.black@usu.edu",
                "hydroshare_user_id": 2351,
            }
        ],
        "contributors": [],
        "sources": [],
        "relations": [],
        "spatial_coverage": {"east": 90, "north": 89, "units": "test units", "projection": "test projections"},
        "rights": {
            "statement": "This resource is shared under the Creative Commons Attribution CC BY.",
            "url": "http://creativecommons.org/licenses/by/4.0/",
        },
        "created": "2021-04-01T17:38:03.968981+00:00",
        "modified": "2021-04-01T17:38:24.993846+00:00",
        "awards": [],
        "citation": "Black, S. S. (2021). asdf, HydroShare, http://www.hydroshare.org/resource/5885512838ab4faabbbdafcea0f9dbd1",
    }
    res = ResourceMetadata(**md)
    assert res.title == "asdf"
    assert res.spatial_coverage.type == "point"


def test_aggregation_metadata_from_form():
    """Tests excluded, non-required fields that have validators (split_dates, split_coverages)"""
    md = {
        "url": "http://www.hydroshare.org/resource/1248abc1afc6454199e65c8f642b99a0/data/contents/logan_resmap.xml#aggregation",
        "title": "asdf",
        "subjects": ["Small", "Logan", "VRT"],
        "language": "eng",
        "additional_metadata": [{"key": "key1", "value": "value1"}, {"key": "another key", "value": "another value"}],
        "spatial_coverage": {
            "name": "12232",
            "northlimit": 30.214583003567654,
            "eastlimit": -97.92170777387547,
            "southlimit": 30.127513332692264,
            "westlimit": -98.01556648306897,
            "units": "Decimal degrees",
            "projection": "WGS 84 EPSG:4326",
        },
        "period_coverage": None,
        "rights": {
            "statement": "This resource is shared under the Creative Commons Attribution CC BY.",
            "url": "http://creativecommons.org/licenses/by/4.0/",
        },
        "type": "GeoRaster",
        "band_information": {
            "name": "Band_1",
            "variable_name": None,
            "variable_unit": None,
            "no_data_value": "-3.40282346639e+38",
            "maximum_value": "2880.00708008",
            "comment": None,
            "method": None,
            "minimum_value": "2274.95898438",
        },
        "spatial_reference": {
            "northlimit": 30.214583003567654,
            "eastlimit": -97.92170777387547,
            "southlimit": 30.127513332692264,
            "westlimit": -98.01556648306897,
            "units": "Decimal degrees",
            "projection": "WGS 84 EPSG:4326",
            "projection_string": "WGS 84 EPSG:4326",
        },
        "cell_information": {
            "name": "logan.vrt",
            "rows": 230,
            "columns": 220,
            "cell_size_x_value": 30,
            "cell_data_type": "Float32",
            "cell_size_y_value": 30,
        },
    }
    # TODO: In the above data, commented all fields set to None in order for the validation to pass for
    #  GeographicRasterMetadata. If we want the fields with None value to be passed as input,
    #  then the schema needs to be updated using Optional[]. Example: "period_coverage": Optional[PeriodCoverage]
    #  Then if we do this schema change for GeographicRasterMetadata, we need to do the same for all other schemas where
    #  the field default value is None.
    agg = GeographicRasterMetadata(**md)
    assert agg.spatial_reference.type == "box"
    assert agg.spatial_coverage.type == "box"
    assert agg.additional_metadata["key1"] == "value1"
    assert agg.additional_metadata["another key"] == "another value"


def test_subjects_resource(res_md):
    res_md.subjects = ["", "a ", "a", " a"]
    assert res_md.subjects == ["a"]


def test_subjects_aggregation(agg_md):
    agg_md.subjects = ["", "a ", "a ", "a"]
    assert agg_md.subjects == ["a"]


def test_default_exclude_none(res_md):
    res_md.spatial_coverage = None
    assert "spatial_coverage" not in res_md.model_dump()
    assert "spatial_coverage" in res_md.model_dump(exclude_none=False)
