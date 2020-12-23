import json

with open('../project/backend_json/Datalog_2019_12_10_15_07_25.json') as f:
    data = json.load(f)
print(data['yawing0_bad'].keys())