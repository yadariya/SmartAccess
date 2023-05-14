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
