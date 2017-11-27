from flask import Flask, session, render_template, request, redirect, flash,  url_for
import urllib2
import json
import requests

app = Flask(__name__)



@app.route('/', methods = ['GET','POST'])
def root():
                          
    r=requests.get("http://www.bungie.net/Platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/ /", headers=HEADERS);
    dict=r.json()#Automaticaly runs json.load() onto r, whish is json formatted text
    items=dict
   # for each in items:
     #   del each['entityType']
     #   del each['hash']
     #   del each['weight']
    dispop=[]
   # for each in items:
    #    dispop.append(each['displayProperties'])
  

    return render_template("armory.html", list=items)

if __name__ == "__main__":
    app.debug = True
    app.run()
