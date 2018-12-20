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
currUser = "Sagiv"

class AlgorithmSolver:

    def __init__(self, path_of_csv_file):
        self.path_of_csv_file = path_of_csv_file
        self.nodes = []
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

        for node in self.nodes:
            tmp = list(set(node.cf))
            if len(tmp) == 1:
                if tmp[0] == '0':
                    edge = Edge(currUser, node.idd, node.fd)
                    self.first_circle_edges.append(edge)
                else:
                    edge = Edge(tmp[0], node.idd, node.fd)
                    self.second_circle_edges.append(edge)
                ans.append(edge)
            else:
                for user in tmp:
                    edge = Edge(user, node.idd, node.fd)
                    ans.append(edge)
                    self.first_circle_edges.append(edge)

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

                self.nodes.append(node)

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

    def __calculate_node_weights(self):
        """
        Calculate the c score of node (Facebook user) according to research article
        :return:
        """
        for node in self.nodes:
            num_of_parameters = 0
            if node.tf != '-1':
                num_of_parameters += 1
                c_tf = self.__calc_c_tf(int(node.tf))


    def calculate_weights(self):
        """
        function that calculate weights for each node and edge
        :return:
        """
        self.__calculate_node_weights()

    def generate(self):
        self.create_nodes_and_edges()
        self.calculate_weights()


if __name__ == "__main__":
    algSolv = AlgorithmSolver("example.csv")
    algSolv.generate()
    pass