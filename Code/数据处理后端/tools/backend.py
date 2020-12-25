#coding=utf-8
import pandas as pd
import numpy as np
import os
import config
import json
import copy
import time
from datetime import datetime
from scipy.fftpack import fft,ifft
# from app import app
from flask import send_file


def getFileNames():
    '''
        return fileList
    '''
    file_list = []
    for file in os.listdir(config.data_path):
        file_list.append(file)
    return json.dumps(file_list)

def getLayout():
    '''
        return layout
    '''
    layout = {
        'right1': config.select_items1,
        'right2': config.select_items2,
        'bottom': config.bottom
    }
    return json.dumps(layout)

def preProcessCsv(fdir, fname):
    """
    docstring
    """
    df = pd.read_csv(os.path.join(fdir, fname), delimiter=";",skiprows=[0,1,2,3])


    print(1)
    df['time'] = df['Timestamp']
    for j in range(5):
        i = str(j)
        df['Logging:Logging.AxisData[{}].ActualTorque'.format(i)] = df.apply(lambda x:x['Logging:Logging.AxisData[{}].ActualTorque'.format(i)].replace(',','.'), axis =1)
        df['Logging:Logging.AxisData[{}].ActualAxisCurrent'.format(i)] = df.apply(lambda x:x['Logging:Logging.AxisData[{}].ActualAxisCurrent'.format(i)].replace(',','.'), axis =1)
        df['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i)] = df.apply(lambda x:x['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i)].replace(',','.'), axis =1)
        df['Logging:Logging.AxisData[{}].ContTotalPowerServo'.format(i)] = df.apply(lambda x:x['Logging:Logging.AxisData[{}].ContTotalPowerServo'.format(i)].replace(',','.'), axis =1)
        df['Logging:Logging.AxisData[{}].OutputPowerServo'.format(i)] = df.apply(lambda x:x['Logging:Logging.AxisData[{}].OutputPowerServo'.format(i)].replace(',','.'), axis =1)
        df['Logging:Logging.AxisData[{}].UDCBusAct'.format(i)] = df.apply(lambda x:x['Logging:Logging.AxisData[{}].UDCBusAct'.format(i)].replace(',','.'), axis =1)
    for j in range(5):
        i = str(j)
        df['Logging:Logging.AxisData[{}].ActualTorque'.format(i)] = pd.Series(df['Logging:Logging.AxisData[{}].ActualTorque'.format(i)],dtype=float)
        df['Logging:Logging.AxisData[{}].ActualAxisCurrent'.format(i)] = pd.Series(df['Logging:Logging.AxisData[{}].ActualAxisCurrent'.format(i)],dtype=float)
        df['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i)] = pd.Series(df['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i)],dtype=float)
        df['Logging:Logging.AxisData[{}].ContTotalPowerServo'.format(i)] = pd.Series(df['Logging:Logging.AxisData[{}].ContTotalPowerServo'.format(i)],dtype=float)
        df['Logging:Logging.AxisData[{}].OutputPowerServo'.format(i)] = pd.Series(df['Logging:Logging.AxisData[{}].OutputPowerServo'.format(i)],dtype=float)
        df['Logging:Logging.AxisData[{}].UDCBusAct'.format(i)] = pd.Series(df['Logging:Logging.AxisData[{}].UDCBusAct'.format(i)],dtype=float)
    
    df = df[df['Logging:Logging.AxisData[4].ActualTorque'] != 0] # 12641

    df['lasttime'] = df['time'].shift().fillna(method = 'bfill')
    df['deltaTime'] = df.apply(lambda x: (datetime.strptime(x['time'], "%Y %m %d %H:%M:%S:%f") - datetime.strptime(x['lasttime'], "%Y %m %d %H:%M:%S:%f")).microseconds / 1000, axis = 1 )
    
    df.to_csv(os.path.join(config.process_data_path, fname),index=False)

# def assertSignal(yawing_part):
#     '''
#         assert whether this df is bad, if bad return False
#     '''

#     v0fft = fft(yawing_part['Axis0Velocity'])
#     t0fft = fft(yawing_part['Axis0Torque'])

#     if (np.max(np.abs(v0fft)) > 1000) & (len(t0fft) < 5000):
#         return True
#     else:
#         return False

def assertSignal(df):

    v = np.array(df['Axis0Velocity'])
    v_max = abs(v).max()
    length_neg = np.where((v < (-0.8 * v_max))==True)[0].shape[0]
    length_pos = np.where((v > (0.8 * v_max))==True)[0].shape[0]
    length_max = max(length_neg, length_pos)

    t = np.array(df['Axis0Torque'])
    t_max = abs(t).max()
    t_mean = abs(t).mean()
    
    num0 = 0
    num1 = 0
    num2 = 0
    num3 = 0 
    num4 = 0

    
    if t_max > 60:
        flag = False
        num0 = (np.array(df['Axis0Error']) != 0).sum()
        num1 = (np.array(df['Axis1Error']) != 0).sum()
        num2 = (np.array(df['Axis2Error']) != 0).sum()
        num3 = (np.array(df['Axis3Error']) != 0).sum()
        num4 = (np.array(df['Axis4Error']) != 0).sum()
        
    
    else:
        if length_max > 200:
            if t_max > 1.3 * t_mean:
                flag = True
            else:
                flag = False
        else:
            flag = False

    return flag, num0, num1, num2, num3, num4


def LockFile(filename):
    lockfilepath = "./{}.txt".format(filename)
    if os.path.exists(lockfilepath):
        while os.path.exists(lockfilepath):
            time.sleep(0.3)
    lockfile = open(lockfilepath,"w+")


def UnlockFile(filename):
    lockfilepath = "./{}.txt".format(filename)
    if os.path.exists(lockfilepath):
        os.remove(lockfilepath)


def returnData(filename):
    '''
        return standard file information
    '''
    LockFile(filename)


    pure_file = filename.split('.')[0] + '.json'
    if os.path.exists(os.path.join(config.backend_json,pure_file)):
       fetched_data = json.load(open(os.path.join(config.backend_json,pure_file), encoding='utf-8'))
    #    fetched_data = json.load(open(os.path.join(config.backend_json,pure_file))) # python2
       UnlockFile(filename)
       return json.dumps(fetched_data)

    # if not exist processed json
    processed_csv_path = os.path.join(config.process_data_path, filename)
    if not os.path.exists(processed_csv_path):
        preProcessCsv(config.data_path, filename)

    df = pd.read_csv(processed_csv_path)



    timeList = df[(df.deltaTime == 0) | (df.deltaTime>= 30)].index.tolist()
    fetched_data = {}
    print(timeList)
    timeListCopy = [0]
    for time in timeList:
        if (time - timeListCopy[-1]) < 1000:
            continue
        else:
            timeListCopy.append(time)
    for i in range(len(timeListCopy)):
        begin = timeListCopy[i]
        if i == len(timeListCopy) - 1 :
            end = len(df)
        else:
            end = timeListCopy[i+1]

        tmp_df = df[begin:end]
        
        yawing_part = {}
        for num in range(5):
            yawing_part['Axis{}Torque'.format(str(num))] = tmp_df['Logging:Logging.AxisData[{}].ActualTorque'.format(str(num))].tolist()
            yawing_part['Axis{}Velocity'.format(str(num))] = tmp_df['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(str(num))].tolist()
            yawing_part['Axis{}Error'.format(str(num))] = tmp_df['Logging:Logging.AxisData[{}].ErrorNumber'.format(str(num))].tolist()
        yawing_part['Timestamp'] = tmp_df['Timestamp'].tolist()
        yawing_part['YawLeft'] = tmp_df['Logging:Logging.YawLeft'].tolist()
        yawing_part['YawRight'] = tmp_df['Logging:Logging.YawRight'].tolist()
        yawing_part['Move'] = tmp_df['Logging:Logging.Move'].tolist()
        yawing_part['YawBrakeReleased'] = tmp_df['Logging:Logging.YawBrakeReleased'].tolist()
        yawing_part['MotorBrakeReleased'] = tmp_df['Logging:Logging.MotorBrakeReleased'].tolist()
        yawing_part['YawBrakeRelease'] = tmp_df['Logging:Logging.YawBrakeRelease'].tolist()
        yawing_part['MotorBrakesRelease'] = tmp_df['Logging:Logging.MotorBrakesRelease'].tolist()

        if abs(np.array(yawing_part['Axis0Torque']).mean()) > 60:
            continue

        whether_bad,  num0, num1, num2, num3, num4 = assertSignal(yawing_part)

        print(num0, num1, num2, num3, num4)

        yawing_part['num0'] = float(num0)
        yawing_part['num1'] = float(num1)
        yawing_part['num2'] = float(num2)
        yawing_part['num3'] = float(num3)
        yawing_part['num4'] = float(num4)
        
        flag = '' if whether_bad else '_bad'
        fetched_data['yawing{}{}'.format(str(i), flag)] = yawing_part
    
    if not os.path.exists(config.backend_json):
        os.makedirs(config.backend_json)
    with open(os.path.join(config.backend_json,pure_file),'w') as file_obj:
        json.dump(fetched_data,file_obj)

    UnlockFile(filename)
    return json.dumps(fetched_data)



if __name__ == "__main__":
    returnData('Datalog_2019_12_10_15_07_25.csv')