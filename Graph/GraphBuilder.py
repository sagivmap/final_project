import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
try:
    from AlgorithmSolver.Node import Node
except Exception as e:
    from .Node import Node

currUser = Node('Ego_Node', 'SOURCE', '0','0','0','0',[])

def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5,
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    # if parent != None:   #this should be removed for directed graphs.
    #     neighbors.remove(parent)  #if directed, then parent not in neighbors.
    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap,
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                parent = root)
    return pos

class GraphBuilder:

    def __init__(self, alg_solv):
        self.als = alg_solv
        self.first_circle_edges = alg_solv.first_circle_edges
        self.graph = nx.DiGraph()

    def draw(self):

        G = nx.DiGraph()
        color_node = []

        G.add_node(currUser.idd)
        color_node.append('blue')

        for node in self.als.first_circle_nodes:
            G.add_node(node.idd)
            color_node.append('green')

        for node in self.als.second_circle_nodes:
            G.add_node(node.idd)
            if node.tsp > 0.3 :
                color_node.append('yellow')
            else:
                color_node.append('red')

        for edge in self.als.edges:
            G.add_edge(edge.src.idd, edge.dest.idd, weight=round(edge.weight,2), color='b')

        pos = hierarchy_pos(G, currUser.idd)

        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        node_labels = {}
        for key,node in self.als.nodes.items():
            node_labels[node.idd] = str(node)

        nx.draw(G, pos=pos, node_color=color_node)
        nx.draw_networkx_labels(G,pos,node_labels, font_size=8)
        # nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

        plt.show()
