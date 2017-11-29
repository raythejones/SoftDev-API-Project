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
    info['desc']= dict['longDescription']
    return info
    

def searchYoutube(name):
     r=requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+name+'&type=video&videoCaption=closedCaption&key='+keys['Youtube'])
     dict=r.json()
     items=dict['items']
     links = []                    
     video=items[0]['id']['videoId']
     links=[]
     link='https://www.youtube.com/embed/'+video
     links.append(link)
     video=items[1]['id']['videoId']
     link='https://www.youtube.com/embed/'+video
     links.append(link)
     video=items[2]['id']['videoId']
     link='https://www.youtube.com/embed/'+video
     links.append(link)
     return links
     
