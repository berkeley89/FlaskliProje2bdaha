from flask import request
from flask import Flask, render_template
from jsonschema import validate, ValidationError
#from jsonschema.exceptions import ValidationError
from datetime import datetime#,timedelta
from os import path

import uuid
import json
import os
import time

app = Flask(__name__)

schema = {
    "type" : "object",
    "properties" : {
        "title" : {"title" : "string"},
        "message": {"message" : "string"},
    },
}

with open('todo.json', 'r') as file:
    words = json.load(file)


@app.route('/',methods=['POST','GET'])
def hillo():
    data = gettodo()
    messages=[]
    for k,v in data.items():
        titles=[]
        titles.append(v.get('title'))
        titles.append(v.get('message'))
        titles.append(k)
        messages.append(titles)
    return render_template('index.html',titles=messages,messages=messages)

@app.route('/todo',methods = ['POST'])
def todo():
    data = request.json
    try:
        validate(instance=data, schema=schema)
        print("Validation successful")

        now = datetime.now()
        dt_string = now.strftime("%B %d, %Y %H:%M:%S")

        new_id = str(uuid.uuid4())
        words[new_id] = {
            "title": data["title"],
            "message": data["message"],
            "done": False,
            "time": dt_string
        }

        with open("todo.json", 'w') as f:
            json.dump(words, f, indent=4, separators=(',', ': '))

        return {"success": True}, 200
    except ValidationError as err:
        return {"error": str(err)}, 400
@app.route('/gettodo',methods = ['GET'])
def gettodo():
    return words
@app.route('/deletetodo',methods = ['POST','GET'])
def deletetodo():
    req = request.json
    delete_id = req["delete"]

    if delete_id in words:
        del words[delete_id]

        with open("todo.json", 'w') as f:
            json.dump(words, f, indent=4, separators=(',', ': '))

        return {"success": True}, 200
    else:
        return {"error": "Item not found"}, 404
@app.route('/toUppercase',methods = ['POST'])
def hello():
  data = request.json
  try:
    validate(instance=data, schema=schema)
    print("Validation successful")
    words.update({data['word']:data['word'].upper()})
    data['word'] = data['word'].upper()
    return data
  except ValidationError as err:
    return {"message": f"fuck you bc {err.message}"}

@app.route('/getWords',methods = ['GET'])
def get_words():
  return words

if __name__ == "__main__":
  app.run(port=8080,debug=True)
