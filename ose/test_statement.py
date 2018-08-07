import unittest
from .environment import Environment
from .student import PoissonStudent
from .statement import load_statements, load_file, \
    extract_information_educlever


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_extract_time(self):
        pass

    def test_load_statements(self):
        filename = 'data/test/statements_sample.json'
        statements = load_file(filename)
        usable_statement = load_statements(statements)
        self.assertEqual(len(statements), len(usable_statement),
                         msg="The loaded statements aren't the same length "
                             "as the unloaded one")

    def test_extract_information_educlever(self):
        filename = 'data/test/unique_example_educlever.json'
        statement = load_file(filename)
        res = extract_information_educlever(statement[0])
        gt = {'actor': u'123456789-1234-1234-1234-12345678901234',
              'verb': u'http://adlnet.gov/expapi/verbs/completed',
              'timestamp': 1519862425.0}
        self.assertDictEqual(res, gt,
                             msg="The statement loaded and the result "
                                 "extracted are not the same")

if __name__ == "__main__":
    unittest.main()
