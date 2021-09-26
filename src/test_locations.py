"""
tests for the locations generator.
"""

import requests
import src.locations as lc
import pickle as pk
from yaml import load, SafeLoader

with open("temp/tiendas.p", 'rb') as fi:
    tiendas = pk.load(fi)

with open("config.yaml") as fil:
    conf = load(fil, Loader=SafeLoader)


# mocking request's calls.
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, website_data, status_code):
            self.website_data = website_data
            self.status_code = status_code

        def text(self):
            return self.website_data.text

    if args[0] == (
            "https://aratiendas.com/nuestras-tiendas?field_region_tid=212"):
        return MockResponse(tiendas, 200)

    return MockResponse(None, 404)


def test_paths():
    """ checks the project root location.
        loads a known file on the project root, and verifies
        it isn't empty. """
    with open("config.yaml") as fil:
        contents = fil.read()

    assert contents is not None


class TestRandomCoords():
    """ Tests the random coordinate generator. """

    def test_size(self):
        """ generates a basic, 10 x 10 coordinate list """
        gen = lc.random_coords(num=12, width=50, length=60)
        assert len(gen) == 12
        assert min(map(lambda x: x[0], gen)) >= 0
        assert min(map(lambda x: x[1], gen)) >= 0
        assert max(map(lambda x: x[0], gen)) <= 50
        assert max(map(lambda x: x[1], gen)) <= 60


class TestSiteCoords():
    """ test the Ara stores location generator. """

    def test_coords(self, requests_mock):
        """ returns a list of ara stores """
        requests_mock.get(conf["stores_url"], text=tiendas.text)
        print(requests.get(conf["stores_url"]).text[:20])
        locs = lc.site_data(
            # the test actually fails, since the people at Ara changed their
            # website. for now we'll use cached data from their old
            # webpage
            directory="assets/ubicaciones_test.html")
        coords = lc.site_coords(locs)

        assert coords == [
            (10.406111, -75.50137),
            (10.410175, -75.55059),
            (10.393466, -75.52036),
            (10.378802, -75.47196),
            (10.38157, -75.48742),
            (10.412859, -75.53714),
            (10.436197, -75.53644),
            (10.402073, -75.50408),
            (10.431944, -75.53182),
            (10.411836, -75.45515),
            (10.426077, -75.54501),
            (10.388577, -75.516431),
            (10.406412, -75.55162),
            (10.401542, -75.49448),
            (10.408142, -75.52964),
            (10.415393, -75.46069),
            (10.445973, -75.51762),
            (10.388579, -75.51861),
            (10.422417, -75.54638),
            (10.401298, -75.48388),
            (4.5728169, -74.53038),
            (10.40252, -75.51955),
            (10.405437, -75.48627),
            (10.407607, -75.51645),
            (10.413228, -75.53373),
            (10.445973, -75.51762),
            (10.402702, -75.498),
            (10.41824, -75.54169),
            (10.387233, -75.50078),
            (10.4019763, -75.4731464),
            (10.436938, -75.51609)
        ]
