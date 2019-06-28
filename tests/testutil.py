import unittest

from phlights.util import build_flight_search_requests

class UtilTest(unittest.TestCase):
    def test_query_builder_empty(self):
        self.assertTrue(build_flight_search_requests(""))