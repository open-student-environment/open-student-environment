import unittest

from .student import PoissonStudent


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPoissonStudent(self):
        student = PoissonStudent(name='Ed', lam=1)
        statement = student.study()
        self.assertIsInstance(statement['timestamp'], float)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPoissonStudent']
    unittest.main()
