class VC:
    def __init__(self, name):
        self.name = name
        self.v = { self.name : 0 }


    def increment(self):
        self.v[self.name] += 1
        return self


    def __repr__(self):
        return "V%s" % repr(self.v)


    def __lt__(self, o):
        ks = list(set(self.v.keys()).union(set(o.v.keys())))
        ks.sort()
        def nextv(k, vz):
            if k in vz:
                return vz[k]
            else:
                return 0
        for k in ks:
            if nextv(k, self.v) > nextv(k, o.v):
                return False
        return True


    def update(self, o):
        for (k, v) in o.v.items():
            if k in self.v:
                if v >= self.v[k]:
                    self.v[k] = v
            else:
                self.v[k] = v
