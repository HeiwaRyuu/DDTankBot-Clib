# THIS IS AN IMAGE RECONITION TEST
from src_imgs_path import *
import pyautogui
import time
import pydirectinput ## MOVE VIRTUAL CURSOR, SO IT DOES NOT MESS WITH REGULAR WINDOWS CURSOR

BAG = SRC_PATH+BAG_IMAGE_WITH_BG
MANUAL_COMPLETO = SRC_PATH+MANUAL_COMPLETO_IMAGE_WITH_BG
OPEN_LOTE = SRC_PATH+OPEN_LOTE_IMAGE_WITH_BG
OPEN_MAX_LOTE = SRC_PATH+OPEN_MAX_LOTE_IMAGE_WITH_BG
OPEN_YES_BUTTON = SRC_PATH+OPEN_YES_BUTTON_IMAGE_WITH_BG
OPEN_SINGLE_ITEM = SRC_PATH+OPEN_SINGLE_ITEM_IMAGE_WITH_BG

class DDTankBot:

    def __init__(self):
        self.padd_x=10
        self.padd_y=10
        self.max_attempts = 20

    ## THIS WILL DO FOR NOW, WILL HAVE TO TRAIN MY OWN OPENCV MODEL AFTER FOR ACTUALLY FINDING HARDER IMAGES TO RECOGNIZE
    def open_bag(self):
        max_attempts = self.max_attempts
        attempts = 0
        while attempts < max_attempts:
            try:
                location = pyautogui.locateOnScreen(BAG , confidence=0.6, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                if location:
                    print("found Image!")
                    x, y = location[0], location[1]
                    pydirectinput.moveTo(x, y)
                    pydirectinput.click()
                else:
                    print(f"Not found BAG Image! ATTEMPT: {attempts+1} OF {max_attempts}")
                    attempts += 1
            except Exception as e:
                print("EXCEPTION: ", e)
                attempts += 1


    def open_yes_button(self):
        max_attempts = self.max_attempts
        attempts = 0
        while attempts < max_attempts:
            try:
                location = pyautogui.locateOnScreen(OPEN_YES_BUTTON , confidence=0.6, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                if location:
                    print("found OPEN_YES_BUTTON Image!")
                    x, y = location[0]+self.padd_x, location[1]+self.padd_y
                    pydirectinput.moveTo(x, y)
                    pydirectinput.click()
                    break
                else:
                    print(f"Not found OPEN_YES_BUTTON Image! ATTEMPT: {attempts+1} OF {max_attempts}")
                    attempts += 1
            except Exception as e:
                print("EXCEPTION: ", e)
                attempts += 1


    def open_max_lote(self):
        max_attempts = self.max_attempts
        attempts = 0
        while attempts < max_attempts:
            try:
                location = pyautogui.locateOnScreen(OPEN_MAX_LOTE , confidence=0.6, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                if location:
                    print("found OPEN_MAX_LOTE Image!")
                    x, y = location[0]+self.padd_x, location[1]+self.padd_y
                    pydirectinput.moveTo(x, y)
                    pydirectinput.click()
                    self.open_yes_button()
                    break
                else:
                    print(f"Not found OPEN_MAX_LOTE Image! ATTEMPT: {attempts+1} OF {max_attempts}")
                    attempts += 1
            except Exception as e:
                print("EXCEPTION: ", e)
                attempts += 1

    
    def open_single_item(self):
        max_attempts = self.max_attempts
        attempts = 0
        while attempts < max_attempts:
            try:
                location = pyautogui.locateOnScreen(OPEN_SINGLE_ITEM , confidence=0.6, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                if location:
                    print("found OPEN_SINGLE_ITEM Image!")
                    x, y = location[0]+self.padd_x, location[1]+self.padd_y
                    pydirectinput.moveTo(x, y)
                    pydirectinput.click()
                    break
                else:
                    print(f"Not found OPEN_SINGLE_ITEM Image!: ATTEMPT: {attempts+1} OF {max_attempts}")
                    attempts += 1
            except Exception as e:
                print("EXCEPTION: ", e)
                attempts += 1


    def open_lote(self):
        max_attempts = self.max_attempts
        attempts = 0
        while attempts < max_attempts:
            try:
                location = pyautogui.locateOnScreen(OPEN_LOTE , confidence=0.6, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                if location:
                    print("found OPEN_LOTE Image!")
                    x, y = location[0]+self.padd_x, location[1]+self.padd_y
                    pydirectinput.moveTo(x, y)
                    pydirectinput.click()
                    self.open_max_lote()
                    return True
                    break
                else:
                    print(f"Not found OPEN_LOTE Image! ATTEMPT: {attempts+1} OF {max_attempts}")
                    attempts += 1
            except Exception as e:
                print("EXCEPTION: ", e)
                attempts += 1


    def open_manual(self):
        max_attempts = self.max_attempts
        attempts = 0
        while attempts < max_attempts:
            try:
                location = pyautogui.locateOnScreen(MANUAL_COMPLETO , confidence=0.6, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                if location:
                    print("found MANUAL_COMPLETO Image!")
                    x, y = location[0]+self.padd_x, location[1]+self.padd_y
                    pydirectinput.moveTo(x, y)
                    pydirectinput.click()
                    check_lote = self.open_lote()
                    if not check_lote:
                        self.open_single_item()
                else:
                    print(f"Not found MANUAL_COMPLETO Image! ATTEMPT: {attempts+1} OF {max_attempts}")
                    attempts += 1
            except Exception as e:
                print("EXCEPTION: ", e)
                attempts += 1



## WILL STOP FOR TODAY -> NEXT UP IS ACTUALLY CHECKING IF THE CURRENT METHOS WILL BE CONSISTENT ENOUGH SO IT CAN RUN ON ANY SCREEN SIZE
## THE IDEAL WORLD WOULD BE WHERE WE CAN CONTROL A VIRTUAL MOUSE INSTEAD OF OUR WINDOWS MOUSE, NOT SURE IT THIS WILL BE POSSIBLE.

def main():
    bot_test = DDTankBot()
    # bot_test.open_bag()
    bot_test.open_manual()


if __name__ == '__main__':
    main()