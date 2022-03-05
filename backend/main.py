import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

templates = Jinja2Templates(directory="static")


@app.get("/{rest_of_path:path}")
async def index(request: Request, rest_of_path: str):
    print(f"rest_of_path: {rest_of_path}")
    return templates.TemplateResponse("index.html", {"request": request})
