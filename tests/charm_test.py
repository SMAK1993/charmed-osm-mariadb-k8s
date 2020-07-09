import unittest
from unittest.mock import (
    call,
    patch,
)
import sys
from uuid import uuid4

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

    @patch('charm.MariaDbCharm.makePodSpec', autospec=True, spec_set=True)
    def test__on_start__sets_the_podspec_correctly(self, mock_make_pod_spec_func):
        # Setup
        harness = self.harness
        harness.set_leader()
        harness.begin()

        mock_make_pod_spec_func.return_value = str(uuid4())

        # Exercise
        with patch.object(harness.charm.model.pod, 'set_spec',
                          autospec=True, spec_set=True) as mock_set_spec_func:
            harness.charm.on.start.emit()

            # Assess
            assert mock_set_spec_func.call_count == 1
            assert mock_set_spec_func.call_args == \
                call(mock_make_pod_spec_func.return_value)
