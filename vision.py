# Imports
from PIL import Image
import pytesseract
import numpy as np
from mss import mss
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def mse(img1, img2):
    if img1.shape != img2.shape:
        print('Images do not have the same dimensions.')
        return

    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse

def read_cash():
    # Read money.png
    # img = Image.open('money.png')

    # Boundaries: 250, 40, 350, 80
    boundingBox = (340, 20, 650, 65)
    sct = mss()

    sct_image = sct.grab(boundingBox)
    img = Image.frombytes('RGB', sct_image.size, sct_image.rgb)

    # Save image    
    # img.save('money.png')

    # Convert to grayscale
    img = img.convert('L')

    # Make all pixels <= rgb(220, 220, 220) black
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j] <= 254:
                pixels[i, j] = 0

    # Save grayscale image
    # img.save('money_converted.png')

    # Convert to text
    cashAmount = pytesseract.image_to_string(img)

    # Remove every non integer
    cashAmount = ''.join(filter(str.isdigit, cashAmount))

    return cashAmount

def view_round_progression():
    # Boundaries: 1775, 960, 1890, 1070
    boundingBox = (1775, 960, 1890, 1070)
    sct = mss()

    sctImage = sct.grab(boundingBox)
    img = Image.frombytes('RGB', sctImage.size, sctImage.rgb)

    # Check if img is most similar to round_end.png or round_in_progress.png
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Read round_end.png
    roundEnd = cv2.imread('round_end.png')
    # Resize roundEnd to match img
    roundEnd = cv2.resize(roundEnd, (img.shape[1], img.shape[0]))
    roundEnd = cv2.cvtColor(roundEnd, cv2.COLOR_BGR2GRAY)

    # Read round_in_progress.png
    roundInProgress = cv2.imread('round_in_progress.png')
    # Resize roundInProgress to match img
    roundInProgress = cv2.resize(roundInProgress, (img.shape[1], img.shape[0]))
    roundInProgress = cv2.cvtColor(roundInProgress, cv2.COLOR_BGR2GRAY)

    # Compare images
    mseValEnd = mse(img, roundEnd)
    mseValInProgress = mse(img, roundInProgress)

    if mseValEnd < mseValInProgress:
        print('Round ended')
    else:
        print('Round in progress')
    
view_round_progression()
print(read_cash())
