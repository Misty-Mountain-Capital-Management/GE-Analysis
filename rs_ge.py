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

def peak(array):
    #this prints max
    maxnum = -999999
    for i in range(1,len(array)):
        if(int(array[i]) > int(maxnum)):
            maxnum = array[i]
    print("The maximum price over the past 180 days is: " + maxnum)
    return maxnum

def get_prices(id):
    item_json = json.loads(requests.get(graphstring % id).text)['daily']
    stamps = []
    for s in item_json.keys():
        stamps.append((s, item_json[s]))
    
    stamps = sorted(stamps, key=lambda stamp: int(stamp[0])) # Sort the list by its date in ascending order.

    prices = [s[1] for s in stamps] # get prices from stamps

    print("The minimum price over the past 180 days for %s is: %s" % (str(id), str(min(prices))))
    average = int(sum(prices) / len(prices))
    print("The average price is: " + str(average))
    return prices

def math(PriceArray, Average, id):
    ############ calc average
    average = []
    test = 0
    for x in range(1,len(PriceArray)):
        test += int(PriceArray[x-1])
        average.append(test/x)
        
    ############

    

    #Graphing...
    plt.plot(PriceArray)
    plt.plot(average)
    plt.ylabel('Price of: ' + name(id) + ' (' + description(id) + ')')
    plt.xlabel("Time in days (previous 180 days)")
    plt.show()
    return 0

def get_stdev(id):
    item_data = get_prices(id)
    stdev = np.std(item_data)
    print("The standard deviation is %s." % str(stdev))
    return stdev
    

def getrend(id):
    print(str(json.loads(info(id))['item']))

def main():
    from time import sleep
    json_text = open("objects.json", "r").read()
    json_data = json.loads(json_text)
    stdevs = {}
    for item in json_data:
        new_stdev = get_stdev(item['id'])
        stdevs[item['name']] = new_stdev
        sleep(5)

    dump_string = json.dumps(stdevs, ensure_ascii=False)
    with open("stdevs.json", "r") as f:
        f.write(dump_string)

    print(stdevs)
        

if __name__ == "__main__":
    main()
