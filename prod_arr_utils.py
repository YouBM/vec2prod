import json
import fileinput
from pprint import pprint
import numpy as np
import Prod2Vec as P2V


def load_prod_arr(file):
    f = open(file)
    prod_arr = json.load(f)
    return prod_arr

def prod2vec(prod):

    p2v = P2V.Prod2Vec()
    return p2v.prod2vec(prod)

    # OBSOLETE

    sel_ids = ["SPRING_SHOES", "SUMMER_SHOES", "AUTUMN_SHOES", "WINTER_SHOES"]
    params = prod['variant_data'][0]['params']
    params_ids = [a['id'] for a in params]

    obj = {}
    for id in sel_ids:

        if id in params_ids:
            param = [a for a in params if a['id'] == id][0]
            val = 1 if param['values']['value_boolean'] == "YES" else 0
        else:
            val = -1

        obj[id] = val

    ret = []
    for a in obj:
        ret.append(obj[a])

    return np.array(ret)

def prod_arr2matrix(prod_arr):
    aa = [prod2vec(p).tolist() for p in prod_arr]
    #return aa
    m = np.matrix(aa, dtype=np.float32)
    return m

def vec_distance(v1, v2):
    return np.sum(np.power(v1 - v2, 2)) / v1.size

def vec2prod_indexes(vec, matrix, n = 1):
    #r, _ =  matrix.shape
    #return np.repeat(np.matrix([vec.tolist()]), r, axis=0)

    touples = []
    i = 0
    for row in matrix:
        d = vec_distance(row, vec)
        touples.append((d, i))
        i += 1
        #print(d)
    s = sorted(touples, key=lambda touple: touple[0])
    s = s[:n]
    ret = [a[1] for a in s]
    # print(ret)
    return ret

def vec2products(vec, matrix, prod_arr, n = 1):
    indexes = vec2prod_indexes(vec, matrix, n)
    ret = [prod_arr[i] for i in indexes]
    return ret


if __name__ == "__main__":
    prods = load_prod_arr("prod_arr.json")
    #prods = prods[:1000]
    print("Loaded %i products overall" % len(prods))

    m = prod_arr2matrix(prods)
    #print("m:", m)

    vec = np.array([0,0,0,0])#prod2vec(prods[1])
    #indexes = vec2prod_indexes(vec, m, 15)
    #print("indexes:", indexes)

    ps = vec2products(vec, m, prods, 10)
    for p in ps:
        v = prod2vec(p)
        dist = vec_distance(v, vec)
        print("dist:", dist, "v:", v, "prod:", p)
        # print()