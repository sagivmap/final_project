try:
    from AlgorithmSolver.Node import Node
    from AlgorithmSolver.Edge import Edge
    from Graph.GraphBuilder import GraphBuilder
except Exception as e:
    from .Node import Node
    from .Edge import Edge
    import Graph.GraphBuilder
import re
import string
import csv
import configparser
import os.path

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "./config/config.ini")

# initiate config file
config = configparser.ConfigParser()
config.read(path)

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
currUser = Node('Ego_Node', 'Ego_Node', '0','0','0','0',[])

class AlgorithmSolver:

    def __init__(self, path_of_csv_file,tsp):
        self.path_of_csv_file = path_of_csv_file
        self.nodes = {}
        self.edges = []
        self.first_circle_nodes = []
        self.second_circle_nodes = []
        self.first_circle_edges = []
        self.second_circle_edges = []
        self.tsp = tsp

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def get_second_circle_nodes(self):
        return self.second_circle_nodes

    def _decode_name(self, name_to_decode):
        try:
            if not name_to_decode.startswith('\\x'):
                return name_to_decode[1:]
            res = re.findall(r'\\x[0-9a-f][0-9a-f]', name_to_decode)
            to_convert = ''
            for char in res:
                while not name_to_decode.startswith(char):
                    to_convert += name_to_decode[:1].encode('utf-8').hex()
                    name_to_decode = name_to_decode[1:]
                to_convert += char.replace('\\x', '')
                name_to_decode = name_to_decode[4:]

            return bytes.fromhex(to_convert).decode('utf-8')
        except Exception as e:
            return ''

    def makearrayfromstring(self, string):
        ans = []
        if len(string) == 2:
            return ans

        tmp = string[1:-1].split(', ')
        for x in tmp:
            ans.append(x[1:-1] + "")
        return ans

    def add_ego_node(self):
        nodes = {'Ego_Node' : currUser}
        nodes.update(self.get_nodes())
        self.nodes = nodes

    def create_edges(self):
        ans = []
        for key, node in self.nodes.items():
            tmp = list(set(node.cf))
            if len(tmp) == 1:
                if tmp[0] == '0':
                    edge = Edge(currUser, node, node.fd)
                    self.first_circle_edges.append(edge)
                else:
                    edge = Edge(self.nodes[tmp[0]], node, node.fd)
                    self.nodes[tmp[0]].second_friends_edges.append(edge)
                    self.second_circle_edges.append(edge)
                ans.append(edge)
            else:
                for user in tmp:
                    try:
                        edge = Edge(self.nodes[user], node, node.fd)
                    except Exception as e:
                        pass
                    self.nodes[user].second_friends_edges.append(edge)
                    ans.append(edge)
                    self.second_circle_edges.append(edge)

        return list(set(ans))

    def create_nodes_and_edges(self):
        with open(self.path_of_csv_file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                if row["Name"][:2] == 'b\'' :
                    name = row["Name"][2:-1]
                else:
                    name = row["Name"];
                try:
                    if(len(name)>0):
                        if not name[0].isalpha():
                            name = self._decode_name(name)
                except Exception as e:
                    print (e)

                cf = self.makearrayfromstring(row["CF"])

                node = Node(row["ID"], name, row["TF"], row["MF"], row["AUA"], row["FD"], cf)

                self.nodes[node.idd] = node

                if '0' in cf:
                    self.first_circle_nodes.append(node)
                else:
                    self.second_circle_nodes.append(node)

        self.edges = self.create_edges()  # after that , we have all nodes and edges


    def __calc_c_tf(self, total_friend):
        if total_friend >= config.getint('VariableConsts','tf_barrier'):
            return 1
        else:
            return total_friend / config.getint('VariableConsts','tf_barrier')

    def __calc_c_mf(self, mutual_friends):
        if mutual_friends >= config.getint('VariableConsts','mf_barrier'):
            return 1
        else:
            return mutual_friends / config.getint('VariableConsts','mf_barrier')

    def __calc_c_aua(self, age_of_user_account):
        if age_of_user_account >= config.getint('VariableConsts','aua_barrier'):
            return 1
        else:
            return age_of_user_account / config.getint('VariableConsts','aua_barrier')

    def __calculate_node_weights(self):
        """
        Calculate the c score of node (Facebook user) according to research article
        :return:
        """
        for keys, node in self.nodes.items():
            num_of_parameters = 0
            if node.tf != '-1':
                num_of_parameters += 1
                c_tf = self.__calc_c_tf(int(node.tf))
            else:
                c_tf = 0

            if node.mf != '-1':
                num_of_parameters += 1
                c_mf = self.__calc_c_mf(int(node.mf))
            else:
                c_mf = 0

            if node.aua != '-1':
                num_of_parameters += 1
                c_aua = self.__calc_c_aua(int(node.aua))
            else:
                c_aua = 0

            if num_of_parameters == 0:
                node.weight = 1
            else:
                node.weight = (c_tf + c_mf + c_aua) / num_of_parameters

    def __calc_p_fd(self, friendship_duration):
        if friendship_duration >= config.getint('VariableConsts','fd_barrier'):
            return 1
        else:
            return friendship_duration / config.getint('VariableConsts','fd_barrier')

    def __calculate_edge_weights(self):
        """
        for each edge that have FD attribute (only first circle edges) calc edge weight
        :return:
        """
        for edge in self.first_circle_edges:
            num_of_parameters = 0
            if edge.fd != '-1':
                num_of_parameters += 1
                p_fd = self.__calc_p_fd(int(edge.fd))
            else:
                p_fd = 0

            if num_of_parameters == 0:
                edge.weight = 1
            else:
                edge.weight = p_fd

        for edge in self.second_circle_edges:
            edge.weight = 1

    def calculate_weights(self):
        """
        function that calculate weights for each node and edge
        :return:
        """
        self.__calculate_node_weights()
        self.__calculate_edge_weights()
        pass

    def calculate_TSP(self):
        for first_circle_edge in self.first_circle_edges:
            curr_edge_weight = first_circle_edge.weight
            edge_node_score = curr_edge_weight * first_circle_edge.dest.weight
            for second_circle_edge in first_circle_edge.dest.second_friends_edges:
                curr_tsp = edge_node_score * second_circle_edge.weight * second_circle_edge.dest.weight
                if curr_tsp > second_circle_edge.dest.tsp:
                    second_circle_edge.dest.tsp = curr_tsp

    def get_first_circle_nodes_and_edges_for_seconde_circle_node(self, node):
        edges = []
        first_circle_nodes = set()

        for edge in self.second_circle_edges:
            if edge.dest.idd == node.idd:
                edges.append(edge)
                first_circle_nodes.add(edge.src)
                for firstedge in self.first_circle_edges:
                    if firstedge.dest.idd == edge.src.idd:
                        edges.append(firstedge)

        return first_circle_nodes, edges

    def getOnlyBadConnections(self):
        bad_second_level_node = (list(filter(lambda x: x.tsp < self.tsp, self.second_circle_nodes)))

        bad_first_circle_nodes = set()
        bad_edges = []
        for bad_node in bad_second_level_node:
            first_circle_nodes, edges = self.get_first_circle_nodes_and_edges_for_seconde_circle_node(bad_node)
            bad_first_circle_nodes.update(first_circle_nodes)
            bad_edges.extend(edges)

        bad_first_circle_nodes = list(bad_first_circle_nodes)
        self.first_circle_nodes = bad_first_circle_nodes
        self.edges = bad_edges
        self.second_circle_nodes = bad_second_level_node

    def generate(self, toBig):
        self.create_nodes_and_edges()
        self.calculate_weights()
        self.calculate_TSP()
        if toBig:
            self.getOnlyBadConnections()

if __name__ == "__main__":
    algSolv = AlgorithmSolver("test1.csv")
    algSolv.generate()
    graph = GraphBuilder(algSolv)
    graph.draw()

    pass