import unittest
import os

from ose.agent import Agent, load_agents


class Test(unittest.TestCase):

    def setUp(self):
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        self.filename = os.path.join(
            base_path, '../../data/test/agents_sample.json')

    def tearDown(self):
        pass

    def test_agent(self):
        agent = Agent(
            name='Fabio',
            role='supervisor',
            groups=[{'id': 0, 'label': 'MEN', 'type': None}])

        self.assertEqual(agent.__repr__(), "Fabio (supervisor)")

    def test_load_agent(self):
        agents = load_agents(self.filename)
        self.assertEqual(len(agents), 9)
        groups = [
            {'id': 1, 'label': 'Ecole du chemin', 'type': 'ecole'},
            {'id': 3, 'label': 'Enseignant Duchmol', 'type': 'classe'},
            {'id': 5480, 'label': 'L3-Anglais', 'type': 'groupe'}
        ]
        self.assertEqual(agents[1].groups, groups)


if __name__ == "__main__":
    unittest.main()
