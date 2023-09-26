import pyautogui
from PIL import Image
import pytesseract
import easyocr
import cv2


## FIND WINDOW POSITION AND DIMENTIONS
def find_window_region():
    window_handle = pyautogui.getWindowsWithTitle('SurfTank')[0]
    window_rect = window_handle.topleft
    window_width = window_handle.width
    window_height = window_handle.height

    return (window_rect[0], window_rect[1], window_width, window_height)

def screenshot_region(region):
    img = pyautogui.screenshot(region=region)
    img.save('wind_screenshot.png')


def image_blackwhite(image):
    img_grey = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    ## define a threshold, 128 is the middle of black and white in grey scale
    thresh = 5
    ## threshold the image
    img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
    #save image
    cv2.imwrite(image,img_binary) 


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


def fetch_wind_value(image):
    wind_value=''
    wind_digits='.0123456789'
    current_wind_digits=[]
    digit_counter=0
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, allowlist=wind_digits, decoder='greedy', rotation_info=[90, 180, 270], detail=0)
    print(result)
    # if len(result) > 0:
    #     text_result = result[0][1]
    #     if len(text_result) > 2:
    #         print("RESULT: ", text_result)
    #         # if text_result[0] == '8':
    #         #     text_result.replace('8', '3', 1)
    #         # elif text_result[0] == '3':
    #         #     text_result.replace('3', '1', 1)
    #         current_wind_digits.append(text_result[0])
    #         current_wind_digits.append(text_result[2])

    wind_value = '.'.join(current_wind_digits)

    print(wind_value)


wind_img = 'wind_screenshot.png'
window_x, window_y, window_width, window_height =find_window_region()
print('WINDOW REGION: ', window_x, window_y, window_width, window_height)
wind_start_x = round(window_width * 0.478, 0)
wind_start_y = round(window_height * 0.09, 0)
print('WIND START REGION: ', wind_start_x, wind_start_y)
wind_width = round(wind_start_x*0.1, 0)
wind_height = round(wind_start_y*0.35, 0)
print('WIND REGION: ', wind_width, wind_height)

wind_region=(window_x+wind_start_x, window_y+wind_start_y, wind_width, wind_height)
screenshot_region(wind_region)
image_blackwhite(wind_img)
image_upscale(wind_img, scale_dimentions=(wind_width*4, wind_height*4))
fetch_wind_value(wind_img)

# test_digits='ex_digits.png'
# img_cv = cv2.imread(wind)
# img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img_rgb, config='--psm 10 --oem 3 -c tessedit_char_whitelist=.0123456789'))