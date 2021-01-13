from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.Nodes={}
        self.Edges={}
        self.EdgeCount=0
        self.NodeCount=0
        self.mc=0

    def v_size(self) -> int:
        return self.NodeCount

    def e_size(self) -> int:
        return self.EdgeCount

    def get_all_v(self) -> dict:
        return self.Nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        if self.Nodes.get(id1) is not None:
            return self.Edges.get(id1)[0]
        return None

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.Nodes.get(id1) is not None:
            return self.Edges.get(id1)[1]
        return None

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.Nodes.get(id1) is None or self.Nodes.get(id2) is None \
                or id1==id2 or self.Edges.get(id1)[1].get(id2) is not None or weight <=0 :
            return False
        self.Edges.get(id1)[1][id2] = weight
        self.Edges.get(id2)[0][id1] = weight
        self.EdgeCount += 1
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.Nodes.get(node_id) is not None:
            return False
        self.Nodes[node_id] = Node(node_id, pos)
        self.Edges[node_id] = [{}, {}]
        self.mc += 1
        self.NodeCount += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if self.Nodes.get(node_id) is not None:
            for i in self.Edges.get(node_id)[0].keys():  # pass all the successors of node_id
                self.Edges.get(i)[1].pop(node_id)  # remove the node_id from edges out of the successor
                self.EdgeCount -= 1
            for i in self.Edges.get(node_id)[1].keys():  # pass all the predecessors of node_id
                self.Edges.get(i)[0].pop(node_id)  # remove the node_id from edges in of the predecessor
                self.EdgeCount -= 1
            self.Nodes.pop(node_id)
            self.Edges.pop(node_id)
            self.mc += 1
            self.NodeCount -= 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.Nodes.get(node_id1) is not None and self.Nodes.get(node_id2) and self.Edges.get(node_id1)[1].get(
                node_id2) is not None:
            self.Edges.get(node_id1)[1].pop(node_id2)  # remove the id2 from edges in of the predecessor
            self.Edges.get(node_id2)[0].pop(node_id1)  # remove the id1 from edges out of the successor
            self.EdgeCount -= 1
            self.mc += 1
        return False

    def __repr__(self):
        return "{}".format(self.Edges)


class Node:

    def __init__(self, key, pos=None):
        self.id = key
        self.pos = pos

    def __repr__(self):
        if self.pos is not None:
            return "(key: {}, pos: {},)".format(self.id, self.pos)
        else:
            return "(key: {})".format(self.id)




