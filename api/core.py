import jwt
import json
import pyodbc 
import datetime
import urllib.parse
from flask import Flask,request,jsonify,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)


params = urllib.parse.quote_plus("DRIVER={FreeTDS};SERVER=carelinq.ck0enzapcdht.us-west-1.rds.amazonaws.com;PORT=1433;UID=admin;PWD=admin_carelinq;DATABASE=carelinq")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params


@app.route("/weight_scale",methods = ["POST"])
def weight_scale():
    input_data = request.get_json(force=True)
    imei = input_data["imei"]
    ts = input_data["ts"]
    batteryVoltage = input_data["batteryVoltage"]
    signalStrength = input_data["signalStrength"]
    rssi = input_data["rssi"]
    deviceId = input_data["deviceId"]
    try:
        unit = input_data["values"]["unit"]
        tare = input_data["values"]["tare"]
        weight = input_data["values"]["weight"]
        flag = 0

    except:
        unit = None
        tare = None
        weight = None
        flag = 1
    details = json.dumps(input_data)
    print(details,flush=True)
    if(flag==0):
        sql = "INSERT INTO BT005(imei,ts,batteryVoltage,signalStrength,unit,tare,weight,rssi,deviceId) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(imei,ts,batteryVoltage,signalStrength,unit,tare,weight,rssi,deviceId)
    else:
        sql = "INSERT INTO BT005(imei,ts,batteryVoltage,signalStrength,rssi,deviceId) VALUES('%s','%s','%s','%s','%s','%s');"%(imei,ts,batteryVoltage,signalStrength,rssi,deviceId)
    result = db.engine.execute(sql) 

    db.session.commit()
    return details

@app.route("/bp_monitor",methods = ["POST"])
def bp_monitor():
    input_data = request.get_json(force=True)
    imei = input_data["imei"]
    ts = input_data["ts"]
    batteryVoltage = input_data["batteryVoltage"]
    signalStrength = input_data["signalStrength"]

    try:
        systolic = input_data["values"]["systolic"]
        diastolic = input_data["values"]["diastolic"]
        pulse = input_data["values"]["pulse"]
        unit = input_data["values"]["unit"]
        irregular = input_data["values"]["irregular"]
        flag = 0
    except:
        systolic = None
        diastolic = None
        pulse = None
        unit = None
        irregular = None
        flag = 1
    if(flag==0):
        sql = "INSERT INTO BT105(imei,ts,batteryVoltage,signalStrength,systolic,diastolic,pulse,unit,irregular) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(imei,ts,batteryVoltage,signalStrength,systolic,diastolic,pulse,unit,irregular)
    else:
        sql = "INSERT INTO BT005(imei,ts,batteryVoltage,signalStrength) VALUES('%s','%s','%s','%s');"%(imei,ts,batteryVoltage,signalStrength)
    details = json.dumps(input_data)
    print(details,flush=True)
    
    result = db.engine.execute(sql) 
    db.session.commit()
    return details




if __name__ == '__main__':
    app.run(host="0.0.0.0",port="80",debug=True)
    #app.run(debug=True)
