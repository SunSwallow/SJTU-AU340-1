# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask_cors import CORS
import os 
import shutil
#from pyecharts import options as opts
#from pyecharts.charts import Bar, Line, Grid
import random
import json
import time
import requests


ORIGIN_DATA_FLODER = './data'
ALLOWED_EXTENSIONS = set('.csv')
UPLOAD_PATH = './upload/'




server = Flask(__name__)
CORS(server, resources=r'/*')
filenames = None
json_raw_files = {}

init_flag = True

def get_index():
    return render_template('index.html')


def get_json():
    global filenames
    print("init_flag:", init_flag)
    if init_flag:
        with open('data/Datalog_2019_12_10_15_07_25.json') as f:
            data = json.load(f)
        return data
    else:
        tmp = os.listdir(UPLOAD_PATH)
        tmp.sort()
        filename = os.path.join(UPLOAD_PATH, tmp[0])
        f ={"filed1":open(filename, 'rb')}
        r = requests.post('http://59.78.19.21:5000' + '/fetch', data={'filename':'data-{}.csv'.format(int(time.time()))}, files=f)
        data = r.text
        with open('./static/data.json', 'w') as f:
            f.write(data)
        # clear_files()
        # print(tmp)
        # print("we get this")
        print(data[:100])   
        return data


@server.route("/data")
def send_json():
    global init_flag   
    init_flag = False
    data = get_json()
    return data

@server.route("/init_data")
def send_json_():
    data = get_json()
    return data


@server.route('/')
def index():
    return get_index()



@server.route('/upload/', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file_up = request.files['file']
        filename = file_up.filename
        extension = filename.split('.')[-1]
        
        if extension == 'csv':
            # print('File saved at :',os.path.join(UPLOAD_PATH, 'data-{}.csv'.format(time.time())))
            file_up.save(os.path.join(UPLOAD_PATH, 'data.csv'))
            return {"status":200}
        else:
            return {"status":"文件扩展名错误！"}

@server.route('/clear')
@server.route('/clear/')
def clear_files():
    if os.path.exists(UPLOAD_PATH):
        shutil.rmtree(UPLOAD_PATH)
    if not os.path.exists(UPLOAD_PATH):
        os.mkdir(UPLOAD_PATH)
    return get_index()


# @server.route("/download/<filepath>", methods=['GET'])
# def download_file(filepath):
#     # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.jpg
#     if init_flag:
#         return server.send_static_file(filepath)  






if __name__ == '__main__':
    server.run(debug=True ,host='0.0.0.0',port=80)
