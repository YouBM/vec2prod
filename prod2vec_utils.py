import json
import fileinput
from pprint import pprint

from prod_arr_utils import *

gparams_names = ['brand',
 'title_full',
 'product_id',
 'price',
 'description',
 'MENS_SHOES',
 'TYPE_OF_SHOES',
 'DETERMINATION_OF_SHOES',
 'SIZE_EUR',
 'COLOR',
 'MATERIAL',
 'SHOES_HIGH',
 'TIE',
 'HEEL',
 'TYPE_OF_TOE',
 'SPRING_SHOES',
 'SUMMER_SHOES',
 'AUTUMN_SHOES',
 'WINTER_SHOES',
 'SEASON_OF_YEAR',
 'COLLECTION_NM',
 'SPORT',
 'FASHION',
 'DETERMINATION',
 'MEN_WOMEN',
 'WOMENS_SHOES',
 'GIRLS_SHOES',
 'BOYS_SHOES',
 'MEMBRANE',
 'SIZE_UK',
 'EXTENDED_SELECTION',
 'SIZE',
 'TYPE_USAGE',
 'TYPE_OF_BINDING',
 'RUNNER',
 'WEIGHT_G']



def prod2lparams(prod):
    s = prod['variant_id'][len(prod['product_id']):]
    variantI = 0 if s == "" else int(s) - 1
    variant = prod['variant_data'][variantI]

    ret = {}

    ret['brand'] = prod['brand']['brand_id']
    ret['description'] = prod['brief_plain']['C']
    #ret['date'] = ret['date']
    ret['title_full'] = prod['title_full']['C']
    ret['product_id'] = prod['product_id']
    #ret['brief_plain'] = prod['product_id']

    ret['price'] = int(variant['price']['CZ1000']['price'])


    params = variant['params']
    #print(variant)
    for param in params:
        key = param['id']
        if 'value_boolean' in param['values']:
            ret[key] = True if param['values']['value_boolean'] == 'YES' else False
        if 'value_string' in param['values']:
            ret[key] = param['values']['value_string'][0]
        if 'value_double' in param['values']:
            ret[key] = float(param['values']['value_double'][0])

    return ret

def prod2gparams(prod):
    lparams = prod2lparams(prod)
    ret = {}
    for gp in gparams_names:
        ret[gp] = lparams[gp] if gp in lparams else None
    return ret

def prod2vec(prod):
    gp = prod2gparams(prod)
    ret = []

    if gp['COLOR'] == None:
        gp['COLOR'] = ""

    # color
    ret += [1] if "BLACK" in gp['COLOR'] else [0]
    ret += [1] if "BLUE" in gp['COLOR'] else [0]
    ret += [1] if "BROWN" in gp['COLOR'] else [0]
    ret += [1] if "GREY" in gp['COLOR'] else [0]
    ret += [1] if "ORANGE" in gp['COLOR'] else [0]
    ret += [1] if "PINK" in gp['COLOR'] else [0]
    ret += [1] if "RED" in gp['COLOR'] else [0]
    ret += [1] if "WHITE" in gp['COLOR'] else [0]

    ret += [1] if "CHILD`S" == gp['DETERMINATION'] else [0]

    ret += [1] if "CASUAL" == gp['DETERMINATION_OF_SHOES'] else [0]
    ret += [1] if "OUTDOOR" == gp['DETERMINATION_OF_SHOES'] else [0]
    ret += [1] if "SPORT" == gp['DETERMINATION_OF_SHOES'] else [0]

    ret += [1] if "HEEL" == gp['HEEL'] else [0]

    # HACK
    if gp['MATERIAL'] == None:
        gp['MATERIAL'] = ""

    ret += [1] if "LEATHER" in gp['MATERIAL'] else [0]
    ret += [1] if "TEXTILE" in gp['MATERIAL'] else [0]
    ret += [1] if "SYNTETIC" in gp['MATERIAL'] else [0]

    ret += [1] if "FOR BOYS" == gp['MEN_WOMEN'] or "FOR CHILDREN" == gp['MEN_WOMEN'] else [0]

    # HACK
    if gp['SEASON_OF_YEAR'] == None:
        gp['SEASON_OF_YEAR'] = ""

    ret += [1] if "SPRING" in gp['SEASON_OF_YEAR'] else [0]
    ret += [1] if "WINTER" in gp['SEASON_OF_YEAR'] else [0]
    ret += [1] if "AUTUMN" in gp['SEASON_OF_YEAR'] else [0]
    ret += [1] if "SUMMER" in gp['SEASON_OF_YEAR'] else [0]

    ret += [1] if "ANKLE" == gp['SHOES_HIGH'] else [0]
    ret += [1] if "HIGH" == gp['SHOES_HIGH'] else [0]
    ret += [1] if "LOW" == gp['SHOES_HIGH'] else [0]
    ret += [1] if "MID" == gp['SHOES_HIGH'] else [0]
    ret += [1] if "UNDER_KNEE" == gp['SHOES_HIGH'] else [0]

    # SIZE
    if gp['SIZE_EUR'] == None:
        gp['SIZE_EUR'] = 0
    sizes_thresholds = range(19, 49, 1)
    for size in sizes_thresholds:
        ret += [1] if (gp['SIZE_EUR'] >= size and
            gp['SIZE_EUR'] < size + 3) else [0]


    ret += [1] if "YES" == gp['SPORT'] else [0]
    ret += [1] if "NO" == gp['SPORT'] else [0]

    # TODO
    return np.array(ret)



def get_gparams_names(prod_arr):
    param_names = []
    for prod in prod_arr:
        lparams = prod2lparams(prod)
        for lparam in lparams:
            if not lparam in param_names:
                param_names.append(lparam)

    return param_names

def get_gparams_values(prod_arr):
    #gp_names = get_gparams_names(prod_arr)
    ret = {}

    for prod in prod_arr:
        gparams = prod2gparams(prod)
        for pname in gparams:
            val = gparams[pname]
            if not pname in ret:
                ret[pname] = {}

            if not val in ret[pname]:
                ret[pname][val] = 1
            else:
                ret[pname][val] += 1

    return ret





if __name__ == "__main__":
    prod_arr = load_prod_arr("prod_arr.json")#[100:120]

    #pprint([(a['title_full'], a['prod_arr)

    #print(len(prod_arr))
    prod = prod_arr[0]
    #vec = prod2gparams(prod)

    #vals = get_gparams_values(prod_arr)
    #pprint(vals)

    #gparams_names = get_gparams_names(prod_arr)
    #print(len(gparams_names))
    #pprint(vec)
    #pprint(prod)
    for prod in prod_arr:
        gparams = prod2gparams(prod)
        pprint(gparams)


    vec = prod2vec(prod)
    pprint(vec)

    #print("File saved.")