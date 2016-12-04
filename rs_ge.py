import requests 
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys

graphstring = "http://services.runescape.com/m=itemdb_oldschool/api/graph/%s.json"
base_call = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=%s'
def getprice(id):
    print(int(str(json.loads(info(id))['item']['current']['price']).replace(',','')))
    return(int(str(json.loads(info(id))['item']['current']['price']).replace(',','')))

def info(id):
    return(requests.get(base_call % id).text)
def description(id):
    return (json.loads(info(id))['item']['description'])

def name(id):
    return((json.loads(info(id))['item']['name']))

def normalize(data):
    maximum = max(data)
    return [i/maximum for i in data]

def get_data(id, normalized=True):
    item_json = json.loads(requests.get(graphstring % id, timeout=30).text)['daily']
    stamps = []
    for s in item_json.keys():
        stamps.append((s, item_json[s]))
    
    stamps = sorted(stamps, key=lambda stamp: int(stamp[0])) # Sort the list by its date in ascending order.

    prices = [s[1] for s in stamps] # get prices from stamps
    average = int(sum(prices) / len(prices))
    min_price = min(prices)
    max_price = max(prices)
    if normalized:
        normalized_prices = normalize(prices)

    print("The minimum price over the past 180 days for %s is: %s" % (str(id), str(min_price)))
    print("The average price is: " + str(average))
    stdev = np.std(normalized_prices) if normalized else np.std(prices)
    print("The standard deviation is %s." % str(stdev))
    
    if normalized:
        return {'prices':normalized_prices, 'min_price':min_price, 'max_price':max_price, 'avg_price':average, 'stdev':stdev}
    else:
        return {'prices':prices, 'min_price':min_price, 'max_price':max_price, 'avg_price':average, 'stdev':stdev}

def getrend(id):
    print(str(json.loads(info(id))['item']))

def main():
    from time import sleep
    json_text = open("objects.json", "r").read()
    json_data = json.loads(json_text)
    object_info = {}
    for item in json_data:
        new_obj_data = get_data(item['id'])
        object_info[item['name']] = new_obj_data

        dump_string = json.dumps(object_info, ensure_ascii=False)
        with open("object_info.json", "w") as f:
            f.write(dump_string)
        sleep(5)

    print(stdevs)


if __name__ == "__main__":
    main()
