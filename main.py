# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import os 
import shutil
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
import random

ORIGIN_DATA_FLODER = './data'
ALLOWED_EXTENSIONS = set('.csv')
UPLOAD_PATH = './upload/'




app = Flask(__name__)

def get_index():
    return render_template('index.html')

def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [random.randint(10, 100) for _ in range(6)])
            .add_yaxis("商家B", [random.randint(10, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="", subtitle=""))
    )
    return c


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()



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