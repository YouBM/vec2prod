import json
import fileinput
from pprint import pprint


def file_to_prod_arr(file):
    f = open("products.json")

    ids = []
    ret = []
    i = 0
    for line in f:
        obj = json.loads(line)


        i += 1

        pid = int(obj['product_id'])

        if not pid in ids:
            ids.append(pid)
            ret.append(obj)

        #pprint(pid)
        #if i >= 100:
        #    break
        if i%500 == 0:
            print("Processing line %i and got %i products" % (i, len(ret)))

    #ret = [ret[k] for k in ret]
    return ret



if __name__ == "__main__":
    prods = file_to_prod_arr("products.json")

    print("Got %i products overall" % len(prods))

    f = open("prod_arr.json", "w+")
    #for id in prods:
    #    prod = prods[id]
    #    json.dump(prod, f)
    #    f.write("\n")

    json.dump(prods, f)
    f.close()

    print("File saved.")