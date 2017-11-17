from flask import Flask, session, render_template, request, redirect, flash,  url_for
import urllib2
import json
import requests

HEADERS = {"X-API-Key":'72504fb40d484be59b89d903b9d4ed08'}
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def root():
    u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=RvEhHA59fuin9WI0oK3RxK7Te31EcneKjEvC0VAp")

    dict = json.loads(u.read())
    url = dict['url']
    exp = dict['explanation']
    return render_template("index.html", link=url, desc=exp)

@app.route('/armory', methods = ['GET','POST'])
def armory():
    if request.args.get('search')=='Submit':
        r=(requests.get("http://www.bungie.net/Platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/" + request.args.get('lookup'), headers=HEADERS))
    else:                         
        r=requests.get("http://www.bungie.net/Platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/ /", headers=HEADERS);
    dict=r.json()#Automaticaly runs json.load() onto r, whish is json formatted text
    items=dict['Response']['results']['results']
    for each in items:
        del each['entityType']
        del each['hash']
        del each['weight']
    dispop=[]
    for each in items:
        dispop.append(each['displayProperties'])
  

    return render_template("armory.html", list=dispop)

if __name__ == "__main__":
    app.debug = True
    app.run()
