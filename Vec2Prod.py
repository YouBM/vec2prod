
from prod_arr_utils import *


class Prod:
    def __init__(self, dist, vec, product):
        self.dist = dist
        self.vec = vec
        self.product = product

    def __str__(self):
        return "dist: {0}, vec: {1}, product: {2}".format(self.dist, self.vec, self.product)


class Vec2Prod:

    def __init__(self, prod_arr_file = "prod_arr.json"):
        self._prod_arr = load_prod_arr(prod_arr_file)
        self._matrix = prod_arr2matrix(self._prod_arr)

    def vec2prods(self, vec, n = 1):
        return vec2products(vec, self._matrix, self._prod_arr, n)


    def vec2Prods(self, vec, n = 1):
        prods = self.vec2prods(vec, n)

        ret = []
        for p in prods:
            v = prod2vec(p)
            d = vec_distance(v, vec)
            ret.append(Prod(d, v, p))

        return ret


if __name__ == "__main__":
    v2p = Vec2Prod("prod_arr.json")
    prods = v2p.vec2Prods(np.array([0, 0, 0, 0]), 10)
    for p in prods:
        print(p)
