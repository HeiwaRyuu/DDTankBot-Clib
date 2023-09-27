import pyautogui
from PIL import Image
import pytesseract
import easyocr
import numpy as np
import cv2
from src_imgs_path import *
import os



## FIND WINDOW POSITION AND DIMENTIONS
def find_window_region():
    window_handle = pyautogui.getWindowsWithTitle('SurfTank')[0]
    window_rect = window_handle.topleft
    window_width = window_handle.width
    window_height = window_handle.height

    return (window_rect[0], window_rect[1], window_width, window_height)


def screenshot_region(region, filename):
    img = pyautogui.screenshot(region=region)
    img.save(filename)
    return filename


def image_blackwhite(image):
    img_grey = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(image,img_grey) 


def image_upscale(image, scale_dimentions):
    x_ratio = 1
    y_ratio = 1
    image_width, image_height = Image.open(image).size
    ## scale up
    if image_width <= scale_dimentions[0]:
        x_ratio = scale_dimentions[0]/image_width
    if image_height <= scale_dimentions[1]:
        y_ratio = scale_dimentions[1]/image_height

    ## scale down
    if image_width > scale_dimentions[0]:
        x_ratio = scale_dimentions[0]/image_width
    if image_height > scale_dimentions[1]:
        y_ratio = scale_dimentions[1]/image_height
    
    if x_ratio != 1 or y_ratio != 1:
        image_width = int(round(image_width*x_ratio, 0))
        image_height = int(round(image_height*y_ratio, 0))
        image_obj = Image.open(image).resize((image_width, image_height))
        image_obj.save(image)


def find_wind_digit(wind_screenshot):
    img_rgb = cv2.imread(wind_screenshot)
    wind_digit_images=[]
    for file in os.listdir(DIGITS_PATH):
        if file.startswith('ddtank_wind_digit'):
            wind_digit_images.append(DIGITS_PATH+file)

    for index, wind_digit_image in enumerate(wind_digit_images):
        wind_digit=wind_digit_image
        template = cv2.imread(wind_digit)
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.85
        loc = np.where(res >= threshold)
        if loc[0].size>0:
            digit = wind_digit_image.split('_')[-1][0]
            return digit


def define_wind_digit_region(image_path, wind_digit_start_x_multiplier, wind_digit_start_y_multiplier, wind_digit_width_multiplier, wind_digit_height_multiplier):
    window_x, window_y, window_width, window_height =find_window_region()
    wind_start_x = round(window_width * wind_digit_start_x_multiplier, 0)
    wind_start_y = round(window_height * wind_digit_start_y_multiplier, 0)
    wind_width = round(wind_start_x* wind_digit_width_multiplier, 0)
    wind_height = round(wind_start_y* wind_digit_height_multiplier, 0)

    wind_region=(window_x+wind_start_x, window_y+wind_start_y, wind_width, wind_height)
    wind_image = screenshot_region(wind_region, image_path)
    image_blackwhite(wind_image)
    image_upscale(wind_image, scale_dimentions=(wind_width*4, wind_height*4))
    digit = find_wind_digit(wind_image)

    return digit

def find_wind_value():
    wind_1_digit_start_x_multiplier = 0.475
    wind_1_digit_start_y_multiplier = 0.09
    wind_1_digit_width_multiplier = 0.045
    wind_1_digit_height_multiplier = 0.365

    wind_2_digit_start_x_multiplier = 0.51
    wind_2_digit_start_y_multiplier = 0.09
    wind_2_digit_width_multiplier = 0.04
    wind_2_digit_height_multiplier = 0.365

    digit_1 = define_wind_digit_region(WIND_SCREENSHOT_1_DIGIT, wind_1_digit_start_x_multiplier, wind_1_digit_start_y_multiplier, wind_1_digit_width_multiplier, wind_1_digit_height_multiplier)
    digit_2 = define_wind_digit_region(WIND_SCREENSHOT_2_DIGIT, wind_2_digit_start_x_multiplier, wind_2_digit_start_y_multiplier, wind_2_digit_width_multiplier, wind_2_digit_height_multiplier)

    wind_value = f'{digit_1}.{digit_2}'
    print(wind_value)


find_wind_value()