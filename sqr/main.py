from typing import Annotated, Optional
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, responses
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import uvicorn
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from passbook.models import Pass, Barcode, StoreCard, BarcodeFormat
import tempfile
import io
import os

app = FastAPI()

config = {
    'wwdr': os.getenv('WWDR_PEM', './certs/wwdr.pem'),
    'cert': os.getenv('CERT_PEM', './certs/certificate.pem'),
    'key': os.getenv('KEY_PEM', './certs/key.pem'),
    'pass': os.getenv('KEY_PEM_PASS'),
    'port': os.getenv('PORT', '8000')
}
assert config['pass'] is not None, "Cannot load KEY_PEM_PASS env"


def FormColor():
    return Form(
        default=None,
        description='rgb(R, G, B) where R, G, B are in [0, 255]',
        regex='rgb\(\d{1,3}, \d{1,3}, \d{1,3}\)',
        example='rgb(0, 255, 0)',
    )


def FormDateTime():
    return Form(
        default=None,
        description='https://www.w3.org/TR/NOTE-datetime',
        regex='\d\d\d\d-\d\d-\d\dT\d\d:\d\d(:\d\d)?(Z|([\+-]\d\d:\d\d))',
        examples={
            'A': '2006-01-02T15:04:05+01:00',
            'B': '2006-01-02T15:04+01:00',
            'C': '2006-01-02T15:04:05Z',
            'D': '2006-01-02T15:04Z',
        },
    )


def scan_qr(image: bytes):
    image_np = np.asarray(bytearray(image), dtype=np.uint8)
    image_cv = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    qrs = decode(image_cv)
    if len(qrs) != 1:
        return None

    return qrs[0].data.decode()


def create_pkpass(format, message, backgroundColor=None, foregroundColor=None, labelColor=None, logoText=None, relevantDate=None, expirationDate=None):
    passfile = Pass(
        StoreCard(),
        passTypeIdentifier='pass.wallet.glebosotov.azazkamaz',
        organizationName='Snikers Team',
        teamIdentifier='A6AQ53FW7T',
    )

    passfile.serialNumber = uuid4().hex
    passfile.barcode = Barcode(
        format=format,
        message=message,
        messageEncoding='utf8',
    )

    passfile.backgroundColor = backgroundColor
    passfile.foregroundColor = foregroundColor
    passfile.logoText = logoText
    passfile.relevantDate = relevantDate
    passfile.expirationDate = expirationDate

    passfile.addFile('icon.png', open('./assets/icon.png', 'rb'))
    passfile.addFile('logo.png', open('./assets/logo.png', 'rb'))

    file = tempfile.NamedTemporaryFile()
    passfile.create(config['cert'], config['key'],
                    config['wwdr'], config['pass'], file.name)
    return io.BytesIO(file.read())


@app.post("/api/submit", responses={400: {}})
async def submit(
    image: bytes = File(),
    backgroundColor: Optional[str] = FormColor(),
    foregroundColor: Optional[str] = FormColor(),
    logoText: Optional[str] = Form(),
    relevantDate: Optional[str] = FormDateTime(),
    expirationDate: Optional[str] = FormDateTime(),
):
    qr = scan_qr(image)

    if qr is None:
        raise HTTPException(400, "Should be exactly one QR")

    file = create_pkpass(
        BarcodeFormat.QR,
        qr,
        backgroundColor=backgroundColor,
        foregroundColor=foregroundColor,
        logoText=logoText,
        relevantDate=relevantDate,
        expirationDate=expirationDate,
    )

    return responses.StreamingResponse(
        file,
        headers={'Content-Disposition': 'attachment; filename="pass.pkpass"'},
    )


app.mount("/", StaticFiles(directory="./static", html=True), name="static")


def run_dev():
    uvicorn.run("sqr.main:app", port=int(
        config['port']), host='0.0.0.0', reload=True)


def run_prod():
    uvicorn.run("sqr.main:app", port=int(
        config['port']), host='0.0.0.0', reload=False)
