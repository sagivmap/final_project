from .AlgorithmSolver import AlgorithmSolver as AlgSol
import json
from ast import literal_eval

def create(path,csvType):
    #csvType 1 == FB , 2 == twitter

    # csv to Json
    algSolv = AlgSol(path)
    algSolv.generate()
    algSolv.add_ego_node()

    nodes = []
    links = []

    jsonfile = open('static/file.json', 'w')
    indexs = {}
    index = 0

    for n in algSolv.get_nodes().values():
        tmp = {}
        st = str(n)
        for s in st.split(' , ') :
            x = s.split(' : ')
            tmp[x[0]] = x[1]

        nodes.append(tmp)
        indexs[tmp['Name']] = index
        index += 1

    for l in algSolv.get_edges():
        tmp = {}
        st = str(l)
        for s in st.split(' , '):
            x = s.split(' : ')
            if x[1] in indexs.keys():
                tmp[x[0]] = indexs[x[1]]
            else:
                tmp[x[0]] = x[1]

        links.append(tmp)

    json.dump({'nodes': nodes, 'links': links}, jsonfile)

    jsonfile.close()
