import validators
import requests
import os
import uuid
from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./url.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    slug = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

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
def create_url(url: str = Form(...), db: Session = Depends(get_db)):
    if not validators.url(url):
        raise_bad_request(message="L'URL saisie est incorrecte")
    if is_url_accessible(url):
       slug = generate_unique_slug(db)

       db_url = URL(original_url=url, slug=slug)
       db.add(db_url)
       db.commit()
       db.refresh(db_url)
       db.close()

       return {"short_url": f"http://localhost:8000/{slug}"}
    else:
        raise HTTPException(status_code=404, detail="L'URL n'est pas accessible")

@app.get("/{slug}")
def redirect_url(slug: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.slug == slug).first()
    if db_url:
        return RedirectResponse(url=db_url.original_url)
    else:
        raise raise_bad_request("URL raccourcie non trouvée")

def generate_unique_slug(db: Session):
    while True:
        slug = str(uuid.uuid4())[:8]
        existing_url = db.query(URL).filter(URL.slug == slug).first()
        db.close()
        if not existing_url:
            return slug