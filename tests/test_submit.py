from unittest.mock import patch
from fastapi.testclient import TestClient
from sqr import app
import json
import random
import string

client = TestClient(app)

def test_submit_no_qr():
    with open("./assets/logo.png", "rb") as f:
        image = f.read()

    with patch('sqr.scan_qr', return_value=None) as mock_scan_qr:
        response = client.post(
            "/api/submit",
            files={"image": ("logo.png", image, "image/png")},
            data={
                "backgroundColor": "rgb(255, 255, 255)",
                "foregroundColor": "rgb(0, 0, 0)",
                "logoText": "Test Logo",
                "relevantDate": "2023-05-10T15:04:05+01:00",
                "expirationDate": "2023-06-10T15:04:05+01:00"
            }
        )

    assert response.status_code == 400
    assert response.json() == {"detail": "Should be exactly one QR"}

def test_submit_endpoint_fuzzing():
    for _ in range(100):
        data = {random_string(): random_string() for _ in range(5)}
        response = client.post("/api/submit", data=json.dumps(data))
        assert response.status_code != 500

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
