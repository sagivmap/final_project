import unittest
from AlgorithmSolver.AlgorithmSolver import AlgorithmSolver
from AlgorithmSolver.Edge import Edge
from AlgorithmSolver.Node import Node


class TestDecodeNonEnglishStrings(unittest.TestCase):
    algSolver = AlgorithmSolver('path_to_nowhere')

    def test_hebrew_name_decoding0(self):
        name_to_decode = '\\xe2\\x80\\x8e\\xd7\\x99\\xd7\\x95\\xd7\\xa1\\xd7\\xa3 \\xd7\\x90\\xd7\\x91\\xd7\\x95' \
                         '\\xd7\\x97\\xd7\\xa6\\xd7\\x99\\xd7\\xa8\\xd7\\x94\\xe2\\x80\\x8e'

        encoded_name = self.algSolver._decode_name(name_to_decode)[1:-1]
        expected = "יוסף אבוחצירה"
        self.assertEqual(expected, encoded_name)

    def test_hebrew_name_decoding1(self):
        name_to_decode = '\\xe2\\x80\\x8e\\xd7\\x97\\xd7\\x99\\xd7\\xa9 ' \
                         '\\xd7\\x97\\xd7\\x99\\xd7\\xa9\\xe2\\x80\\x8e'

        encoded_name = self.algSolver._decode_name(name_to_decode)[1:-1]
        expected = "חיש חיש"
        self.assertEqual(expected, encoded_name)

class TestCreationOfGraph(unittest.TestCase):
    algSolver = AlgorithmSolver('test1.csv')
    currUser = Node('Ego_Node', 'SOURCE', '0', '0', '0', '0', [])

    def test_creation_of_nodes(self):
        self.algSolver.create_nodes_and_edges()
        nodes_created = self.algSolver.get_nodes()
        self.assertEqual(True, 'bob' in nodes_created.keys())
        bob_node = nodes_created['bob']
        self.assertEqual('3650', bob_node.aua)
        self.assertEqual('24', bob_node.fd)
        self.assertEqual('bob', bob_node.idd)
        self.assertEqual('bob', bob_node.name)
        self.assertEqual('30', bob_node.mf)
        self.assertEqual('900', bob_node.tf)
        self.assertEqual(['0'], bob_node.cf)

        self.assertEqual(True, 'charlie' in nodes_created.keys())
        charlie_node = nodes_created['charlie']
        self.assertEqual('300', charlie_node.aua)
        self.assertEqual('10', charlie_node.fd)
        self.assertEqual('charlie', charlie_node.idd)
        self.assertEqual('charlie', charlie_node.name)
        self.assertEqual('20', charlie_node.mf)
        self.assertEqual('90', charlie_node.tf)
        self.assertEqual(['0'], charlie_node.cf)

        self.assertEqual(True, 'david' in nodes_created.keys())
        david_node = nodes_created['david']
        self.assertEqual('250', david_node.aua)
        self.assertEqual('6', david_node.fd)
        self.assertEqual('david', david_node.idd)
        self.assertEqual('david', david_node.name)
        self.assertEqual('19', david_node.mf)
        self.assertEqual('95', david_node.tf)
        self.assertEqual(['0'], david_node.cf)

        self.assertEqual(True, 'eve' in nodes_created.keys())
        eve_node = nodes_created['eve']
        self.assertEqual('10', eve_node.aua)
        self.assertEqual('-1', eve_node.fd)
        self.assertEqual('eve', eve_node.idd)
        self.assertEqual('eve', eve_node.name)
        self.assertEqual('3', eve_node.mf)
        self.assertEqual('50', eve_node.tf)
        self.assertTrue('bob' in  eve_node.cf)
        self.assertTrue('charlie' in eve_node.cf)
        self.assertTrue('david' in eve_node.cf)

        self.assertEqual(True, 'frank' in nodes_created.keys())
        frank_node = nodes_created['frank']
        self.assertEqual('400', frank_node.aua)
        self.assertEqual('-1', frank_node.fd)
        self.assertEqual('frank', frank_node.idd)
        self.assertEqual('frank', frank_node.name)
        self.assertEqual('2', frank_node.mf)
        self.assertEqual('120', frank_node.tf)
        self.assertTrue('david' in frank_node.cf)
        self.assertTrue('charlie' in frank_node.cf)

    def test_creation_of_edges(self):
        self.algSolver.create_nodes_and_edges()
        nodes_created = self.algSolver.get_nodes()
        edge_expected0 = Edge(nodes_created['david'],nodes_created['eve'], '-1')
        edge_expected1 = Edge(nodes_created['david'],nodes_created['frank'], '-1')
        edge_expected2 = Edge(nodes_created['bob'],nodes_created['eve'], '-1')
        edge_expected3 = Edge(self.currUser,nodes_created['bob'], '24')
        edge_expected4 = Edge(self.currUser,nodes_created['charlie'], '10')
        edge_expected5 = Edge(nodes_created['charlie'],nodes_created['eve'], '-1')
        edge_expected6 = Edge(nodes_created['charlie'],nodes_created['frank'], '-1')
        edge_expected7 = Edge(self.currUser,nodes_created['david'], '6')
        edges_created = self.algSolver.get_edges()
        self.assertTrue(edge_expected0 in edges_created)
        self.assertTrue(edge_expected1 in edges_created)
        self.assertTrue(edge_expected2 in edges_created)
        self.assertTrue(edge_expected3 in edges_created)
        self.assertTrue(edge_expected4 in edges_created)
        self.assertTrue(edge_expected5 in edges_created)
        self.assertTrue(edge_expected6 in edges_created)
        self.assertTrue(edge_expected7 in edges_created)

class TestWeightCalculation(unittest.TestCase):
    algSolver = AlgorithmSolver('test1.csv')

    def test_nodes_weights(self):
        self.algSolver.create_nodes_and_edges()
        self.algSolver.calculate_weights()
        created_nodes = self.algSolver.get_nodes()
        self.assertAlmostEqual(created_nodes['charlie'].weight, 0.90730593, 7)
        self.assertEqual(created_nodes['bob'].weight, 1)
        self.assertAlmostEqual(created_nodes['david'].weight, 0.86164383, 7)
        self.assertAlmostEqual(created_nodes['eve'].weight, 0.22579908, 7)
        self.assertAlmostEqual(created_nodes['frank'].weight, 0.7, 7)

    def test_edges_weights(self):
        self.algSolver.create_nodes_and_edges()
        self.algSolver.calculate_weights()
        created_edges = self.algSolver.get_edges()
        edge_ego_to_bob = [x for x in created_edges if (x.src.idd == 'Ego_Node' and x.dest.idd == 'bob')][0]
        self.assertEqual(edge_ego_to_bob.weight, 1)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'Ego_Node' and x.dest.idd == 'charlie')][0]
        self.assertAlmostEqual(edge_ego_to_charlie.weight, 0.83333333, 7)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'Ego_Node' and x.dest.idd == 'david')][0]
        self.assertEqual(edge_ego_to_charlie.weight, 0.5)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'bob' and x.dest.idd == 'eve')][0]
        self.assertEqual(edge_ego_to_charlie.weight, 1)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'charlie' and x.dest.idd == 'eve')][0]
        self.assertEqual(edge_ego_to_charlie.weight, 1)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'charlie' and x.dest.idd == 'frank')][0]
        self.assertEqual(edge_ego_to_charlie.weight, 1)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'david' and x.dest.idd == 'eve')][0]
        self.assertEqual(edge_ego_to_charlie.weight, 1)
        edge_ego_to_charlie = [x for x in created_edges if (x.src.idd == 'david' and x.dest.idd == 'frank')][0]
        self.assertEqual(edge_ego_to_charlie.weight, 1)

class TestTSPCalculation(unittest.TestCase):
    algSolver = AlgorithmSolver('test1.csv')

    def test_calculate_TSP(self):
        self.algSolver.create_nodes_and_edges()
        self.algSolver.calculate_weights()
        self.algSolver.calculate_TSP()

        second_circle_nodes = self.algSolver.get_second_circle_nodes()
        node_of_eve = [x for x in second_circle_nodes if (x.idd == 'eve')][0]
        node_of_frank = [x for x in second_circle_nodes if (x.idd == 'frank')][0]

        self.assertAlmostEqual(node_of_eve.tsp, 0.22579908, 7)
        self.assertAlmostEqual(node_of_frank.tsp, 0.52926179, 7)


if __name__ == '__main__':
    test_classes_to_run = [TestDecodeNonEnglishStrings,
                           TestWeightCalculation,
                           TestTSPCalculation]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)