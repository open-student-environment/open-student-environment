import unittest
from .environment import Environment
from ose.agent.student import PoissonStudent
from pymc import Uniform, MCMC

from ose.agent import Agent


class Test(unittest.TestCase):

    def setUp(self):
        self.students = [PoissonStudent(name='Ed', lam=2)]
        self.statements = [
            {'timestamp': 0.7354156191538802, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 0.8781497209426028, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.144202469575485, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.427249032536914, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.5319657470218193, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'John', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'John', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied', \
             'actor': 'Kevin', 'object': 'resource'}
        ]

    def tearDown(self):
        pass

    def test_simulate(self):
        env = Environment(self.students)
        statements = env.simulate(10)
        self.assertGreaterEqual(statements[-1]["timestamp"], 8,
                                msg="The environment generated an unexpected"
                                    "low amount of data for a student")

    def test_environment(self):
        env = Environment(self.students, self.statements)
        self.assertEqual(len(env._statements.keys()),
                         3,
                         msg="The environment created a different"
                             " number of student than there is in"
                             " the statements")

    def test_add_student(self):
        env = Environment(self.students, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_student(student)
        self.assertEqual(len(env.students.keys()), 2,
                         msg="Adding a student didn't change the number of" +
                             "student in the environment")

    def test_statements_added_to_student(self):
        env = Environment(self.students, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_student(student)
        self.assertEqual(len(env.students[student.name].dt),
                         len(env._statements[
                                 student.name]),
                         msg="The student statements and dt have different "
                             "sizes")

    def test_fit(self):
        statement = {'actor': u'123456789-1234-1234-1234-12345678901234',
         'verb': u'http://adlnet.gov/expapi/verbs/completed',
         'timestamp': 1519862425.0}
        user_name = '123456789-1234-1234-1234-12345678901234'
        lam = Uniform('lam', lower=0, upper=1)
        s1 = PoissonStudent(user_name, lam=lam)
        env = Environment([s1], [statement])
        env.add_student(s1)
        res = env.fit([lam], method='mcmc')
        self.assertIsInstance(res, MCMC,
                              msg="The output of fit is not an PYMC instance")

    def test_initialization(self):
        names = ['a', 'b', 'c', 'd']
        g = [
            {'id': 1, 'label': 'level 2', 'type': 'level'},
            {'id': 2, 'label': 'CM2', 'type': 'class'},
            {'id': 3, 'label': 'Jules Ferry', 'type': 'school'}
        ]
        agents = [Agent(name, groups=[g[i % 3]]) for i, name in enumerate(names)]
        env = Environment(agents)
        self.assertEqual(env.groups, {group['id']: group for group in g})

    def test_get_structure(self):
        g = [
            {'id': 1, 'label': 'level 2', 'type': 'level'},
            {'id': 2, 'label': 'CM2', 'type': 'class'},
            {'id': 3, 'label': 'CM1', 'type': 'class'},
            {'id': 4, 'label': 'Jules Ferry', 'type': 'school'},
            {'id': 5, 'label': 'Jean Jaures', 'type': 'school'}
        ]
        t1 = Agent(name='teacher 1', groups=[g[3], g[1], g[2]])
        t2 = Agent(name='teacher 2', groups=[g[0], g[4]])
        s1 = Agent(name='student 1', groups=[g[1]])
        s2 = Agent(name='student 2', groups=[g[1]])
        s3 = Agent(name='student 3', groups=[g[1]])
        s4 = Agent(name='student 4', groups=[g[2]])
        s5 = Agent(name='student 5', groups=[g[2]])
        s6 = Agent(name='student 6', groups=[g[0]])

        agents = [t1, t2, s1, s2, s3, s4, s5, s6]
        env = Environment(agents)
        structure = env._get_structure(self.students)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPoissonStudent']
    unittest.main()
