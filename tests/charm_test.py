import unittest
import sys

sys.path.append('lib')

from ops.testing import (
    Harness,
)

sys.path.append('src')

from charm import MariaDbCharm


class CharmTest(unittest.TestCase):

    def setUp(self):
        # Setup
        self.harness = Harness(MariaDbCharm)

    def test__init__runs_succesfully(self):
        # Setup
        harness = self.harness

        # Exercise
        harness.begin()
