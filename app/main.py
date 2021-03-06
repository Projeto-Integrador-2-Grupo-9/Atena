from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import DESCENDING
from .db import database

collection = database["Logs"]


class Current_Position(BaseModel):
    lat: float
    lng: float


class Log(BaseModel):
    device: str
    current_position: Current_Position
    timestamp: str


class Device(BaseModel):
    mac_address: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Connection": "successful!"}


@app.post("/log")
def post_log(log: Log):

    collection.insert_one(log.dict())

    return {
        "status": "sucess",
        "log": log
    }


@app.get("/logs")
def get_logs(device: Device, limit: int = 10):

    query = {"device": device.mac_address}

    result = collection.find(query, {'_id': 0}).limit(
        limit).sort('timestamp', DESCENDING)

    return {
        "status": "sucess",
        "logs": list(result)
    }


@app.get("/last_log")
def get_last_log(device: Device):
    query = {"device": device.mac_address}

    result = collection.find(query, {'_id': 0}).limit(
        1).sort('timestamp', DESCENDING)

    return {
        "status": "sucess",
        "logs": list(result)
    }
