import os

import unittest

from .utils import load_agent_data, get_agents_graph, graph2gephi


agents = """{"uuid":"a","uai":null,"role":"user:enseignant","isEphemeral":0,"schoolLevels":[],"organizations":[{"id":1,"label":"Ecole du chemin","type":"ecole"},{"id":2,"label":"Classe de CP","type":"classe"},{"id":3,"label":"Enseignant Duchmol","type":"classe"},{"id":5480,"label":"L3-Anglais","type":"groupe"},{"id":17177,"label":"Groupe 2","type":"groupe"},{"id":19272,"label":"Les CM1","type":"groupe"},{"id":30207,"label":"Groupe VERT","type":"groupe"},{"id":30367,"label":"GROUPE B","type":"groupe"}],"isolution":"brneac3"}
{"uuid":"b","uai":null,"role":"user:eleve","isEphemeral":0,"schoolLevels":["niveau1"],"organizations":[{"id":1,"label":"Ecole du chemin","type":"ecole"},{"id":3,"label":"Enseignant Duchmol","type":"classe"},{"id":5480,"label":"L3-Anglais","type":"groupe"}],"isolution":"brneac3"}
{"uuid":"c","uai":null,"role":"user:eleve","isEphemeral":0,"schoolLevels":["niveau2"],"organizations":[{"id":2,"label":"Classe de CP","type":"classe"},{"id":3,"label":"Enseignant Duchmol","type":"classe"},{"id":5480,"label":"L3-Anglais","type":"groupe"}],"isolution":"brneac3"}
{"uuid":"d","uai":null,"role":"user:eleve","isEphemeral":0,"schoolLevels":[],"organizations":[{"id":1,"label":"Ecole du chemin","type":"ecole"},{"id":3,"label":"Enseignant Duchmol","type":"classe"},{"id":5480,"label":"L3-Anglais","type":"groupe"}],"isolution":"brneac3"}
{"uuid":"e","uai":"0951099D","role":"user:enseignant","isEphemeral":0,"schoolLevels":[],"organizations":[{"id":102,"label":"Enseignant Boissonnat","type":"classe"}],"isolution":"brneac3"}
{"uuid":"f","uai":"0060138T","role":"user:enseignant","isEphemeral":0,"schoolLevels":[],"organizations":[{"id":116,"label":"Enseignant SICRE","type":"classe"}],"isolution":"brneac3"}
{"uuid":"g","uai":"0060138T","role":"user:enseignant","isEphemeral":0,"schoolLevels":[],"organizations":[{"id":123,"label":"Enseignant SICRE","type":"classe"}],"isolution":"brneac3"}
{"uuid":"h","uai":null,"role":"user:eleve","isEphemeral":0,"schoolLevels":["niveau3"],"organizations":[{"id":3,"label":"Enseignant Duchmol","type":"classe"},{"id":5480,"label":"L3-Anglais","type":"groupe"}],"isolution":"brneac3"}
{"uuid":"i","uai":"0060138T","role":"user:enseignant","isEphemeral":0,"schoolLevels":[],"organizations":[{"id":130,"label":"Enseignant SICRE","type":"classe"}],"isolution":"brneac3"}"""


class Test(unittest.TestCase):

    def setUp(self):
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        path = os.path.join(base_path, 'data')
        if not os.path.exists(path):
            os.makedirs(path)
        filename = os.path.join(path, 'test.json')
        self.filename = filename
        with open(filename, 'w') as f:
            f.write(agents)

    def tearDown(self):
        pass

    def test_load_agent_data(self):
        data = load_agent_data(self.filename)
        self.assertEqual(len(data), 9)

    def test_build_graph_from_data(self):
        data = load_agent_data(self.filename)
        nodes, adjancy = get_agents_graph(data)
        agents = {
            'a', 'b', 1, 3, 5480, 'c', 2, 'd', 'e', '0951099D', 'f',
            '0060138T', 'g', 'h', 'i'
        }
        self.assertEqual(nodes.keys(), agents)
        self.assertEqual(set(nodes.keys()).difference(set(adjancy.keys())),
                         {'d', 'b', 'c', 'h'})

    def test_graph2gephi(self):
        data = load_agent_data(self.filename)
        nodes, adjancy = get_agents_graph(data)
        graph2gephi(nodes, adjancy, filename='./test-output.csv')
        os.remove('./test-output.csv')

if __name__ == "__main__":
    unittest.main()
