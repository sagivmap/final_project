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

    def setWeight(self, weight):
        self.weight = weight

    def __str__(self):
        return str("id: " + self.idd + "\n" + "Name: " + self.name  + "\nTotal number of friends: " + self.tf
                   + "\nNumber of mutual friends: " + self.mf + "\nAge of user account in years: " + str(int(int(self.aua)/365)))

    def __eq__(self, other):
        return self.idd == other.idd

    def __hash__(self):
        return hash('idd', self.idd)