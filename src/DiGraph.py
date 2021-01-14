from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self.Nodes={}
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
            return self.Nodes.get(id1).edges_in
        return {}

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.Nodes.get(id1) is not None:
            return self.Nodes.get(id1).edges_out
        return {}

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.Nodes.get(id1) is None or self.Nodes.get(id2) is None \
                or id1==id2 or self.Nodes.get(id1).edges_out.get(id2) is not None or weight <=0 :
            return False
        self.Nodes.get(id1).edges_out[id2]= weight
        self.Nodes.get(id2).edges_in[id1] = weight
        self.EdgeCount += 1
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.Nodes.get(node_id) is not None:
            return False
        self.Nodes[node_id] = node_data(node_id, pos)
        self.mc += 1
        self.NodeCount += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if self.Nodes.get(node_id) is not None:
            for i in self.Nodes.get(node_id).edges_in.keys(): # pass all the predecessors of node_id
                self.Nodes.get(i).edges_out.pop(node_id)  # remove the node_id from edges in of the predecessor
                self.EdgeCount -= 1
            for i in self.Nodes.get(node_id).edges_out.keys():  # pass all the successors of node_id
                self.Nodes.get(i).edges_in.pop(node_id)  # remove the node_id from edges out of the successor
                self.EdgeCount -= 1
            self.Nodes.pop(node_id)
            self.mc += 1
            self.NodeCount -= 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.Nodes.get(node_id1) is not None and self.Nodes.get(node_id2) is not None and self.Nodes.get(node_id1).\
                edges_out.get(node_id2) is not None:
            self.Nodes.get(node_id1).edges_out.pop(node_id2)  # remove the id2 from edges in of the predecessor
            self.Nodes.get(node_id2).edges_in.pop(node_id1)  # remove the id1 from edges out of the successor
            self.EdgeCount -= 1
            self.mc += 1
            return True
        return False

    def __repr__(self):
        return "Graph: "+ "|V|= " +str(self.NodeCount) + " |E|= "+str(self.EdgeCount)


class node_data:

    def __init__(self, key, pos=None):
        self.id = key
        self.pos = pos
        self.edges_out ={}
        self.edges_in ={}

    def __repr__(self):
        if self.pos is not None:
            return str(self.id)+" pos: "+self.pos+" |edges out| "+str(len(self.edges_out))+" |edges in| "+str(len(self.edges_out))
        else:
            return str(self.id)+": |edges out| "+str(len(self.edges_out))+" |edges in| "+str(len(self.edges_in))
