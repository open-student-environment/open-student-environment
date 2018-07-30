import unittest

import numpy as np

from .student import PoissonStudent, WrongAssignment

statements = [
    {'actor': 'Dave', 'verb': 'do', 'object': 'thing', 'timestamp': 1},
    {'actor': 'Dave', 'verb': 'do', 'object': 'thing', 'timestamp': 4},
    {'actor': 'Dave', 'verb': 'do', 'object': 'thing', 'timestamp': 2},
    {'actor': 'Dave', 'verb': 'do', 'object': 'thing', 'timestamp': 3}
]


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_poisson_study(self):
        student = PoissonStudent(name='Ed', lam=1)
        statement = student.study()
        self.assertIsInstance(statement['timestamp'], float)

    def test_poisson_get_timestamps(self):
        student = PoissonStudent(name='Dave', lam=1)
        timestamps = student._get_timestamps(statements)
        self.assertEqual(timestamps, [1, 2, 3, 4])

    def test_poisson_update(self):
        student = PoissonStudent(name='Dave', lam=1)
        student.update(statements)
        eq = np.array_equal(student.expT.value, [1, 1, 1, 1])
        self.assertTrue(eq)

    def test_wrong_assignement(self):
        student = PoissonStudent(name='Ed', lam=1)
        with self.assertRaises(WrongAssignment):
            student.update(statements)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPoissonStudent']
    unittest.main()
