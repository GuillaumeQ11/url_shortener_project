import validators
import requests
import os
import uuid
from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./url.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    """
    Defines a SQLAlchemy table 'urls' with columns for ID, original URL, and slug.
    """

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    slug = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    '''Get the db session'''

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/{slug}")
def redirect_url(slug: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.slug == slug).first()
    if db_url:
        return RedirectResponse(url=db_url.original_url)
    else:
        raise raise_bad_request("URL raccourcie non trouvée")
    
def raise_bad_request(message) -> HTTPException:
    '''Raise an HTTPException with status code 400 and the provided message'''
    raise HTTPException(status_code=400, detail=message)

def is_url_accessible(url: str) -> bool:
    ''' 
    Check if the url is valid, firstly with typo validation, then trying to access to the url
    '''
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    
def generate_unique_slug(db: Session) -> str:
    """
    Generate a unique 8-character slug using UUID.
    Also checks that the slug does not already exist in the database.
    """

    while True:
        slug = str(uuid.uuid4())[:8]
        existing_url = db.query(URL).filter(URL.slug == slug).first()
        db.close()
        if not existing_url:
            return slug
        
@app.get("/")
def read_root():
    """
    Endpoint to read and return the content of 'index.html' file as HTML response.
    """

    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r") as file:
        html_content = file.read()
        return HTMLResponse(content=html_content)

@app.post("/url")
def create_url(url: str = Form(...), slug: str = Form(None), db: Session = Depends(get_db)):
    """
    Endpoint to shorten a long URL. Validates the URL first, checks its accessibility,
    generates a unique slug, saves the URL and slug in the database.
    Returns a dictionary containing the shortened URL.
    """

    if not validators.url(url):
        raise_bad_request(message="L'URL saisie est incorrecte")
    if is_url_accessible(url):
       if slug:
           existing_url = db.query(URL).filter(URL.slug == slug).first()
           if existing_url:
               raise raise_bad_request("Le slug fourni est déjà utilisé.")
       else:
           slug = generate_unique_slug(db)

       db_url = URL(original_url=url, slug=slug)
       db.add(db_url)
       db.commit()
       db.refresh(db_url)
       db.close()

       return {"short_url": f"http://localhost:8000/{slug}"}
    else:
        raise HTTPException(status_code=404, detail="L'URL n'est pas accessible")