import unittest
from DiGraph import DiGraph


def createGraph():
    g = DiGraph()  # creates an empty directed graph
    for n in range(7):
        g.add_node(n)
    g.add_edge(0, 1, 7)
    g.add_edge(0, 2, 4)
    g.add_edge(1, 2, 6)
    g.add_edge(1, 3, 2)
    g.add_edge(2, 6, 10)
    g.add_edge(4, 5, 11)
    g.add_edge(5, 3, 9)
    g.add_edge(5, 4, 1)
    g.add_edge(6, 0, 5)
    return g


class TestDiGraph(unittest.TestCase):

    def test_sizeGraph(self):
        g = createGraph()
        self.assertEqual(g.v_size(),7)
        self.assertEqual(g.e_size(),9)

    def test_inOutEdges(self):
        g = createGraph()
        g.add_node(7)
        g.add_edge(6, 7, 2)
        self.assertTrue(7 in g.all_out_edges_of_node(6))
        self.assertFalse(6 in g.all_out_edges_of_node(7))
        w76 = g.all_in_edges_of_node(7)[6]
        self.assertEqual(w76, 2)
        self.assertEqual(w76, g.all_out_edges_of_node(6)[7])

    def test_rmNode(self):
        g = createGraph()
        all_v = g.get_all_v().copy()
        g.remove_node(5)
        all_v.pop(5)
        self.assertDictEqual(all_v, g.get_all_v())
        self.assertEqual(g.e_size(), 6)
        self.assertEqual(g.v_size(), 6)

    def test_rmEdge(self):
        g = createGraph()
        all_out1 = g.all_out_edges_of_node(1).copy()
        g.remove_edge(1,2)
        all_out1.pop(2)
        self.assertDictEqual(all_out1,g.all_out_edges_of_node(1))
        self.assertNotEqual(g.e_size(), 7)

    def test_addNodeAndEdgeFail(self):
        g = createGraph()
        self.assertFalse(g.add_edge(5, 4, 1))  # the edge already exists
        self.assertFalse(g.add_edge(8, 2, 1))  # the first node doesn't exist
        self.assertFalse(g.add_edge(3, 8, 1))  # the second node doesn't exist
        self.assertFalse(g.add_node(4))  # the node already exists


if __name__ == '__main__':
    unittest.main()



