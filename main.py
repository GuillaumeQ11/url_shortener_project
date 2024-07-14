from fastapi import FastAPI, HTTPException, Form
import validators
import requests
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r") as file:
        html_content = file.read()
        return HTMLResponse(content=html_content)

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def is_url_accessible(url: str) -> bool:
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False

@app.post("/url")
def create_url(url: str = Form(...)):
    if not validators.url(url):
        raise_bad_request(message="L'URL saisie est incorrecte")
    if is_url_accessible(url):
        return "L'URL est accessible !"
    else:
        return "L'url n'est pas accessible"
