import pyautogui;
import time;
import random;

monkeyDict = {
    "dartMonkey": "q"
}

def select_monkey(monkey):
    try:
        print(monkeyDict[monkey])
    except:
        print("Whoops, something went wrong. (the monkey is not in the dictionary)")

#this fucntion checks every pixel around coordinates x and y for specific rgb values
#def 

def check_area(x, y):
    for i in range(0, 100):
        for j in range(0, 100):
            if (pyautogui.pixelMatchesColor(x + i, y + j, (255, 0, 0), tolerance=0)):
                return False
    return True

def click_random():
    c = True
    while c:
        x = random.randint(25, 1640)
        y = random.randint(0, 1080)
        pyautogui.moveTo(x, y)
        if check_area(x, y):
            pyautogui.click(x, y)
            c = False
        

    
select_monkey("theZoo")
