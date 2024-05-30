from fastapi import FastAPI
import queue
import uvicorn
from typing import Any
import socket

from mixmancer.config.data_models import DataModel

app = FastAPI()
data_queue: queue.Queue[Any] = queue.Queue()


@app.post("/send-data")
def send_data(data: DataModel):
    data_dict = data.__dict__
    data_list = list(data_dict.values())
    data_queue.put(data_list)
    return {"status": "success", "data": data_list}


def start_fastapi():
    host_ip = socket.gethostbyname(socket.gethostname())
    print(f"FastAPI server running at http://{host_ip}:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
