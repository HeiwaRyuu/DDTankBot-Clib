# THIS IS AN IMAGE RECONITION TEST
from src_imgs_path import *
import pyautogui
import time
import pydirectinput ## MOVE VIRTUAL CURSOR, SO IT DOES NOT MESS WITH REGULAR WINDOWS CURSOR
import time
from PIL import Image


class DDTankBot:

    def __init__(self):
        self.padd_x=10
        self.padd_y=10
        self.max_attempts = 10
        self.condifence = 0.8
        self.standard_lower_confidence = 0.5
        self.sleep_delay = lambda x: time.sleep(x)
        self.standard_sleep_delay = 0.5
        self.initialize_images()

    
    def initialize_images(self):
        self.BAG = BAG_IMAGE
        self.OPEN_LOTE = OPEN_LOTE_IMAGE
        self.OPEN_MAX_LOTE = OPEN_MAX_LOTE_IMAGE
        self.OPEN_YES_BUTTON = OPEN_ITEM_YES_BUTTON_IMAGE
        self.OPEN_SINGLE_ITEM = OPEN_SINGLE_ITEM_IMAGE

    ## THIS WILL DO FOR NOW, WILL HAVE TO TRAIN MY OWN OPENCV MODEL AFTER FOR ACTUALLY FINDING HARDER IMAGES TO RECOGNIZE

    ## THESE MAKE THE CODE MORE READABLE
    def check_if_img_on_screen_and_click(self, image, confidence='standard', last_step_check=False, padding=(0,0), half_padding=False, max_attempts=1):
        if confidence == 'standard':
            confidence = self.condifence
        if half_padding:
            img_width, img_height = Image.open(image).size
            padd_x = img_width*(1/2)
            padd_y = img_height*(1/2)
            padding = (padd_x, padd_y)
        attempts = 0
        while attempts < max_attempts:
            if last_step_check:
                try:
                    location = pyautogui.locateOnScreen(image , confidence=confidence, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                    if location:
                        print(f"found {image} Image!")
                        x, y = location[0], location[1]
                        pydirectinput.moveTo(x + int(round(padding[0], 0)), y + int(round(padding[1], 0)))
                        pydirectinput.click()
                        return True
                    else:
                        print(f"Not found {image} Image!")
                        return False
                except Exception as e:
                    print("EXCEPTION: ", e)

    
    def check_if_img_on_screen(self, image, last_step_check=False, max_attempts=1):
        attempts = 0
        while attempts < max_attempts:
            if last_step_check:
                try:
                    location = pyautogui.locateOnScreen(image , confidence=self.condifence, grayscale=False) ##WORKS FOR A SMALL RANGE OF IMAGE SIZES
                    if location:
                        print(f"found {image} Image!")
                        return True
                    else:
                        print(f"Not found {image} Image!")
                        return False
                except Exception as e:
                    print("EXCEPTION: ", e)


    def open_bag(self):
        return self.check_if_img_on_screen_and_click(self.BAG, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)


    def open_yes_button(self):
        return self.check_if_img_on_screen_and_click(self.OPEN_YES_BUTTON, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)

    def open_max_lote(self):
        return self.check_if_img_on_screen_and_click(self.OPEN_MAX_LOTE, confidence=self.standard_lower_confidence, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)

    
    def open_single_item(self):
        return self.check_if_img_on_screen_and_click(self.OPEN_SINGLE_ITEM, confidence=self.standard_lower_confidence, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)


    def open_lote(self):
        return self.check_if_img_on_screen_and_click(self.OPEN_LOTE, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)
         

    def check_if_item(self, item):
        return self.check_if_img_on_screen_and_click(item, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)


    def open_item(self, item):
        attempts = 0
        max_attempts = 1
        item_on_screen = True
        while item_on_screen:
            while attempts < max_attempts:
                item_on_screen = self.check_if_item(item)
                self.sleep_delay(self.standard_sleep_delay*5)
                attempts += 1
                if item_on_screen:
                    break
            if item_on_screen:
                self.sleep_delay(self.standard_sleep_delay)
                if_open_lote = self.open_lote()
                if if_open_lote:
                    self.open_max_lote()
                    self.open_yes_button()
                else:
                    self.open_single_item()


    ## LETS DEVELOP A LOGIC FOR KILLING THE ANT QUEEN (INDEPENDENT OF WHERE YOU SPAWN, BUT FIRST, WE NEEK TO FIND A WAY TO RECOGNIZE THE SPAWN POINT, AND THEN THE ANT QUEEN POSITION)
    ## ON TOP OF THAT, WE NEED OUR DISTANCE TO HER, OUR ANGLE, THE WIND, AND ALSO THE DIFF IN HEIGHT BETWEEN US AND HER



class DDTankAntQueen(DDTankBot):
    def __init__(self):
        super().__init__()
        self.initialize_antqueen_images()


    def initialize_antqueen_images(self):
        self.OPEN_EXPEDITION=OPEN_EXPEDITION
        self.EXPEDITION_SELECTION=ANTQUEEN_EXPEDITION_SELECTION
        self.EXPEDITION_DIFFICULTY=EASY_EXPEDITION_DIFFICULTY
        self.EXPEDITION_YES_SELECTION=EXPEDITION_YES_SELECTION
        self.TWO_FREE_BOSS_BATTLE=TWO_FREE_BOSS_BATTLE
        self.ONE_FREE_BOSS_BATTLE=ONE_FREE_BOSS_BATTLE
        self.START_AT_BOSS_BATTLE=START_AT_BOSS_BATTLE
        self.BUY_EXPEDITION_MEDALS_POP_UP=BUY_EXPEDITION_MEDALS_POP_UP
        self.NOT_ENOUGH_MEDALS_POP_UP=NOT_ENOUGH_MEDALS_POP_UP
        self.FAST_MEDAL_BUY_POP_UP=FAST_MEDAL_BUY_POP_UP
        self.SPEND_MEDAL_TO_OPEN_EXPEDITION=SPEND_MEDAL_TO_OPEN_EXPEDITION

    

    ## MAIN LOOP
    def mainloop(self):
        self.sleep_delay(self.standard_sleep_delay)
        open_expedition_check = self.check_if_img_on_screen_and_click(self.OPEN_EXPEDITION, last_step_check=True, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)
        
        ## CHECK IF FREE BOSS BATTLES
        two_free_boss_battle_check = self.check_if_img_on_screen(self.TWO_FREE_BOSS_BATTLE, last_step_check=open_expedition_check)
        one_free_boss_battle_check = self.check_if_img_on_screen(self.ONE_FREE_BOSS_BATTLE, last_step_check=open_expedition_check)

        select_expedition_check = self.check_if_img_on_screen_and_click(self.EXPEDITION_SELECTION, last_step_check=open_expedition_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        select_difficulty_check = self.check_if_img_on_screen_and_click(self.EXPEDITION_DIFFICULTY, last_step_check=select_expedition_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        select_start_at_boss_battle_check = self.check_if_img_on_screen_and_click(self.START_AT_BOSS_BATTLE, last_step_check=select_difficulty_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        select_yes_check = self.check_if_img_on_screen_and_click(self.EXPEDITION_YES_SELECTION, last_step_check=select_start_at_boss_battle_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        buy_medals_check = self.buy_medals(two_free_boss_battle_check, one_free_boss_battle_check, select_yes_check)
        self.sleep_delay(self.standard_sleep_delay)

        self.finish_opening_expedition(buy_medals_check, select_yes_check)

        if buy_medals_check:
            print("INSTANCE OPENED!")
        else:
            print("INSTANCE NOT OPENED!")


    def buy_medals(self, two_free_boss_battle_check, one_free_boss_battle_check, select_yes_check):
        if two_free_boss_battle_check or one_free_boss_battle_check:
            if select_yes_check:
                return False
        else:
            img_width, img_height = Image.open(self.BUY_EXPEDITION_MEDALS_POP_UP).size
            padd_x = img_width*(1/5)
            padd_y = img_height*(3.5/4)
            self.check_if_img_on_screen_and_click(self.BUY_EXPEDITION_MEDALS_POP_UP, last_step_check=True, padding=(padd_x, padd_y))

            img_width, img_height = Image.open(self.NOT_ENOUGH_MEDALS_POP_UP).size
            padd_x = img_width*(1/6)
            padd_y = img_height*(3.5/4)
            self.check_if_img_on_screen_and_click(self.NOT_ENOUGH_MEDALS_POP_UP, last_step_check=True, padding=(padd_x, padd_y))

            img_width, img_height = Image.open(self.FAST_MEDAL_BUY_POP_UP).size
            padd_x = img_width*self.condifence
            padd_y = img_height*0.375
            self.check_if_img_on_screen_and_click(self.FAST_MEDAL_BUY_POP_UP, last_step_check=True, padding=(padd_x, padd_y))
            ## DOUBLE PRESS 9 FOR MAX NUMBER OF MEDALS
            pyautogui.press('9')
            pyautogui.press('9')
            img_width, img_height = Image.open(self.FAST_MEDAL_BUY_POP_UP).size
            padd_x = img_width*(1/2)
            padd_y = img_height*0.85
            self.check_if_img_on_screen_and_click(self.FAST_MEDAL_BUY_POP_UP, last_step_check=True, padding=(padd_x, padd_y))

            return True
        
    
    def finish_opening_expedition(self, buy_medals_check, select_yes_check):
        if buy_medals_check:
            self.sleep_delay(self.standard_sleep_delay)
            img_width, img_height = Image.open(self.EXPEDITION_YES_SELECTION).size
            padd_x = img_width*1/2
            padd_y = img_height*1/2
            self.check_if_img_on_screen_and_click(self.EXPEDITION_YES_SELECTION, last_step_check=True, padding=(padd_x, padd_y))

            img_width, img_height = Image.open(self.SPEND_MEDAL_TO_OPEN_EXPEDITION).size
            padd_x = img_width*0.23
            padd_y = img_height*0.85
            self.check_if_img_on_screen_and_click(self.SPEND_MEDAL_TO_OPEN_EXPEDITION, last_step_check=True, padding=(padd_x, padd_y))
        else:
            if select_yes_check:
                img_width, img_height = Image.open(self.SPEND_MEDAL_TO_OPEN_EXPEDITION).size
                padd_x = img_width*0.23
                padd_y = img_height*0.85
                self.check_if_img_on_screen_and_click(self.SPEND_MEDAL_TO_OPEN_EXPEDITION, last_step_check=True, padding=(padd_x, padd_y))





## WILL STOP FOR TODAY -> NEXT UP IS ACTUALLY CHECKING IF THE CURRENT METHOS WILL BE CONSISTENT ENOUGH SO IT CAN RUN ON ANY SCREEN SIZE
## THE IDEAL WORLD WOULD BE WHERE WE CAN CONTROL A VIRTUAL MOUSE INSTEAD OF OUR WINDOWS MOUSE, NOT SURE IT THIS WILL BE POSSIBLE.

def main():
    bot_test = DDTankBot()
    # bot_test.open_bag()
    bot_test.open_item(MANUAL_COMPLETO_IMAGE)
    # antqueen_farm_bot = DDTankAntQueen()
    # antqueen_farm_bot.mainloop()


if __name__ == '__main__':
    main()