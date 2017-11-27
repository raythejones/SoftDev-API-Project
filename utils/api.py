import requests
import csv

with open('keys.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['first_name'], row['last_name'])

def searchWalmart(query):
    r=requests.get('http://api.walmartlabs.com/v1/search?apiKey='+keys['Walmart']+'&query='+query+'&numItems=25')
    dict=r.json()
    items=dict['items']
    realitems=[]
    for each in items:
        if each['marketplace'] =='false':
            realitems.append(each)
    return realitems

def showYoutube(query):
     r=requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+query+'&type=video&videoCaption=closedCaption&key='+keys['Youtube'])
     dict=r.json()
     items=dict['items']
     video=items[0]['videoId']
     link='https://www.youtube.com/watch?v='+video
     return link
     
