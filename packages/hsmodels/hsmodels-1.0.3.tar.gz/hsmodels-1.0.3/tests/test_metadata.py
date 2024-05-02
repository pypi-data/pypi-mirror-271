import os
from datetime import datetime

import pytest
from rdflib import Graph
from rdflib.compare import _squashed_graphs_triples

from hsmodels.namespaces import RDF
from hsmodels.schemas import load_rdf, rdf_graph
from hsmodels.schemas.enums import RelationType, UserIdentifierType
from hsmodels.schemas.fields import BoxCoverage, PeriodCoverage, PointCoverage
from hsmodels.utils import to_coverage_dict


@pytest.fixture()
def res_md():
    with open("data/metadata/resourcemetadata.xml", 'r') as f:
        return load_rdf(f.read())


@pytest.fixture()
def res_md_point():
    with open("data/metadata/resourcemetadata_with_point_coverage.xml", 'r') as f:
        return load_rdf(f.read())


def compare_graphs(new_graph, original_graph):
    for new_triple, original_triple in _squashed_graphs_triples(new_graph, original_graph):
        if new_triple[1] == RDF.value:
            # for coverage and spatial reference, the value string needs to be parsed into a dictionary for comparison
            if ';' in new_triple[2]:
                assert new_triple[0] == original_triple[0]
                assert new_triple[1] == original_triple[1]
                assert to_coverage_dict(new_triple[2]) == to_coverage_dict(original_triple[2])
        else:
            assert new_triple == original_triple


def compare_metadatas(new_graph, original_metadata_file):
    original_graph = Graph()
    with open(original_metadata_file, "r") as f:
        original_graph = original_graph.parse(data=f.read())
    compare_graphs(new_graph, original_graph)


metadata_files = [
    'resourcemetadata.xml',
    'geographicraster_meta.xml',
    'fileset_meta.xml',
    'referencedtimeseries.refts_meta.xml',
    'multidimensional_meta.xml',
    'singlefile_meta.xml',
    'geographicfeature_meta.xml',
    'timeseries_meta.xml',
    'modelprogram_meta.xml',
    'modelinstance_meta.xml',
    'collection_meta.xml',
]


@pytest.mark.parametrize("metadata_file", metadata_files)
def test_resource_serialization(metadata_file):
    metadata_file = os.path.join('data', 'metadata', metadata_file)
    with open(metadata_file, 'r') as f:
        md = load_rdf(f.read())
    g = rdf_graph(md)
    compare_metadatas(g, metadata_file)


def test_resource_metadata(res_md):
    assert res_md.title == "sadfadsgasdf"

    assert len(res_md.subjects) == 14
    assert "key1" in res_md.subjects
    assert "key2" in res_md.subjects
    assert "asdf" in res_md.subjects
    assert "Snow water equivalent" in res_md.subjects

    assert res_md.abstract == "sadfasdfsadfa"

    assert res_md.language == "eng"

    assert str(res_md.identifier) == "http://www.hydroshare.org/resource/84805fd615a04d63b4eada65644a1e20"

    assert len(res_md.additional_metadata) == 3
    assert "key2" in res_md.additional_metadata
    assert res_md.additional_metadata["key2"] == "value2"

    # test additional_metadata can be optional
    res_md.additional_metadata = {}

    assert len(res_md.creators) == 3
    for cr in res_md.creators:
        assert cr.creator_order in (1, 2, 3)
    creator_orders = [cr.creator_order for cr in res_md.creators]
    assert len(creator_orders) == len(set(creator_orders))

    creator = res_md.creators[0]
    assert creator.organization == 'Utah State University'
    assert creator.email == 'jeff.horsburgh@usu.edu'
    creator = res_md.creators[1]
    assert not creator.organization
    assert not creator.email
    assert creator.name == 'Tseganeh Z. Gichamo'
    creator = res_md.creators[2]
    assert creator.organization == 'USU'
    assert creator.email == 'scott.black@usu.edu'

    try:
        res_md.creators = []
        assert False, "should have thrown exception"
    except ValueError as e:
        assert "list must contain at least one entry" in str(e)

    assert len(res_md.contributors) == 2
    contributor = next(x for x in res_md.contributors if x.email == "dtarb@usu.edu")
    assert contributor
    assert contributor.phone == "tel:4357973172"
    assert contributor.address == "Utah, US"
    assert str(contributor.homepage) == "http://hydrology.usu.edu/dtarb"
    assert contributor.organization == "Utah State University"
    assert str(contributor.identifiers[UserIdentifierType.ORCID]) == "https://orcid.org/0000-0002-1998-3479"
    assert contributor.name == "David Tarboton"

    # test contributor can be optional
    res_md.contributors = []

    assert len(res_md.relations) == 3
    assert any(x for x in res_md.relations if x.value == "https://sadf.com" and x.type == RelationType.isPartOf)
    assert any(
        x for x in res_md.relations if x.value == "https://www.google.com/" and x.type == RelationType.isCreatedBy
    )

    # test relation can be optional
    res_md.relations = []

    assert res_md.rights.statement == "my statement"
    assert str(res_md.rights.url) == "http://studio.bakajo.com/"

    assert res_md.modified == datetime.fromisoformat("2020-11-13T19:40:57.276064+00:00")
    assert res_md.created == datetime.fromisoformat("2020-07-09T19:12:21.354703+00:00")
    assert res_md.review_started == datetime.fromisoformat("2020-11-12T18:53:19.778819+00:00")
    assert res_md.published == datetime.fromisoformat("2020-11-13T18:53:19.778819+00:00")

    assert len(res_md.awards) == 2
    award = next(x for x in res_md.awards if x.title == "t")
    assert award
    assert award.number == "n"
    assert award.funding_agency_name == "agency1"
    assert str(award.funding_agency_url) == "https://google.com/"
    # test awards can be optional
    res_md.awards = []

    assert res_md.period_coverage == PeriodCoverage(
        start=datetime.fromisoformat("2020-07-10T00:00:00"), end=datetime.fromisoformat("2020-07-29T00:00:00")
    )
    # test period_coverage can be optional
    res_md.period_coverage = None

    assert res_md.spatial_coverage == BoxCoverage(
        name="asdfsadf",
        northlimit=42.1505,
        eastlimit=-84.5739,
        projection='WGS 84 EPSG:4326',
        southlimit=30.282,
        type='box',
        units='Decimal degrees',
        westlimit=-104.7887,
    )

    pc = PointCoverage(
        name='Logan, Utah',
        north=41.7371,
        east=-111.8351,
        projection='WGS 84 EPSG:4326',
        type='point',
        units='Decimal degrees',
    )

    res_md.spatial_coverage = pc
    # test spatial_coverage can be optional
    res_md.spatial_coverage = None

    assert res_md.publisher
    assert (
        res_md.publisher.name == "Consortium of Universities for the Advancement of Hydrologic Science, Inc. (CUAHSI)"
    )
    assert str(res_md.publisher.url) == "https://www.cuahsi.org/"
