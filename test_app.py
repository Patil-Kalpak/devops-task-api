import requests

BASE_URL = "http://localhost:5000"

def test_home():
    r = requests.get(BASE_URL + "/")
    assert r.status_code == 200

def test_tasks():
    r = requests.get(BASE_URL + "/tasks")
    assert r.status_code == 200
