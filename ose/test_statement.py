import os
import unittest

from .statement import load_statements


class Test(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        self.filename = os.path.join(path, 'data/test/statements_sample.json')

    def tearDown(self):
        pass

    def test_extract_time(self):
        pass

    def test_load_statements(self):
        statements = load_statements(self.filename)
        self.assertEqual(len(statements), len(statements),
                         msg="The loaded statements aren't the same length "
                             "as the unloaded one")

    def test_extract_information(self):
        res = load_statements(self.filename)[0]
        gt = {'actor': u'12312312-1234-1234-1234-1234560778901',
              'verb': u'http://adlnet.gov/expapi/verbs/completed',
              'timestamp': 1519862425.0}
        self.assertDictEqual(res, gt,
                             msg="The statement loaded and the result "
                                 "extracted are not the same")

if __name__ == "__main__":
    unittest.main()
