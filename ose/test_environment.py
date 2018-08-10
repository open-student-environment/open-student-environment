import os
import unittest

from pymc import Uniform, MCMC

from ose.environment import Environment, get_active_agents, filter_by_users
from ose.agent import Agent, PoissonStudent, Role
from ose.agent import load_agents
from ose.statement import load_statements


class Test(unittest.TestCase):

    def setUp(self):
        self.agents = [PoissonStudent(name='Ed', role=Role.STUDENT, lam=2)]
        self.statements = [
            {'timestamp': 0.7354156191538802, 'verb': 'studied',
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 0.8781497209426028, 'verb': 'studied',
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.144202469575485, 'verb': 'studied',
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.427249032536914, 'verb': 'studied',
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.5319657470218193, 'verb': 'studied',
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied',
             'actor': 'Ed', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied',
             'actor': 'John', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied',
             'actor': 'John', 'object': 'resource'},
            {'timestamp': 1.9421492844170225, 'verb': 'studied',
             'actor': 'Kevin', 'object': 'resource'}
        ]
        self.base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir))

    def tearDown(self):
        pass

    def test_simulate(self):
        env = Environment(self.agents)
        statements = env.simulate(10)
        self.assertGreaterEqual(statements[-1]["timestamp"], 8,
                                msg="The environment generated an unexpected"
                                    "low amount of data for a agent")

    def test_environment(self):
        env = Environment(self.agents, self.statements)
        self.assertEqual(len(env._statements.keys()),
                         3,
                         msg="The environment created a different"
                             " number of agent than there is in"
                             " the statements")

    def test_add_agent(self):
        env = Environment(self.agents, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_agent(student)
        self.assertEqual(len(env.agents), 2,
                         msg="Adding an agent didn't change the number of" +
                             "agent in the environment")

    def test_statements_added_to_agent(self):
        env = Environment(self.agents, self.statements)
        student = PoissonStudent(name='John', lam=2)
        env.add_agent(student)
        self.assertEqual(len(env._agents[student.name].dt),
                         len(env._statements[
                                 student.name]),
                         msg="The agent statements and dt have different "
                             "sizes")

    def test_fit(self):
        statement = {
            'actor': u'123456789-1234-1234-1234-12345678901234',
            'verb': u'http://adlnet.gov/expapi/verbs/completed',
            'timestamp': 1519862425.0
        }
        user_name = '123456789-1234-1234-1234-12345678901234'
        lam = Uniform('lam', lower=0, upper=1)
        s1 = PoissonStudent(user_name, lam=lam)
        env = Environment([s1], [statement])
        env.add_agent(s1)
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
        t1 = Agent(name='t1', role=Role.TEACHER, groups=[g[3], g[1], g[2]])
        t2 = Agent(name='t2', role=Role.TEACHER, groups=[g[0], g[4]])
        s1 = Agent(name='s1', role=Role.STUDENT, groups=[g[1]])
        s2 = Agent(name='s2', role=Role.STUDENT, groups=[g[1]])
        s3 = Agent(name='s3', role=Role.STUDENT, groups=[g[1]])
        s4 = Agent(name='s4', role=Role.STUDENT, groups=[g[2]])
        s5 = Agent(name='s5', role=Role.STUDENT, groups=[g[2]])
        s6 = Agent(name='s6', role=Role.STUDENT, groups=[g[0]])

        agents = [t1, t2, s1, s2, s3, s4, s5, s6]
        env = Environment(agents)
        _, adjancy = env._get_structure(agents)
        expected_adjancy = {
            't1': {2, 3, 4},
            't2': {1, 5},
            2: {'s1', 's2', 's3'},
            3: {'s5', 's4'},
            1: {'s6'}
        }
        self.assertEqual(adjancy, expected_adjancy)

    def test_build_graph_from_data(self):
        agents = load_agents(self.base_path + '/data/test/agents_sample.json')
        env = Environment(agents)
        nodes, adjancy = env.nodes, env.structure
        tnodes = {
            'a', 1, 2, 3, 5480, 17177, 19272, 30207, 30367, 'b', 'c', 'd', 'e',
            102, '0951099D', 'f', 116, '0060138T', 'g', 123, 'h', 'i', 130
        }
        self.assertEqual(set(nodes.keys()), tnodes)
        self.assertEqual(set(nodes.keys()).union(set(adjancy.keys())),
                         set(nodes.keys()))

    def test_filter_by_users(self):
        statements = load_statements(
            self.base_path + '/data/test/statements_sample.json')
        agents = load_agents(self.base_path + '/data/test/agents_sample.json')
        env = Environment(agents, statements)
        nodes, adjancy = env.nodes, env.structure
        active_agents = get_active_agents(statements)
        nodes, adjancy = filter_by_users(nodes, adjancy, active_agents)
        # TODO: Check for real

    def test_get_students(self):
        agents = load_agents(self.base_path + '/data/test/agents_sample.json')
        env = Environment(agents)
        students = env._get_students('a', keep_inactive=True)
        self.assertEqual(students, {'b', 'c', 'h', 'd'})

    def test_to_gdf(self):
        agents = load_agents(self.base_path + '/data/test/agents_sample.json')
        env = Environment(agents)
        env.to_gdf(filename=self.base_path + '/data/test-output.csv')
        os.remove(self.base_path + '/data/test-output.csv')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testPoissonStudent']
    unittest.main()
