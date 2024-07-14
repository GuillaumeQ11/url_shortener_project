import pytest
from fastapi.testclient import TestClient
from main import app
from main import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from main import URL

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_url():
    response = client.post("/url", data={"url": "https://www.google.com"})
    assert response.status_code == 200

def test_invalid_typo_url():
    response = client.post("/url", data={"url": "not_a_url"})
    assert response.status_code == 400

def test_invalid_not_reachable_url():
    response = client.post("/url", data={"url": "https://about.gitlabo.com"})
    assert response.status_code == 404
