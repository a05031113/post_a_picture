import uvicorn
import boto3
import random
from botocore.client import Config
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import *
from dotenv import load_dotenv
from py.model import *
import os
load_dotenv()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/upload/url")
async def upload_url():
    now = datetime.now()
    time_string = now.strftime("%Y%m%d%H%M%S")
    file_name = time_string + str(random.randint(100, 999))
    return r2().get_put_url(file_name)


@app.post("/api/upload/success")
async def upload_success(data: Data):
    msg = data.msg
    imgName = data.imgName
    imgURL = "https://d2clms9ecxwnmg.cloudfront.net/" + imgName
    rds().insert(msg, imgURL)
    return


@app.get("/api/messages")
async def get_message():
    results = rds().select()
    output = {}
    output["data"] = results
    return output


@app.get("/api/message/new")
async def get_new_message():
    results = rds().select_new()
    output = {}
    output["data"] = results
    return output


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
