class Edge:

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.weight = -1

    def __eq__(self, other):
        return self.src == other.src and self.dest == other.dest

    def __hash__(self):
        return hash(('src', self.src ,'dest' , self.dest))

    def __str__(self):
        return str("Src: " + self.src + " ,Dest: " + self.dest)