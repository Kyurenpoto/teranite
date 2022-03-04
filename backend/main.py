import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

app = FastAPI()

app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True), name="static")
