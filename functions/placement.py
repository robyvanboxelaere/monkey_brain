import pyautogui
from pyautogui import click, locateOnScreen, moveTo, scroll, sleep
import time
import random
import os
import numpy as np

# Import read_cash() from functions\vision.py
from vision import read_cash

# Get the current directory
currentDir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the image file
imagePath = os.path.join(currentDir, "../assets/towers/")

# Entry class for monkey list
class Entry:
    def __init__(self, price, name, position):
        self.price = price
        self.name = name
        self.position = position

def scrollUpMonkeyMenu():
    # Move mouse to menu
    pyautogui.moveTo(1750, 300)
    # Scroll until you detect 1.png
    locatedTower = locateOnScreen(imagePath + '1.png', confidence=0.8)
    while locatedTower is None:
        scroll(250)
        locatedTower = locateOnScreen(imagePath + '1.png', confidence=0.8)

    # Another scroll to make there's no cutoff
    scroll(250)

#TODO: Add random monkey placement
def generateRandomValidMonkey():
    # Generate random monkey
    # Do not include monkey if you don't have the money to buy it
    # List of monkeys with prices
    monkeyList = {
        Entry(585, "Quincy", 0), 
        Entry(215, "Dart Monkey", 1),
        Entry(350, "Boomerang Monkey", 2),
        Entry(565, "Bomb Shooter", 3),
        Entry(300, "Tack Shooter", 4),
        Entry(540, "Ice Monkey", 5),
        Entry(245, "Glue Gunner", 6),
        Entry(380, "Sniper Monkey", 7),
        Entry(540, "Monkey Buccaneer", 8),
        Entry(865, "Monkey Ace", 9),
        Entry(405, "Wizard Monkey", 10),
        Entry(2700, "Super Monkey", 11),
        Entry(540, "Ninja Monkey", 12),
        Entry(595, "Alchemist", 13),
        Entry(430, "Druid", 14),
        Entry(1080, "Spike Factory", 15),
        Entry(1295, "Monkey Village", 16),
        Entry(430 , "Engineer Monkey", 17),
    }

    # Get cash amount
    cashAmount = int(read_cash())

    # Remove all monkeys that are too expensive, retain 
    validMonkeysList = monkeyList.copy()
    for monkey in validMonkeysList:
        if monkey.price > cashAmount:
            validMonkeysList.remove(monkey)

    # Get random monkey from list
    randomMonkey = random.choice(list(validMonkeysList))

    # Return entry number
    return randomMonkey

def findMonkey(monkey):
    locatedTower = locateOnScreen(imagePath + str(monkey.position) + '.png', confidence=0.8)
    while locatedTower is None:
        scroll(-250)
        locatedTower = locateOnScreen(imagePath + str(monkey.position) + '.png', confidence=0.8)

    return locatedTower

def selectValidMonkey(monkey = None):
    # Move mouse to menu
    scrollUpMonkeyMenu()

    if monkey is None:
        # Generate random monkey
        monkey = generateRandomValidMonkey()
    else:
        # Get cash amount
        cashAmount = int(read_cash())

        # If the monkey is too expensive, return
        if monkey.price > cashAmount:
            print("Monkey is too expensive")
            return
    
    locatedTower = findMonkey(monkey)

    # Move mouse to tower
    # pyautogui.moveTo(locatedTower)
    # Click on tower
    pyautogui.click(locatedTower)

    print("Putting down " + monkey.name + " for " + str(monkey.price) + " dollars")
    
# Check if the area is valid
# The monkey is surrounded by red pixels (255, 0, 0) when the area is invalid
def checkArea(x, y):
    # Capture the screen or a region of interest (adjust region as needed)
    screenshot = pyautogui.screenshot(region=(x, y, 100, 100))
    
    # Convert the screenshot to a NumPy array for faster processing
    screenshot_array = np.array(screenshot)

    # Check if any pixel in the region is red
    if np.any((screenshot_array == [255, 0, 0]).all(axis=-1)):
        print("Area is invalid")
        return True
    return False

# Clicks the screen at a random location
def placeMonkey(monkey = None, x = None, y = None):
    selectValidMonkey(monkey)
    if x is None or y is None:
        invalidArea = True
        while invalidArea:
            x = random.randint(25, 1640)
            y = random.randint(100, 1080)
            pyautogui.moveTo(x, y)
            invalidArea = checkArea(x, y)
    else:
        invalidArea = checkArea(x, y)
        if invalidArea:
            print("Area is invalid")
            return

    print("Clicking at: " + str(x) + ", " + str(y))
    pyautogui.click(x, y)
        
# Wait 3 seconds before starting
time.sleep(3)
pyautogui.moveTo(1450, 300)
pyautogui.click()
placeMonkey()