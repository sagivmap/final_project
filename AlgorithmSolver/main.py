
from Node import Node
from Edge import Edge
import random, string, csv


VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
currUser = "Sagiv"

def generate_word(length):
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)

    return word[0].upper() + word[1:] #name starts with capital letter

def makearrayfromstring(string):
    ans = []
    if len(string) == 2 :
        return ans

    tmp = string[1:-1].split(', ')
    for x in tmp:
        ans.append(x[1:-1] + "")
    return ans

def create_edges():
    ans = []

    for node in allNodes:
        tmp = list(set(node.cf))
        if len(tmp) == 1:
            ans.append(Edge(node.idd,currUser if tmp[0] == '0' else tmp[0]))
        else:
            for user in tmp:
                ans.append(Edge(node.idd, user))

    return list(set(ans))

def graph(nodes,edges):
    return []

with open('sagivData.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    allNodes = []
    firstCircle = []
    secondCircle = []
    for row in csv_reader:
        name = row["Name"][2:-1]
        if not name[0].isalpha() :
            name = generate_word(5) + ' ' + generate_word(5)

        cf = makearrayfromstring(row["CF"])

        x = Node(row["ID"],name,row["TF"],row["MF"],row["AUA"],row["FD"],cf)

        allNodes.append(x)

        if '0' in cf:
            firstCircle.append(x)
        else:
            secondCircle.append(x)

allEdges = create_edges() #after that , we have all nodes and edges

graph = graph(allNodes, allEdges)

#sort of a logger
with open('./files/firstCircle.txt', 'w') as f:
    for item in firstCircle:
        f.write("%s\n" % item)
with open('./files/secondCircle.txt', 'w') as f:
    for item in secondCircle:
        f.write("%s\n" % item)
with open('./files/allEdges.txt', 'w') as f:
    for edge in allEdges:
        f.write("%s\n" % edge)

'''
TODO:
    add weight func
    impl dinitz
    add visualization
'''


