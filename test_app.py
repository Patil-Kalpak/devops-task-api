import requests

BASE_URL = "https://task-app-13067289558.asia-south1.run.app"

def test_home():
    r = requests.get(BASE_URL + "/")
    assert r.status_code == 200

def test_tasks():
    r = requests.get(BASE_URL + "/tasks")
    assert r.status_code == 200
