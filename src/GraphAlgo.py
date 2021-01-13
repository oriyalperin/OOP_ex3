from typing import List
import json
import sys
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from src.DiGraph import DiGraph
import matplotlib.pyplot as plt
import numpy as np


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=None):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def save_to_json(self, file_name: str) -> bool:
        """
        open the given file,
        create two lists - one for the nodes and one for the edges
        pass all the nodes in the graph and add them to the nodes list:
        if there is "pos" to the node, add the node in the format: (id: , pos: )
        else - add the node in the format: (id: ) .
        pass all the edges in the graph and add them to the edges list:
        add the edge in the format: (src: , w: , dest: ) .
        write to the file the tow lists.

        """
        with open(file_name, 'w') as json_file:
            try:
                ng = {"Nodes": [], "Edges": []}
                for node in self.graph.get_all_v().values():
                    if node.pos is None:
                        ng["Nodes"].append({"id": node.id})
                    else:
                        ng["Nodes"].append({"pos": str(node.pos), "id": node.id})
                for startnode in self.graph.get_all_v().keys():
                    for endnode, weight in self.graph.all_out_edges_of_node(startnode).items():
                        ng["Edges"].append({"src": startnode, "w": weight, "dest": endnode})
                json.dump(ng, json_file)
                return True
            except Exception as e:
                print("Failed save graph to json: " + str(e))
                return False

    def load_from_json(self, file_name: str) -> bool:
        """
        open the given file,
        load the file to a json string
        create DiGraph g,
        pass the json string:
        for the "Nodes" in the string,
        pass all the nodes in the Nodes
        add each of them to the g graph.
        for the "Edges" in the string,
        pass all the edges in the g graph:
        for each edge, extract the src, w and dest
        and use g connect function
        to connect between the src and dest according to the w.
        put g into the self graph
        """

        try:
            with open(file_name) as json_file:
                json_string = json.load(json_file)
                g = DiGraph()
            for node in json_string["Nodes"]:
                key = node["id"]
                if "pos" not in node:
                    g.add_node(key)
                else:
                    x, y, z = map(float, str(node["pos"]).split(","))
                    position = (x, y, z)
                    g.add_node(key, position)
            for edge in json_string["Edges"]:
                src = edge["src"]
                dest = edge["dest"]
                weight = edge["w"]
                g.add_edge(src, dest, weight)
            self.graph = g
            return True
        except Exception as e:
            print("Failed load json to graph " + str(e))
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        uses Dijkstra algorithm.
        the nodes_weight will save for each node in the graph- the weight of it relative to the id1.
        the stackmap will be a stack which save all the nodes we saw but didn't pass of their neighbors yet.
        the shortestPathMap will save for each vertex, the predecessor node of it in this function,
        it will help us to know the path of the shortest path.
        """
        if self.graph is None or self.graph.Nodes.get(id1) is None or self.graph.Nodes.get(id2) is None:
            return float("inf"), []
        nodes_weight = {}
        stackmap = {}
        for i in self.graph.get_all_v():
            nodes_weight[i]=[sys.maxsize,False]
        shortestPathMap = {}
        nodes_weight[id1][0] = 0
        stackmap[id1] = 0
        while len(stackmap) != 0:  # while there are no vertices to check in order to find the shortest path
            min_node = -1
            min_weight = sys.maxsize
            for i in stackmap.keys():  # get the vertex with the minimum weight
                if nodes_weight.get(i)[0] < min_weight:
                    min_weight = nodes_weight.get(i)[0]
                    min_node = i
            if min_node == id2:  # if we through all the paths to the destination
                break
            dis = nodes_weight.get(min_node)[0]
            stackmap.pop(min_node)  # and remove it from the queue
            ni = self.graph.all_out_edges_of_node(min_node)  # get the neighbors of current vertex
            for i in ni.keys():  # pass the neighbors of current vertex
                if nodes_weight.get(i)[1] is False and ni.get(i) + dis < nodes_weight.get(i)[0]:
                    # if the neighbor hasn't visited yet
                    # and if we found another path to the neighbor with less total distance to it
                    nodes_weight[i][0] = ni.get(i) + dis  # update the weight to be the total distance of the last path
                    shortestPathMap[i] = min_node  # the predecessor of the neighbor will be a pointer on the current
                    # vertex that we came from it to the neighbor vertex
                    stackmap[i] = ni.get(i) + dis  # push this ni to the stack
            nodes_weight[min_node][1]= True  # we have done passing all the neighbors of the current vertex, so we are marking it
        if shortestPathMap.get(id2) is None:  # if we didn't found predecessor to the dest node
            return float("inf"), []  # there's no path to the dest from src
        x = id2
        path = [x]  # create a list that illustrate the shortest path and add the last vertex= the dest of the path
        while x != id1:  # while isn't the start of the path
            x = shortestPathMap.get(x)  # get the previous vertex that we came from it to the current vertex
            path.insert(0, x)  # add it to the top of list
        return nodes_weight[id2][0], path  # return the path

    def connected_component(self, id1: int) -> list:
        """
               uses the tarjan algorithm in a iterative way
               """
        if self.graph.v_size() == 0 or self.graph.e_size() == 0 or self.graph.Nodes.get(id1) is None:
            return []
        disc = {}
        low = {}
        time = 0
        return self._scc_id_(id1, time, disc, low)

    def connected_components(self) -> List[list]:
        """
        uses the tarjan algorithm in a iterative way
        """
        if self.graph.v_size() == 0 or self.graph.e_size() == 0:
            return [[]]
        disc = {}
        low = {}
        time = 0
        com = self._scc_(time, disc, low)
        return com

    def _scc_util_(self, u,st, com, time, disc, low, id:tuple = -1):
        work = [(u, 0)]  # recursion stack
        while work: # while the stack isn't empty
            u, i = work[-1]  # i is next successor to process.
            del work[-1]  # pop from the work stack, u and i will be the couple we just pop
            if i == 0:  # when first visiting a vertex:
                disc[u] = time  # update the discovery time of the vertex
                low[u] = time  # update the low time of the vertex
                time += 1  # increase the time
                st.append(u)  # add the vertex u to the st stack
            recurse = False  # set the recurse flag to be false until we visit a neighbor that  isn't visited
            k=0
            for ni in self.graph.all_out_edges_of_node(u).keys():  # pass all the neighbors of u
                if i>k:  # if we already pass on this neighbor of u
                    k+=1
                    continue  # skip on it to the next neighbor
                w = ni  # set w to be the current neighbor
                if w not in disc:  # if we didn't visited on w
                    work.append((u, k+1))  # add u with the next index of neighbor to pass on
                    work.append((w, 0)) # Add w to recursion stack.
                    recurse = True  # set recurse to be true cause we going to visit w
                    break  # out of the iteration on u
                elif w in st:  # if w is visited= wi is on the st stack
                    low[u] = min(low[u], disc[w])  # if disc of w smaller than low of u, set the low of u to be disc of w
                k+=1  # increase the number of neighbors that wa passed
            if recurse: continue  # if we going to visit neighbor, skip to the next iteration
            if disc[u] == low[u]:  # if after all u low isn't changed= we found component
                c= []  # c the connected component list
                flag=False  # flag will tell us if the id for one com is in this component
                while True:
                    v = st[-1]  # get the top of the stack
                    del st[-1]  # remove it from stack
                    c.insert(0,v)  # add to the top of this list component
                    if v == id:  # if there is given id and we found it in this component
                        flag=True
                    if v == u:  # if we pass all the rest of the vertices on this component
                        break  # out
                com.append(c)  # add this component to the list of all components
                if flag and id!=-1:  # if we found the id in the last component
                    return  # out of the function
            if work:  # u was recursively visited. if there is more nodes in the work stack=
                # we want to check them and set their low
                temp = u  # save u in temp
                u, _ = work[-1]  # u= pop from work stack the next vertex
                low[u] = min(low[u], low[temp])  # if the neighbor low is less then u low -set it to ni low

    def _scc_(self, time, disc, low):
        com = []
        st = []
        for node in self.graph.get_all_v().keys(): # pass all nodes in the graph
            if node not in disc:  # if we didn't visit them
                self._scc_util_(node,st,com,time,disc,low)  # found their component
        return com

    def _scc_id_(self, key, time, disc, low):
        com = []
        st = []  
        self._scc_util_(key,st, com, time, disc, low, key)  # find key component
        return com.pop(len(com)-1)  # return the key component

    def plot_graph(self) -> None:
        my_graph = self.graph
        if my_graph is not None:
            points={}
            for node in my_graph.get_all_v().values():  # pass all the nodes in the graph
                if node.pos is None:  # if there's no pos to the node
                    nc=my_graph.v_size()/2  # half of nodes size in the graph
                    while True:
                        x = np.random.uniform(1,nc)
                        y= np.random.uniform(1,nc)
                        if x not in points:
                            points[x]= {}
                        if points.get(x).get(y) is None:
                            points[x][y]=node.id
                            break
                    node.pos = (np.random.uniform(1,nc),np.random.uniform(1,nc), 0)  # node pos will be x,y ramndom beteen 1 to nc
                plt.plot(node.pos[0], node.pos[1], 'o')  # draw the node on the pos coordinate
                plt.text(node.pos[0] , node.pos[1], node.id, fontsize=11,color='red')  # drae the key node next to the node
            for node1 in my_graph.get_all_v().values():  # pass all the nodes in the graph
                for node2 in self.graph.all_out_edges_of_node(node1.id).keys(): # pass the neighbors of each node
                    posx1 = node1.pos[0]  # get the x of node pos
                    posy1 = node1.pos[1]  # get the y of node pos
                    posx2 = self.graph.Nodes.get(node2).pos[0]   # get the x of neighbor pos
                    posy2 = self.graph.Nodes.get(node2).pos[1]   # get the y of neighbor pos
                    plt.arrow(posx1, posy1, (posx2-posx1), (posy2-posy1),length_includes_head=True, head_width=0.0002,width=0)
                    # draw an arrow between the nodes

            plt.show()
