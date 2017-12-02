import pprint

from Prod2Vec import *
from Vec2Prod import *
import Utils


p2v = Prod2Vec()
v2p = Vec2Prod("prod_arr.json")

prod_arr = Utils.load_prod_arr("prod_arr.json")

prod = prod_arr[0]

pprint(p2v.prod2params(prod))

vec = p2v.prod2vec(prod)
print(vec)

pprods = v2p.vec2Prods(vec, 5)

for pprod in pprods:
    print(pprod)