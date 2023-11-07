from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import os


pattern = r'[\u4e00-\u9faf]+'

app = FastAPI()
class RequestData(BaseModel):
    context: str
    title: str
    quizSize: str

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/normal/")
def process_context(request_data: RequestData):
    title=request_data.title.replace(' ','　')
    with open("context.txt", "w") as file:
        file.write(request_data.context)
    if request_data.quizSize!="":
        os.system(f'python3 core.py -n {request_data.quizSize} -t {title}')
    else:
        os.system(f'python3 core.py -n {"漢字書き取りテスト"} -t {title}')
    return {
        "log": "ok"
    }
@app.get("/get_file/{filename:path}")
async def get_file(filename: str):
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