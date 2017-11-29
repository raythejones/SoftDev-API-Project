import requests
import csv
keys={}
with open('data/keys.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
          print row
          keys[row['Name']] = row['Key']

def searchWalmart(query):
    r=requests.get('http://api.walmartlabs.com/v1/search?apiKey='+keys['Walmart']+'&query='+query+'&numItems=25')
    dict=r.json()
    items=dict['items']
    realitems=[]
    for each in items:
         if each['stock'] =="Available":
              realitems.append(each)
    return realitems


def productInfo(dict):
    info={}
    info['name'] = dict['name']
    info['image']= dict['largeImage']
    info['link'] = dict['productUrl']
    info['desc']= dict['shortDescription']
    return info
    

def searchYoutube(name):
     r=requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+query+'&type=video&videoCaption=closedCaption&key='+keys['Youtube'])
     dict=r.json()
     items=dict['items']
     video=items[0]['videoId']
     links=[]
     link='https://www.youtube.com/embed/'+video
     links.append(link)
     video=items[1]['videoId']
     link='https://www.youtube.com/embed/'+video
     links.append(link)
     video=items[2]['videoId']
     link='https://www.youtube.com/embed/'+video
     links.append(link)
     return links
     
