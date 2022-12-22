
class CircQ:
    def __init__(self, n):
        self.n = n
        self.q = []
        self.idx = 0

    def insert(self, elem):
        if self.idx < self.n:
            self.q.append(elem)
            self.idx += 1
        else:
            self.q[0:self.n-1] = self.q[1:self.n]
            self.q[self.n-1] = elem

    def get_window(self):
        return list(reversed(self.q))

if __name__ == '__main__':
    wq = CircQ(7)
    wq.insert('a')
    print(wq.get_window())
    wq.insert('b')
    print(wq.get_window())
    wq.insert('c')
    print(wq.get_window())
    wq.insert('d')
    print(wq.get_window())
    wq.insert('e')
    print(wq.get_window())
    wq.insert('f')
    print(wq.get_window())
    wq.insert('g')
    print(wq.get_window())
    wq.insert('h')
    print(wq.get_window())
    wq.insert('i')
    print(wq.get_window())
    wq.insert('j')
    print(wq.get_window())
    wq.insert('k')
    print(wq.get_window())
    wq.insert('l')
    print(wq.get_window())
    wq.insert('m')
    print(wq.get_window())
    wq.insert('n')
    print(wq.get_window())
    wq.insert('o')
    print(wq.get_window())