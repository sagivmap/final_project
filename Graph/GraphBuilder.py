import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from Node import Node

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

        for edge in self.als.edges:
            G.add_edge(edge.src.idd, edge.dest.idd, weight=round(edge.weight,2), label='sagiv')

        pos = hierarchy_pos(G, currUser.idd)
        nx.draw(G, pos=pos)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        node_labels = {}
        for node in self.als.nodes:
            pass
                # node_labels[node.idd] = str(node)
        # nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        plt.show()















































        # X, Y = bipartite.sets(f)
        # pos = dict()
        # pos.update((n, (1, i)) for i, n in enumerate(X))  # put nodes from X at x=1
        # pos.update((n, (2, i)) for i, n in enumerate(Y))  # put nodes from Y at x=2
        # # nx.draw(f, pos=pos)
        # X, Y = bipartite.sets(g)
        # pos = dict()
        # pos.update((n, (1, i)) for i, n in enumerate(X))  # put nodes from X at x=1
        # pos.update((n, (2, i)) for i, n in enumerate(Y))  # put nodes from Y at x=2
        # # nx.draw(g, pos=pos)
        # F = nx.compose(f, g)
        # nx.draw(F)
        # plt.show()

        # G = nx.complete_multipartite_graph(1, 2, 3)
        #
        # nx.draw(G)
        # plt.show()

        # g.add_nodes_from(self.als.first_circle_edges, bipartite=0)
        # g.add_nodes_from(self.als.second_circle_edges, bipartite=1)

        # B.add_edges_from(aux)

        # plt.figure()
        #
        # edges = B.edges()
        # print(edges)

        # X, Y = bipartite.sets(B)
        # pos = dict()
        # pos.update((n, (1, i)) for i, n in enumerate(X))  # put nodes from X at x=1
        # pos.update((n, (2, i)) for i, n in enumerate(Y))  # put nodes from Y at x=2
        # nx.draw(B, pos=pos)
        # plt.show()

        # X,Y,Z = bipartite.sets(g)
        # edges = g.edges
        # pos = dict()
        # pos.update((n, (1, i)) for i, n in enumerate(Y))  # put nodes from X at x=1
        # pos.update((n, (2, i)) for i, n in enumerate(Z))  # put nodes from Y at x=2
        # pos.update()
        # for edge in self.als.first_circle_edges:
        #     g.add_edges_from([(edge.src.idd, edge.dest.idd)], weight=edge.weight)
        #
        # nx.draw_networkx(g, pos=pos, edges=edges)
        # # nx.draw(g)
        # plt.show()



























        # self.graph.add_node(currUser.idd, color=blue)

        # for edge in self.als.first_circle_edges:
        #     self.graph.add_node(edge.dest.idd)
        #     self.graph.add_edges_from([(edge.src.idd, edge.dest.idd)], weight=edge.weight, color="green")

        # nx.draw(self.graph)
        # plt.show()
        #
        # # for edge in self.als.second_circle_edges:
        #     self.graph.add_node(edge.dest.idd, level=3)
        #     self.graph.add_edges_from([(edge.src.idd, edge.dest.idd)], weight=edge.weight)


# import networkx as nx
# import matplotlib.pyplot as plt
# from networkx.algorithms import bipartite
# from Node import Node
#
#
#
#
# class GraphBuilder:
#     def _init_(self, als):
#         self.als = als
#         self.first_circle_edges = als.first_circle_edges
#         self.graph = nx.DiGraph()
#
#     def draw(self):
#         # self.graph = nx.DiGraph()
#         #
#
#         # val_map = {'A': 1.0, 'D': 0.5714285714285714, 'H': 0.0}
#         #
#         # values = [val_map.get(node, 0.45) for node in self.graph.nodes()]
#         # edge_labels = dict([((u, v,), d['weight']) for u, v, d in self.graph.edges(data=True)])
#         # red_edges = [('C', 'D'), ('D', 'A')]
#         # edge_colors = ['black' if edge not in red_edges else 'red' for edge in self.graph.edges()]
#         #
#         # pos = nx.spring_layout(self.graph)
#         # nx.draw_networkx_labels(self.graph, pos)
#         # nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
#         # nx.draw(self.graph, pos, node_color=values, node_size=200, edge_color=edge_colors, edge_cmap=plt.cm.Reds)
#         # plt.show()
#         # import pylab as pltt
#         # nx.draw(self.graph, pos=graphviz_layout(self.graph), node_size=1600, cmap=plt.cm.Blues,
#         #         node_color=range(len(self.graph)),
#         #         prog='dot')
#         # pltt.show()
#         import networkx as nx
#         import pylab as plt
#         from networkx.drawing.nx_agraph import graphviz_layout
#
#         self.graph = nx.DiGraph()
#         self.graph.add_node(1, level=1)
#         self.graph.add_node(2, level=2)
#         self.graph.add_node(3, level=2)
#         self.graph.add_node(4, level=3)
#
#         self.graph.add_edge(1, 2)
#         self.graph.add_edge(1, 3)
#         self.graph.add_edge(2, 4)
#
#         nx.draw(self.graph, pos=graphviz_layout(self.graph), node_size=1600, cmap=plt.cm.Blues,
#                  node_color=range(len(self.graph)),
#                  prog='dot')

        # G = nx.cubical_graph()
        # pos = nx.spring_layout(G)  # positions for all nodes

        # self.graph.add_node(currUser.idd, color=blue)

        # for edge in self.als.first_circle_edges:
        #     self.graph.add_node(edge.dest.idd)
        #     self.graph.add_edges_from([(edge.src.idd, edge.dest.idd)], weight=edge.weight, color="green")

        # nodes
        # nx.draw_networkx_nodes(G, pos,
        #                        nodelist=[0, 1, 2, 3],
        #                        node_color='r',
        #                        node_size=500,
        #                        alpha=0.8)
        # nx.draw_networkx_nodes(G, pos,
        #                        nodelist=[4, 5, 6, 7],
        #                        node_color='b',
        #                        node_size=500,
        #                        alpha=0.8)
        #
        # # edges
        # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        # nx.draw_networkx_edges(G, pos,
        #                        edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
        #                        width=8, alpha=0.5, edge_color='r')
        # nx.draw_networkx_edges(G, pos,
        #                        edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
        #                        width=8, alpha=0.5, edge_color='b')
        #
        # # some math labels
        # labels = {}
        # labels[0] = r'$a$'
        # labels[1] = r'$b$'
        # labels[2] = r'$c$'
        # labels[3] = r'$d$'
        # labels[4] = r'$\alpha$'
        # labels[5] = r'$\beta$'
        # labels[6] = r'$\gamma$'
        # labels[7] = r'$\delta$'
        # nx.draw_networkx_labels(G, pos, labels, font_size=16)
        #
        # plt.axis('off')
        # # plt.savefig("labels_and_colors.png")  # save as png
        # plt.show()  # display