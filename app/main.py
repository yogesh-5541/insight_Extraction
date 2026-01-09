from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.extractor import extract_insights
from app.database import save_to_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class TextInput(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract")
def extract_text(data: TextInput):
    result = extract_insights(data.text)
    record_id = save_to_db(result)
    return {
        "id": record_id,
        "extracted_data": result
    }
