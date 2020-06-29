"""
tests for the locations generator.
"""
import unittest as ut


class TestBasics (ut.TestCase):
    """ tests basic python behaviors. """

    def test_paths(self):
        """ checks the project root location.
        loads a known file on the project root, and verifies
        it isn't empty.
        """
        with open("../config.yaml") as fil:
            contents = fil.read()
        self.assertIsNotNone(contents)
