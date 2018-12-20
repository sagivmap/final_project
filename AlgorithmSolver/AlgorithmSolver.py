from Node import Node
from Edge import Edge
import random
import string
import csv
import configparser

# initiate config file
config = configparser.ConfigParser()
config.read('config/config.ini')

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
currUser = Node('Ego_Node', 'SOURCE', '0','0','0','0',[])

class AlgorithmSolver:

    def __init__(self, path_of_csv_file):
        self.path_of_csv_file = path_of_csv_file
        self.nodes = {}
        self.edges = []
        self.first_circle_nodes = []
        self.second_circle_nodes = []
        self.first_circle_edges = []
        self.second_circle_edges = []

    def decode_name(self, name_to_decode):
        return name_to_decode.decode('string-escape')

    def makearrayfromstring(self, string):
        ans = []
        if len(string) == 2:
            return ans

        tmp = string[1:-1].split(', ')
        for x in tmp:
            ans.append(x[1:-1] + "")
        return ans

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
                    edge = Edge(self.nodes[user], node, node.fd)
                    self.nodes[user].second_friends_edges.append(edge)
                    ans.append(edge)
                    self.second_circle_edges.append(edge)

        return list(set(ans))

    def create_nodes_and_edges(self):
        with open(self.path_of_csv_file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                name = row["Name"][2:-1]
                if not name[0].isalpha():
                    name = self.decode_name()

                cf = self.makearrayfromstring(row["CF"])

                node = Node(row["ID"], name, row["TF"], row["MF"], row["AUA"], row["FD"], cf)

                self.nodes[node.idd] = node

                if '0' in cf:
                    self.first_circle_nodes.append(node)
                else:
                    self.second_circle_nodes.append(node)

        self.edges = self.create_edges()  # after that , we have all nodes and edges

        # sort of a logger
        with open('./files/firstCircle.txt', 'w') as f:
            for item in self.first_circle_nodes:
                f.write("%s\n" % item)
        with open('./files/secondCircle.txt', 'w') as f:
            for item in self.second_circle_nodes:
                f.write("%s\n" % item)
        with open('./files/allEdges.txt', 'w') as f:
            for edge in self.edges:
                f.write("%s\n" % edge)

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
            curr_tsp = curr_edge_weight * first_circle_edge.dest.weight
            for second_circle_edge in first_circle_edge.dest.second_friends_edges:
                curr_tsp *= second_circle_edge.weight
                curr_tsp *= second_circle_edge.dest.weight
                if curr_tsp > second_circle_edge.dest.tsp:
                    second_circle_edge.dest.tsp = curr_tsp

    def generate(self):
        self.create_nodes_and_edges()
        self.calculate_weights()
        self.calculate_TSP()
        pass

if __name__ == "__main__":
    algSolv = AlgorithmSolver("example.csv")
    algSolv.generate()
    pass