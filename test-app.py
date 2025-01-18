import requests

def test_home():
    response = requests.get("http://localhost:5000/")
    assert response.status_code == 200
    assert response.text == "Hello, Jenkins!"