from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime

import os
import re
import jaconv
import random
import pykakasi


kks = pykakasi.kakasi()
pattern = r'[\u4e00-\u9faf]+'

def create_question(content):
    print(content)
    word_list = []
    kangi_list = []
    result = kks.convert(content)
    for item in result:
        word_list.append(item["orig"])
    for item in word_list:
        if re.findall(pattern,item)!=[]:
            kangi_list.append(item)
    random.shuffle(kangi_list)
    word = kangi_list[0]
    hira = kks.convert(word)[0]["hira"]
    kangi_yomi = re.sub('[一-龥]','',word)
    kangi_yomi = '**'+jaconv.hira2kata(re.sub(kangi_yomi,'',hira))+'**'
    word = re.sub(u'[ぁ-んァ-ン]','',word)
    return re.sub(word,kangi_yomi,content),word 

app = FastAPI()
class RequestData(BaseModel):
    context: str

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/normal/")
def process_context(request_data: RequestData):
    print(request_data.context)
    with open("context.txt", "w") as file:
        file.write(request_data.context)
    os.system("python3 main.py")
    return {
        "log": "ok"
    }
@app.get("/get_file/{filename:path}")
async def get_file(filename: str):
    '''任意ファイルのダウンロード'''
    current = Path()
    file_path = current / "files" / filename
    now = datetime.now()
    response = FileResponse(
        path=file_path,
        filename=f"download_{now.strftime('%Y%m%d%H%M%S')}_{filename}"
    )

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)