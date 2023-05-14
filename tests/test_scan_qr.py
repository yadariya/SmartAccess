import os
import pytest
from sqr import scan_qr


def test_scan_qr_valid():
    with open("./assets/valid_qr_code.png", "rb") as f:
        image = f.read()
    result = scan_qr(image)
    assert result == "valid qr code"


def test_scan_qr_invalid():
    with open("./assets/invalid_qr_code.png", "rb") as f:
        image = f.read()
    result = scan_qr(image)
    assert result == ''


def test_scan_qr_no_qr():
    with open("./assets/logo.png", "rb") as f:
        image = f.read()
    result = scan_qr(image)
    assert result is None


def test_scan_qr_fuzzing():
    for _ in range(1000):
        input = os.urandom(1024)
        try:
            result = scan_qr(input)
            if result is None:
                # Skip this iteration if imdecode() returned None
                continue
        except Exception as e:
            pytest.fail(f"scan_qr() crashed with exception: {e}")
