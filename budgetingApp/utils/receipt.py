from base64 import b64decode
from requests import post
from json import loads
from os import remove

def saveReceiptToFile(imageData, filePath: str = "tmp/receipt.jpeg"):
    """
    Decodes a BASE64 image and saves it at a given path.

    This function is used to save as temporary files the receipts
    uploaded by the users using their camera.

    Arguments:
        - imageData: The raw image data received from POST
        - filePath (str): The path where to save the image.
    """

    _, imgstr = imageData.split(';base64,')
    data = b64decode(imgstr)

    with open(filePath, "wb") as file:
        file.write(data)

def parseReceiptImage(imageFile: str = "tmp/receipt.jpeg"):
    """
    Extracts key features from an image.

    This function is used to perform OCR (Optical-Character-Recognition)
    on receipt images. The result given by a third party API is then converted
    into a JSON object for immediate usage.

    Arguments:
        - imageFile (str): The path to the receipt image.
    """

    receiptOcrEndpoint = 'https://ocr2.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
    # receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt'
    
    
    res = post(receiptOcrEndpoint, data = {
        'api_key': 'TEST',
        'recognizer': 'auto',
        'ref_no': 'ocr_python_123'},
        
        files = {"file": open(imageFile, "rb")})
    
    # Remove temporary image after process
    remove("tmp/receipt.jpeg")

    return loads(res.text)