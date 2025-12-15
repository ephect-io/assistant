from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

DATA_PATH = "../../data/train.jsonl"

@app.get("/data")
def read_data():
    data = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return JSONResponse(content=data)
