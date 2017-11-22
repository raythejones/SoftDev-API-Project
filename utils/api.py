import requests
import csv

with open('keys.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['first_name'], row['last_name'])

def searchWalmart(query):
    r=(requests.get('http://api.walmartlabs.com/v1/search?apiKey='+keys['Walmart']+'&query='+query+'&numItems=25'))
    dict=r.json()
    items=dict['items']
    realitems=[]
    for each in items:
        if each['marketplace'] =='false':
            realitems.append(each)
    return realitems
    
