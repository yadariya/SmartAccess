from sqr import create_pkpass, BarcodeFormat

def test_create_pkpass_basic():
    pkpass = create_pkpass(BarcodeFormat.QR, "https://example.com/qr")
    assert pkpass is not None

def test_create_pkpass_with_colors():
    pkpass = create_pkpass(
        BarcodeFormat.QR,
        "https://example.com/qr",
        backgroundColor="rgb(0, 0, 255)",
        foregroundColor="rgb(255, 255, 255)"
    )
    assert pkpass is not None

def test_create_pkpass_with_logo_text():
    pkpass = create_pkpass(
        BarcodeFormat.QR,
        "https://example.com/qr",
        logoText="Test Logo"
    )
    assert pkpass is not None

def test_create_pkpass_with_dates():
    pkpass = create_pkpass(
        BarcodeFormat.QR,
        "https://example.com/qr",
        relevantDate="2023-05-10T15:04:05+01:00",
        expirationDate="2023-06-10T15:04:05+01:00"
    )
    assert pkpass is not None