# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import os 
import shutil
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
import random
import json
import time
import requests


ORIGIN_DATA_FLODER = './data'
ALLOWED_EXTENSIONS = set('.csv')
UPLOAD_PATH = './upload/'




app = Flask(__name__)
filenames = None
json_raw_files = {}

def get_index():
    return render_template('index.html')

def get_json():
    global filenames
    with open('data/Datalog_2019_12_10_15_07_25.json') as f:
        data = json.load(f)
    return data

    r = requests.get(host + '/filename')
    filenames = json.loads(r.text)
    r = requests.post(host + '/fetch', data={'filename': filenames[0]})
    json_raw_files[0] = r.text

    return r.text


@app.route("/data")
def send_json():
    data = get_json()
    return data


@app.route('/')
def index():
    return get_index()



@app.route('/upload/', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file_up = request.files['file']
        filename = file_up.filename
        extension = filename.split('.')[-1]
        
        if extension == 'csv':
            file_up.save(os.path.join(UPLOAD_PATH, filename))
            return {"status":200}
        else:
            return {"status":"文件扩展名错误！"}

@app.route('/clear')
@app.route('/clear/')
def clear_files():
    if os.path.exists(UPLOAD_PATH):
        shutil.rmtree(UPLOAD_PATH)
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)
    return get_index()


@app.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):
    # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.jpg
    return app.send_static_file(filepath)  






if __name__ == '__main__':
    app.run(debug=True, port=9584)