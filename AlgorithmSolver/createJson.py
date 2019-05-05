import time

from .AlgorithmSolver import AlgorithmSolver as AlgSol
import json
from ast import literal_eval

def create(path,csvType, toBig=False):
    #csvType 1 == FB , 2 == twitter

    file = open('static/file.json', 'w')

    # csv to Json
    algSolv = AlgSol(path)
    algSolv.generate(toBig)
    algSolv.add_ego_node()

    nodes = []
    links = []

    tmp = {}
    first_node = algSolv.nodes['Ego_Node']
    st = str(first_node)
    for s in st.split(' , '):
        x = s.split(' : ')
        tmp[x[0]] = x[1]

    tmp['level'] = 0
    nodes.append(tmp)

    # first circle
    for n in algSolv.first_circle_nodes:
        tmp = {}
        st = str(n)
        for s in st.split(' , ') :
            x = s.split(' : ')
            tmp[x[0]] = x[1]

        tmp['level'] = 1
        nodes.append(tmp)

     #second circle
    for n in algSolv.second_circle_nodes:
        tmp = {}
        st = str(n)
        for s in st.split(' , '):
            x = s.split(' : ')
            tmp[x[0]] = x[1]

        tmp['level'] = 2
        nodes.append(tmp)

    for l in algSolv.get_edges():
        tmp = {}
        st = str(l)
        for s in st.split(' , '):
            x = s.split(' : ')
            tmp[x[0]] = x[1]

        links.append(tmp)

    json.dump({'nodes': nodes, 'links': links}, file)