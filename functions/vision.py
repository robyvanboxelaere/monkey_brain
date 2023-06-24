# Imports
from PIL import Image
import pytesseract
import numpy as np
from mss import mss
import cv2
from pyautogui import locateOnScreen
import time
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the image file
image_path = os.path.join(current_dir, "../assets/")

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

    # Convert to grayscale
    img = img.convert('L')

    # Make all pixels <= rgb(220, 220, 220) black
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j] <= 254:
                pixels[i, j] = 0

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
    roundEnd = cv2.imread(os.path.join(image_path, 'round_end.png'))
    # Resize roundEnd to match img
    roundEnd = cv2.resize(roundEnd, (img.shape[1], img.shape[0]))
    roundEnd = cv2.cvtColor(roundEnd, cv2.COLOR_BGR2GRAY)

    # Read round_in_progress.png
    roundInProgress = cv2.imread(os.path.join(image_path, 'round_in_progress.png'))
    # Resize roundInProgress to match img
    roundInProgress = cv2.resize(roundInProgress, (img.shape[1], img.shape[0]))
    roundInProgress = cv2.cvtColor(roundInProgress, cv2.COLOR_BGR2GRAY)

    # Compare images
    mseValEnd = mse(img, roundEnd)
    mseValInProgress = mse(img, roundInProgress)

    # Return True if round ended, False if round in progress
    if mseValEnd < mseValInProgress:
        print('Round ended')
        return True
    else:
        print('Round in progress')
        return False

# Function that checks if the game has ended (victory or defeat screen in middle of screen)
def check_game_state():
    # Check if it detects victory or defeat screen image
    # If victory
    if locateOnScreen(os.path.join(image_path, 'victory_screen.png'), confidence=0.9) != None:
        print('Victory')
        return True
    # If defeat
    elif locateOnScreen(os.path.join(image_path, 'defeat_screen.png'), confidence=0.9) != None:
        print('Defeat')
        return True

    print('Game still in progress')
    return False

# Function that checks round progression and cash amount
def return_game_info():
    return view_round_progression(), read_cash()

# Loop that checks game states
def loop_game_info(seconds):
    # Keep looping until round ends
    while True:
        # Check round progression and cash amount
        roundEnded, cashAmount = return_game_info()
        print('Cash amount: ' + cashAmount)
        if roundEnded:
            break

        # Check game state
        gameEnded = check_game_state()
        if gameEnded:
            break

        # Wait for x seconds
        time.sleep(seconds)

loop_game_info(5)