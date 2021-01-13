import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class TestAlgoGraph(unittest.TestCase):

    def test_SaveLoadGraph(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(2)
        g.add_node(3)
        g.add_edge(0, 2, 5);
        g.add_edge(0, 3, 8);
        g.add_edge(2, 3, 9);
        ga = GraphAlgo(g)
        ga.save_to_json("../data/graph.json")
        ga2 = GraphAlgo()
        ga2.load_from_json("../data/graph.json")
        g2 = ga2.get_graph()
        self.assertIsNotNone(g2)
        self.assertEqual(3, g2.e_size())
        g2.add_node(4)
        self.assertNotEqual(g2.v_size(), g.v_size())

    def test_shortest_path(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_edge(0, 1, 2);
        g.add_edge(1, 2, 1);
        g.add_edge(0, 3, 8);
        g.add_edge(2, 3, 3);
        ga = GraphAlgo(g)
        x = ga.shortest_path(0, 3)
        self.assertEqual((6, [0, 1, 2, 3]), x)

    def test_connected_component(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_edge(0, 1, 2);
        g.add_edge(1, 2, 1);
        g.add_edge(0, 3, 8);
        g.add_edge(2, 3, 3);
        ga = GraphAlgo(g)
        x = ga.connected_component(3)
        self.assertEqual(([3]), x)

    def test_connected_components(self):
        g = DiGraph()
        g.add_node(0)
        g.add_node(1)
        g.add_node(2)
        g.add_node(3)
        g.add_edge(0, 1, 2);
        g.add_edge(1, 2, 1);
        g.add_edge(0, 3, 8);
        g.add_edge(2, 3, 3);
        ga = GraphAlgo(g)
        x = ga.connected_components()
        self.assertEqual(4, len(x))


if __name__ == '__main__':
    unittest.main()