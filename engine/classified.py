from flask import Flask
from flask import Flask, render_template
from flask import Flask, request, jsonify 
import datetime
import time
import json
from naivebayes import trainClass, predictClass

app = Flask(__name__)

@app.route('/problemclass', methods=['GET','POST'])
def classification():
    text = request.args.get("text")
    cls,conf = predictClass(text) 
    if cls is not None and conf is not None:
        result='classification:' +str(cls[0])+' & confidence:'+str(conf)
        return (result)
    else:
        return ("Failed to get the result")

@app.route('/train', methods=['GET','POST'])
def train():
    trainClass()
    return ("Successfully Trained")

if __name__ == '__main__':
   app.run(debug = True,host = '0.0.0.0',port = 8500)
