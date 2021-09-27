import random
import src.distanceAPI as dst
from math import sqrt
from pytest import approx  # type: ignore
from random import random as rnd

random.seed(12345)


class TestPythDist():
    """ Tests the properties of the pythagorean distance matrix
    generator. """

    LOCATIONS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]

    def test_size(self):
        """ Tests the matrix has the appropiate dimensions. """

        mtr = dst.pyth_dist(self.LOCATIONS)
        assert len(mtr) == 6
        for row in mtr:
            assert len(row) == 6

    def test_values(self):
        """ Tests the matrix has the right values. """

        expected = [[
            0, sqrt(2), 2*sqrt(2), 3*sqrt(2), 4*sqrt(2), 5*sqrt(2)
        ], [
            sqrt(2), 0, sqrt(2), 2*sqrt(2), 3*sqrt(2), 4*sqrt(2)
        ], [
            2*sqrt(2), sqrt(2), 0, sqrt(2), 2*sqrt(2), 3*sqrt(2)
        ], [
            3*sqrt(2), 2*sqrt(2), sqrt(2), 0, sqrt(2), 2*sqrt(2)
        ], [
            4*sqrt(2), 3*sqrt(2), 2*sqrt(2), sqrt(2), 0, sqrt(2)
        ], [
            5*sqrt(2), 4*sqrt(2), 3*sqrt(2), 2*sqrt(2), sqrt(2), 0
        ]]

        mtr = dst.pyth_dist(self.LOCATIONS)
        for i, x in enumerate(mtr):
            for j, y in enumerate(x):
                assert y == approx(expected[i][j])


class TestDistMatr():
    """ Test the properties of the generated matrix from Google Maps API."""

    SPEED = 5

    COORDINATES = [
        (10, 20),
        (15, 10),
        (17, 9),
        (6, 20),
        (15, 16),
        (0, 10),
        (10, 10),
        (17, 19),
        (1, 2),
        (3, 4),
        (5, 6),
        (7, 8)
        ]

    def random(self):
        return (rnd() * 20, rnd() * 20)

    def API_CALL(self, orig, dest):
        if len(orig) > 10:
            raise ValueError("Too many origins")
        elif len(dest) > 10:
            raise ValueError("Too many destinations")

        # for this test's purposes, we'll mock the Google maps API
        # with the Pythagorean function and a fixed speed constant.
        # non-numeric addresses will be spoofed with a random location.
        result = []
        for x in orig:
            row = {"elements": []}
            x_ = x
            if type(x) == str:
                x_ = self.random()
            for y in dest:
                y_ = y
                if type(y) == str:
                    y_ = self.random()
                calc = sqrt((x_[0] - y_[0])**2 + (x_[1] - y_[1])**2)
                row["elements"].append({
                    "distance": {"value": calc},
                    "duration": {"value": calc/self.SPEED}
                })
            result.append(row)
        return {
            "destination_addresses": [],
            "origin_addresses": [],
            "rows": result
        }

    def test_size(self, mocker):
        """ test the returned result has the right shape. """
        mocker.patch("src.distanceAPI.gmaps.distance_matrix", self.API_CALL)

        result = dst.dist_matr(self.COORDINATES)

        assert len(result) == 2
        assert len(result[0]) == 12
        assert len(result[1]) == 12
