# 从 wikipedia 复制来的实现
# https://en.wikipedia.org/wiki/Extendible_hashing
import random

PAGE_SZ = 10


class Page(object):
    def __init__(self) -> None:
        self.m = []
        self.d = 0

    def full(self) -> bool:
        return len(self.m) >= PAGE_SZ

    def put(self, k, v) -> None:
        for i, (key, value) in enumerate(self.m):
            if key == k:
                del self.m[i]
                break
        self.m.append((k, v))

    def get(self, k):
        for key, value in self.m:
            if key == k:
                return value


class EH(object):
    def __init__(self) -> None:
        self.gd = 0
        self.pp = [Page()]

    def get_page(self, k):
        h = hash(k)
        return self.pp[h & ((1 << self.gd) - 1)]

    def put(self, k, v) -> None:
        p = self.get_page(k)
        full = p.full()
        p.put(k, v)
        if full:
            if p.d == self.gd:
                self.pp *= 2
                self.gd += 1

            p0 = Page()
            p1 = Page()
            p0.d = p1.d = p.d + 1
            bit = 1 << p.d
            for k2, v2 in p.m:
                h = hash(k2)
                new_p = p1 if h & bit else p0
                new_p.put(k2, v2)

            for i in range(hash(k) & (bit - 1), len(self.pp), bit):
                self.pp[i] = p1 if i & bit else p0

    def get(self, k):
        return self.get_page(k).get(k)


if __name__ == "__main__":
    eh = EH()
    N = 10088
    elements = list(range(N))

    random.shuffle(elements)
    for x in elements:
        eh.put(x, x)

    for i in range(N):
        assert eh.get(i) == i
