
import pprint
from prod2vec_utils import *
import Utils


class Prod2Vec:

    def __init__(self):
        pass

    def prod2vec(self, prod):
        return prod2vec(prod)

    def prod2params(self, prod):
        return prod2gparams(prod)





if __name__ == "__main__":
    #v2p = Vec2Prod("prod_arr.json")
    #prods = v2p.vec2Prods(np.array([0, 0, 0, 0]), 10)
    #for p in prods:
    #    print(p)
    prod_arr = Utils.load_prod_arr("prod_arr.json")
    prod = prod_arr[0]

    p2v = Prod2Vec()

    obj = []
    for prod in prod_arr[0:2]:
        vec = p2v.prod2vec(prod)
        params = p2v.prod2params(prod)
        obj.append({"params": params, "vec": vec})
        #pprint(params)
        #print(vec)

    print(obj)
    pass
