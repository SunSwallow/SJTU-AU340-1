#coding=utf-8
from flask import Flask,make_response
from flask import request
from flask_cors import CORS
from flask import current_app
import json
import config
import tools.backend as tbk

app = Flask(__name__, static_folder='./processData',static_url_path='')
CORS(app, supports_credentials=True)
app.config['JSON_AS_ASCII'] = False
with app.app_context():  # Create an :class:`~flask.ctx.AppContext`.
    a = current_app
    d = current_app.config['DEBUG']

app = Flask(__name__)
 
@app.route('/filename',methods=['GET'])
def filename():
    return tbk.getFileNames()

@app.route('/layout',methods=['GET'])
def layout():
    return tbk.getLayout()

@app.route('/fetch',methods=['POST'])
def fetch():
    # try:
    if request.method == 'POST':
        filename = request.form['filename']
        # print(filename)
        file = request.files.get('filed1')

        file.save(config.data_path + '/' +filename)
        # print(filename)
        # print(filename)
        return tbk.returnData(filename)
    # except:
        # return json.dumps([False])
 
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=4396,debug=True)