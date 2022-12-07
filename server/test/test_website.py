from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_website_list():
    with client:
        response = client.get("/websites")
        assert response.status_code == 200


def test_website_ws_indalid_json():
    with client.websocket_connect("/websites") as websocket:
        # Json valid
        websocket.send_text('Hello WebSocket')
        data = websocket.receive_json()
        assert data['status'] == 'error' and data['message'] == 'Invalid JSON'


def test_website_ws_invalid_data():
    with client.websocket_connect("/websites") as websocket:
        # Json valid
        websocket.send_text('{"name": "https://www.google.com"}')
        data = websocket.receive_json()
        assert data['status'] == 'error' and data['message'] == 'Invalid data'
        
        
def test_website_ws_valid_data():
    with client.websocket_connect("/websites") as websocket:
        # Json valid
        websocket.send_text('{"name": "https://www.google.com", "id": "google.com"}')
        data = websocket.receive_json()
        assert data['status'] == 'ok'
        data = websocket.receive_json()
        assert data['name'] == 'https://www.google.com' and data['id'] == 'google.com'