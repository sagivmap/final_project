class Node:

    def __init__(self, idd, name, tf, mf, aua, fd, cf):
        self.idd = idd
        self.name = name
        self.tf = tf  if not tf == "" else "-1"
        self.mf = mf
        self.aua = aua  if not aua == "" else "-1"
        self.fd = fd  if not fd == "" else "-1"
        self.cf = cf
        self.weight = -1
        self.tsp = 0
        self.second_friends_edges = []

    def setWeight(self, weight):
        self.weight = weight

    def __str__(self):
        if self.tsp == 0:
            return str("id: " + self.idd + "\n" + "Name: " + self.name  + "\nTF: " + self.tf
                   + "\nMF: " + self.mf + "\nAUA: " + str(int(self.aua)))
        else:
            return str("id: " + self.idd + "\n" + "Name: " + self.name  + "\nTF: " + self.tf
                   + "\nMF: " + self.mf + "\nAUA: " + str(int(self.aua)) +"\nTSP: " +str(round(self.tsp,2)))


    def __eq__(self, other):
        return self.idd == other.idd

    def __hash__(self):
        return hash(self.idd)