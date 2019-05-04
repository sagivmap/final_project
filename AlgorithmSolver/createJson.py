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

    # json.dump({'nodes': nodes, 'links': links}, jsonfile)

    x = {
        "nodes": [
            {"id": 0, "name": "Ego Node", "TF": "", "AUA": "", "MF": "", "FD": "", "TSP": -1, "level": 0},
            {"id": 1, "name": "bob", "TF": "89", "AUA": "197", "MF": "", "FD": "", "TSP": -1, "level": 1},
            {"id": 2, "name": "charlie", "TF": "78", "AUA": "197", "MF": "", "FD": "", "TSP": -1, "level": 1},
            {"id": 3, "name": "david", "TF": "97", "AUA": "356", "MF": "", "FD": "", "TSP": -1, "level": 1},
            {"id": 4, "name": "eve", "TF": "76", "AUA": "51", "MF": "3", "FD": "", "TSP": 0.17, "level": 2},
            {"id": 5, "name": "frank", "TF": "95", "AUA": "334", "MF": "2", "FD": "", "TSP": 0.32, "level": 2}
        ],
        "links": [
            {"source": 1, "target": 4},
            {"source": 3, "target": 5},
            {"source": 0, "target": 3},
            {"source": 0, "target": 1},
            {"source": 3, "target": 4},
            {"source": 2, "target": 4},
            {"source": 2, "target": 5},
            {"source": 0, "target": 2}
        ]
    }

    file = open('static/file.json', 'w')
    f = json.dumps(x)
    file.write(f)
    file.close()
