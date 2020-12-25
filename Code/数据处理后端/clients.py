#coding=utf-8
import json
import requests

if __name__ == "__main__":
    host = 'http://127.0.0.1:4396'

    r = requests.get(host + '/filename')
    print(json.loads(r.text))

    r = requests.get(host + '/layout')
    print(json.loads(r.text))

    r = requests.post(host + '/fetch', data={
        'filename': 'Datalog_2019_12_10_15_07_25.csv'
    })
    print(json.loads(r.text))
