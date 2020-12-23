# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import os 
import shutil
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
import random
import json
import time


ORIGIN_DATA_FLODER = './data'
ALLOWED_EXTENSIONS = set('.csv')
UPLOAD_PATH = './upload/'




app = Flask(__name__)

def get_index():
    return render_template('index.html')

def get_json():
    with open('../project/backend_json/Datalog_2019_12_10_15_07_25.json') as f:
        data = json.load(f)
    
    return data


def line_base():
    '''
    ['Axis0Torque', 'Axis0Velocity', 'Axis1Torque', 'Axis1Velocity', 'Axis2Torque', 'Axis2Velocity', 'Axis3Torque', 'Axis3Velocity', 'Axis4Torque', 'Axis4Velocity', 'Timestamp', 'YawLeft', 'YawRight', 'Move', 'YawBrakeReleased', 'MotorBrakeReleased', 'YawBrakeRelease', 'MotorBrakesRelease']
    '''

    with open('../project/backend_json/Datalog_2019_12_10_15_07_25.json') as f:
        data = json.load(f)
    yawing0 = data['yawing0_bad']
    l = (
        Line()
            .add_xaxis(yawing0['Timestamp'])
            .add_yaxis('Velocity',{"1":yawing0['Axis0Velocity'], '2':yawing0['Axis1Velocity']})
            # .add_yaxis('Axis1Velocity',yawing0['Axis1Velocity'])
            .set_global_opts(title_opts=opts.TitleOpts(title="FUCKALL", subtitle=""),
                            xaxis_opts=opts.AxisOpts(type_='time'))
    )

    return l


@app.route("/barChart")
def get_bar_chart():
    c = line_base()
    return c.dump_options_with_quotes()

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
        print(extension)
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




if __name__ == '__main__':
    app.run(debug=True, port=9584)