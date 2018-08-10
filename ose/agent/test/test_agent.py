import unittest

from ose.agent import Agent, load_agents


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
        pass

    def tearDown(self):
        pass

    def test_agent(self):
        agent = Agent(
            name='Fabio',
            role='supervisor',
            groups=[{'id': 0, 'label': 'MEN', 'type': None}])

        self.assertEqual(agent.__repr__(), "Fabio (supervisor)")

    def test_load_agent(self):
        data = load_agents(self.filename)
        self.assertEqual(len(data), 9)


if __name__ == "__main__":
    unittest.main()
