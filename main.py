# THIS IS AN IMAGE RECONITION TEST
from src_imgs_path import *
import os
import pyautogui ## THIS WILL DO FOR NOW, WILL HAVE TO TRAIN MY OWN OPENCV MODEL AFTER FOR ACTUALLY FINDING HARDER IMAGES TO RECOGNIZE
import time
import pydirectinput ## MOVE VIRTUAL CURSOR, SO IT DOES NOT MESS WITH REGULAR WINDOWS CURSOR
import time
from PIL import Image


class DDTankBot:

    def __init__(self):
        self.padd_x=10
        self.padd_y=10
        self.max_attempts = 10
        self.max_error_ratio_up = 1.02
        self.min_error_ratio_down = 0.98
        self.condifence = 0.8
        self.standard_lower_confidence = 0.5
        self.resized_confidence = 0.6
        self.sleep_delay = lambda x: time.sleep(x)
        self.standard_sleep_delay = 0.5
        self.standard_window_dimensions=(942, 646)
        self.initialize_images()

    
    def initialize_images(self):
        self.BAG = BAG_IMAGE
        self.OPEN_LOTE = OPEN_LOTE_IMAGE
        self.OPEN_MAX_LOTE = OPEN_MAX_LOTE_IMAGE
        self.OPEN_YES_BUTTON = OPEN_ITEM_YES_BUTTON_IMAGE
        self.OPEN_SINGLE_ITEM = OPEN_SINGLE_ITEM_IMAGE


    def screenshot_region(self, region):
        return pyautogui.screenshot(region=region)


    ## FIND WINDOW POSITION AND DIMENTIONS
    def find_window_region(self):
        window_handle = pyautogui.getWindowsWithTitle('SurfTank')[0]
        window_rect = window_handle.topleft
        window_width = window_handle.width
        window_height = window_handle.height

        return (window_rect[0], window_rect[1], window_width, window_height)
    

    ## CALCULATE THE SIZE DOWN RATIO SO WE CAN FIND THE IMAGES ON SCREEN PROPERLY BASED ON OUR PRINTS
    def find_window_scale_ratio(self, window_width, window_height):
        x_ratio = window_width/self.standard_window_dimensions[0]
        y_ratio = window_height/self.standard_window_dimensions[1]

        return (x_ratio, y_ratio)
    

    ## IF IMAGE RATIO IS DIFFERENT FROM 1, WE NEED TO RESIZE THE IMAGE TO MATCH THE WINDOW SIZE
    def resize_image(self, image, x_ratio, y_ratio):
        if_resized = False
        confidence = self.resized_confidence
        if ((round(x_ratio, 2) <= self.min_error_ratio_down) or (round(x_ratio, 2) >= self.max_error_ratio_up)) or ((round(y_ratio, 2) <= self.min_error_ratio_down) or (round(y_ratio, 2) >= self.max_error_ratio_up)):
            image_width, image_height = Image.open(image).size
            image_width = int(round(image_width*x_ratio, 0))
            image_height = int(round(image_height*y_ratio, 0))
            image_obj = Image.open(image).resize((image_width, image_height))
            new_path = RISEZED_TEMP_PATH+image.split('/')[-1]
            image_obj.save(new_path)
            
            image = new_path
            if_resized = True
            confidence=self.resized_confidence ## CHANGE IT IF NECESSARY
        
        return image, if_resized, confidence
        

    ## DELETE TEMPORARY RESIZED IMAGES
    def delete_resized_temp_images(self, file_path):
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    

    ## THESE MAKE THE CODE MORE READABLE
    def check_if_img_on_screen(self, image, confidence='standard', last_step_check=False, padding=(0,0), half_padding=False, max_attempts=1, click=True):
        attempts = 0
        if confidence == 'standard':
            confidence = self.condifence
        
        ## IF HALF PADDING IS TRUE, WE WILL USE HALF OF THE IMAGE SIZE AS PADDING TO CLICK ON ITS CENTER
        if half_padding:
            img_width, img_height = Image.open(image).size
            padd_x = img_width*(1/2)
            padd_y = img_height*(1/2)
            padding = (padd_x, padd_y)

        while attempts < max_attempts:
            if last_step_check:
                try:
                    window_x, window_y, window_width, window_height = self.find_window_region()
                    x_ratio, y_ratio = self.find_window_scale_ratio(window_width, window_height)
                    image, if_resized, confidence = self.resize_image(image, x_ratio, y_ratio)
                    # self.sleep_delay(self.standard_sleep_delay)
                    location = pyautogui.locateOnScreen(image , confidence=confidence, grayscale=False, region=(window_x, window_y, window_width, window_height)) ##WORKS FOR A BROAD RANGE OF SCREEN SIZES NOW
                    if if_resized:
                        self.delete_resized_temp_images(image)
                    if location:
                        print(f"found {image} Image!")
                        x, y = location[0], location[1]
                        pydirectinput.moveTo(x + int(round(padding[0], 0)), y + int(round(padding[1], 0)))
                        if click:
                            pydirectinput.click()
                        return True
                    else:
                        print(f"Not found {image} Image!")
                        attempts += 1
                except Exception as e:
                    print("EXCEPTION: ", e)
                    attempts += 1
            else:
                return False

        return False


    def open_bag(self):
        return self.check_if_img_on_screen(self.BAG, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)


    def open_yes_button(self):
        return self.check_if_img_on_screen(self.OPEN_YES_BUTTON, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)

    def open_max_lote(self):
        return self.check_if_img_on_screen(self.OPEN_MAX_LOTE, confidence=self.standard_lower_confidence, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)

    
    def open_single_item(self):
        return self.check_if_img_on_screen(self.OPEN_SINGLE_ITEM, confidence=self.standard_lower_confidence, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)


    def open_lote(self):
        return self.check_if_img_on_screen(self.OPEN_LOTE, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)
         

    def check_if_item(self, item):
        return self.check_if_img_on_screen(item, last_step_check=True, half_padding=True, max_attempts=self.max_attempts)


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
            else:
                break


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
        self.START_EXPEDITION_BUTTON=START_EXPEDITION_BUTTON
        self.CONFIRM_START_EXPEDITION_ALONE=CONFIRM_START_EXPEDITION_ALONE


    def mainloop(self):
        self.sleep_delay(self.standard_sleep_delay)
        open_expedition_check = self.check_if_img_on_screen(self.OPEN_EXPEDITION, last_step_check=True, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)
        
        ## CHECK IF FREE BOSS BATTLES
        two_free_boss_battle_check = self.check_if_img_on_screen(self.TWO_FREE_BOSS_BATTLE, confidence=self.standard_lower_confidence, last_step_check=open_expedition_check, click=False)
        one_free_boss_battle_check = self.check_if_img_on_screen(self.ONE_FREE_BOSS_BATTLE, confidence=self.standard_lower_confidence, last_step_check=open_expedition_check, click=False)

        select_expedition_check = self.check_if_img_on_screen(self.EXPEDITION_SELECTION, last_step_check=open_expedition_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        select_difficulty_check = self.check_if_img_on_screen(self.EXPEDITION_DIFFICULTY, last_step_check=select_expedition_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        select_start_at_boss_battle_check = self.check_if_img_on_screen(self.START_AT_BOSS_BATTLE, last_step_check=select_difficulty_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        select_yes_check = self.check_if_img_on_screen(self.EXPEDITION_YES_SELECTION, last_step_check=select_start_at_boss_battle_check, half_padding=True)
        self.sleep_delay(self.standard_sleep_delay)

        buy_medals_check = self.buy_medals(two_free_boss_battle_check, one_free_boss_battle_check, select_yes_check)
        self.sleep_delay(self.standard_sleep_delay)

        is_expedition_open = self.finish_opening_expedition(buy_medals_check, select_yes_check)

        if is_expedition_open:
            print("INSTANCE OPENED!")
        else:
            print("INSTANCE NOT OPENED!")

        has_expedition_started = self.start_expedition(is_expedition_open)


    def buy_medals(self, two_free_boss_battle_check, one_free_boss_battle_check, select_yes_check):
        if ((two_free_boss_battle_check) or (one_free_boss_battle_check)) and (select_yes_check):
            return False
        elif ((not two_free_boss_battle_check) and (not one_free_boss_battle_check)) and (not select_yes_check):
            return False
        else:
            check_buy_expedition_medals_pop_up = self.check_if_img_on_screen(self.BUY_EXPEDITION_MEDALS_POP_UP, last_step_check=True)
            if check_buy_expedition_medals_pop_up:
                pyautogui.press('enter')

            check_not_enough_medals_pop_up = self.check_if_img_on_screen(self.NOT_ENOUGH_MEDALS_POP_UP, last_step_check=True)
            if check_not_enough_medals_pop_up:
                pyautogui.press('enter')

            img_width, img_height = Image.open(self.FAST_MEDAL_BUY_POP_UP).size
            padd_x = img_width*self.condifence
            padd_y = img_height*0.375
            self.check_if_img_on_screen(self.FAST_MEDAL_BUY_POP_UP, last_step_check=True, padding=(padd_x, padd_y))
            ## DOUBLE PRESS 9 FOR MAX NUMBER OF MEDALS
            pyautogui.press('9')
            pyautogui.press('9')
            pyautogui.press('enter')
            return True
        
    
    def finish_opening_expedition(self, buy_medals_check, select_yes_check):
        if buy_medals_check:
            self.sleep_delay(self.standard_sleep_delay)
            img_width, img_height = Image.open(self.EXPEDITION_YES_SELECTION).size
            padd_x = img_width*1/2
            padd_y = img_height*1/2
            self.check_if_img_on_screen(self.EXPEDITION_YES_SELECTION, last_step_check=True, padding=(padd_x, padd_y))

            pyautogui.press('enter')
            return True
        else:
            if select_yes_check:
                img_width, img_height = Image.open(self.SPEND_MEDAL_TO_OPEN_EXPEDITION).size
                padd_x = img_width*0.23
                padd_y = img_height*0.85
                self.check_if_img_on_screen(self.SPEND_MEDAL_TO_OPEN_EXPEDITION, last_step_check=True, padding=(padd_x, padd_y))
                return True
            
    
    def start_expedition(self, is_expedition_open):
        if is_expedition_open:
            img_width, img_height = Image.open(self.START_EXPEDITION_BUTTON).size
            padd_x = img_width*0.5
            padd_y = img_height*0.5
            self.check_if_img_on_screen(self.START_EXPEDITION_BUTTON, last_step_check=is_expedition_open, half_padding=True)


            stard_expedition_alone_check = self.check_if_img_on_screen(self.CONFIRM_START_EXPEDITION_ALONE, last_step_check=True, half_padding=True)
            if stard_expedition_alone_check:
                pyautogui.press('enter')
            return True
        else:
            return False


## FIXED SCREEN SIZE CHANGE BY RESIZING IMAGES ACCORDING TO THE NEW SCREEN SIZE (BY CALCULATING SCREEN RATIO)
## THE IDEAL WORLD WOULD BE WHERE WE CAN CONTROL A VIRTUAL MOUSE INSTEAD OF OUR WINDOWS MOUSE, NOT SURE IT THIS WILL BE POSSIBLE. -> STILL LOOKING FOR IT

def main():
    bot_test = DDTankBot()
    # bot_test.open_bag()
    # bot_test.open_item(HONRA_IMAGE)
    antqueen_farm_bot = DDTankAntQueen()
    antqueen_farm_bot.mainloop()


if __name__ == '__main__':
    main()