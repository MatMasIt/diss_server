from pypresence import Presence
import time, subprocess, json
import dataModel
import handler
import threading
import asyncio
import uuid
# current_data   structure
# state -> state
# details -> details
# large_image
# small_image
# large_text
# small_text
# start
# end
# timeFilip
# lastTimeUpdate
# descriptar

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = False

current_data = dataModel.default


@app.route('/new', methods=['POST'])
def new():
    global current_data
    if (request.json == None):  # is body empty?
        res = {
            "ok": False,
            "errorId": 1,
            "error": "No json body supplied"
        }  # error -> no json body supplied
    elif "descriptar" not in request.json.keys(
    ):  # is the descriptar app present?
        res = {
            "ok": False,
            "errorId": 4,
            "error": "Descriptar not specified"
        }  # error -> descriptar does not exist
    elif request.json["descriptar"] in current_data.keys(
    ):  # is the descriptar app present?
        res = {
            "ok": False,
            "errorId": 4,
            "error": "Descriptar already used"
        }  # error -> descriptar does not exist
    else:
        temp = dict(current_data)
        temp[request.json["descriptar"]] = {}
        for key in request.json.keys():  # loop through keys
            if key not in dataModel.default["default"].keys():  # is key in the list?
                return key
                res = {"ok": False, "errorId": 8, "error": "Key invalid"}
                return jsonify(res)
            else:
                temp[request.json["descriptar"]][key] = request.json[key]
        if dataModel.is_valid_current_data_format(temp):
            temp[request.json["descriptar"]]["accessCode"] = str(uuid.uuid4())
            current_data[request.json["descriptar"]] = temp[
                request.json["descriptar"]]
            res = {"ok": True, "accessCode":temp[request.json["descriptar"]]}
        else:
            res = {"ok": False}
    return jsonify(res)


@app.route('/set/<descriptar>', methods=['POST'])
def setD(descriptar):
    global current_data  # global current data store
    if (request.json == None):  # is body empty?
        res = {
            "ok": False,
            "errorId": 1,
            "error": "No json body supplied"
        }  # error -> no json body supplied
    elif not descriptar in current_data.keys(
    ):  # is the descriptar app present?
        res = {
            "ok": False,
            "errorId": 4,
            "error": "Descriptar does not exist"
        }  # error -> descriptar does not exist
    elif "accessCode" in request.json.keys(
    ) and current_data[descriptar]["accessCode"] != request.json[
            "accessCode"]:  # is access code present and correct
        res = {
            "ok": False,
            "errorId": 5,
            "error": "Invalid access code"
        }  # error -> the access code is invalid
    else:
        temp = dict(current_data[descriptar])  # generate temporary list
        for key in request.json.keys():  # loop through keys
            if key not in dataModel.default["default"].keys():  # is key in the list?
                res = {"ok": False, "errorId": 8, "error": "Key invalid"}
                return jsonify(res)
            else:
                temp[descriptar][key] = request.json[key]
        if dataModel.is_valid_current_data_format(temp):
            current_data[descriptar] = temp[descriptar]
            res = {"ok": True}
        else:
            res = {"ok": False}
    return jsonify(res)


@app.route('/get/<descriptar>',
           methods=['POST'])  # get a rich presence by his descriptar
def get(descriptar):
    global current_data  # global current data store
    if (request.json == None):  # is body empty?
        res = {
            "ok": False,
            "errorId": 1,
            "error": "No json body supplied"
        }  # error -> no json body supplied
    else:
        if not descriptar in current_data.keys(
        ):  # is the descriptar app present?
            res = {
                "ok": False,
                "errorId": 4,
                "error": "Descriptar Does not exist"
            }  # error -> descriptar does not exist
        elif "accessCode" in request.json.keys(
        ):  # is an access code specified?
            if current_data[descriptar]["accessCode"] == request.json[
                    "accessCode"]:  # Is the access code correct?
                res = current_data[descriptar]  # send current Data
            else:
                res = {
                    "ok": False,
                    "errorId": 5,
                    "error": "Invalid access code"
                }  # error -> the access code is invalid
        elif "publicRead" in current_data[descriptar].keys() and  current_data[descriptar]["publicRead"]:  # is public read allowed?
            res = current_data[descriptar]  # pull data
            res.pop("accessCode")  # ! remove accessCode for security
        else:
            res = {
                "ok": False,
                "errorId": 6,
                "error": "Unauthorized"
            }  # error -> not authorized

    print(res)
    return jsonify(res)  # send data


@app.route('/delete/<descriptar>', methods=['DELETE'])
def delete(descriptar):
    res={"ok": True}
    if (request.json == None):  # is body empty?
        res = {
            "ok": False,
            "errorId": 1,
            "error": "No json body supplied"
        }  # error -> no json body supplied
    elif not descriptar in current_data.keys(
    ):  # is the descriptar app present?
        res = {
            "ok": False,
            "errorId": 4,
            "error": "Descriptar does not exist"
        }  # error -> descriptar does not exist
    elif "accessCode" in request.json.keys(
    ) and current_data[descriptar]["accessCode"] != request.json[
            "accessCode"]:  # is access code present and correct
        res = {
            "ok": False,
            "errorId": 5,
            "error": "Invalid access code"
        }  # error -> the access code is invalid
    else:
        current_data.pop(descriptar)
    return res


def diTH():
    global current_data
    connected = False
    while not connected:
        try:
            client_id = '778926641333796885'  # Fake ID, put your real one here
            RPC = Presence(client_id)  # Initialize the client class
            RPC.connect()  # Start the handshake loop
            connected = True
        except Exception as e:
            print(126)
            print(e)
            connected = False
        time.sleep(20)
    while True:  # The presence will stay on as long as the program is running
        try:
            print("---cdata---")
            print(current_data)
            print("---Ecdata---")
            d = handler.handle(current_data)
            print(d)
            RPC.update(state=d["state"],
                       details=d["details"],
                       large_image=d["large_image"],
                       small_image=d["small_image"],
                       large_text=d["large_text"],
                       small_text=d["small_text"],
                       start=d["start"],
                       end=d["end"])
            time.sleep(15)  # Can only update rich presence every 15 seconds
        except Exception as e:
            print(144)
            print(e)
            while not connected:
                try:
                    client_id = '778926641333796885'  # Fake ID, put your real one here
                    RPC = Presence(client_id)  # Initialize the client class
                    RPC.connect()  # Start the handshake loop
                    connected = True
                except Exception as e:
                    print(149)
                    print(e)
                    connected = False
                time.sleep(20)


def server():
    app.run(port=4020)


thread = threading.Thread(target=server)
thread.start()
diTH()
