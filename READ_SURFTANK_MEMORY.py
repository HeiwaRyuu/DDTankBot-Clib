from pymem import *
from pymem.process import *
import time
import numpy as np
import pyautogui
import pydirectinput
import os
import psutil
import keyboard

ANGLE_PTR_OFFSET = 0xDD44F0 
ANGLE_OFFSETS = [0x0, 0x508, 0x3A0, 0x4, 0xD4, 0x158, 0x320]

PLAYER_TURN_PTR_OFFSET = 0xDD44F0
PLAYER_TURN_OFFSETS = [0x0, 0x508, 0x3A0, 0x4, 0xD4, 0x158, 0x2CC]

PLAYER_SHOOTING_PTR_OFFSET = 0xDD44F0
PLAYER_SHOOTING_OFFSETS = [0x0, 0x508, 0x3A0, 0x4, 0xD4, 0x158, 0x284]

LAST_ROUND_SHOT_FORCE_PTR_OFFSET = 0xDD46C4
LAST_ROUND_SHOT_FORCE_OFFSETS = [0x16C, 0x270, 0xC, 0x9C, 0xD0, 0x8C, 0xB8]

CURRENT_ROUND_SHOT_FORCE_PTR_OFFSET = 0xDD46C4
CURRENT_ROUND_SHOT_FORCE_OFFSETS = [0x16C, 0x270, 0xC, 0x9C, 0xD0, 0x8C, 0xC0]

PLAYER_X_POS_PTR_OFFSET = 0xDD46C4
PLAYER_X_POS_OFFSETS = [0x16C, 0x270, 0x9C, 0x10C, 0x160, 0x2C, 0x3C]

PLAYER_Y_POS_PTR_OFFSET = 0xDD46C4
PLAYER_Y_POS_OFFSETS = [0x16C, 0x270, 0x9C, 0x10C, 0x160, 0x2C, 0x40]

PLAYER_LIFE_PTR_OFFSET = 0xDD46C4
PLAYER_LIFE_OFFSETS = [0x4, 0x510, 0x120, 0x4, 0xD4, 0x158, 0x178]

PLAYER_STAMINA_PTR_OFFSET = 0xDD46C4
PLAYER_STAMINA_OFFSETS = [0x4, 0x510, 0x120, 0x4, 0xD4, 0x158, 0x190]

PLAYER_POW_PTR_OFFSET = 0xDD46C4
PLAYER_POW_OFFSETS = [0x4, 0x510, 0x120, 0x4, 0xD4, 0x158, 0x1FC]

PLAYER_MP_PTR_OFFSET = 0xDD46C4
PLAYER_MP_OFFSETS = [0x16C, 0x2AC, 0x24C, 0x0, 0xB4, 0x25C, 0x28]


####### ENEMY POSITION #######
## WORKING AFTER SOME FILTERS
AOB_ENEMY_POS = rb'\x59\x40................................\x54\x68..\x00\x00\x00\x00\x06\x00\x00\x00....................\x00\x10\xFF\xFF..\x08\x80....\x00\x00\x80\x3F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F..\x00\x00..\x00\x00.\x00\x00\x00.\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x59\x40\x00\x00\x00\x00\x00\x00\x59\x40\xFF\xFF\xFF\x07\xFF\xFF\xFF\x07\xFF\xFF\xFF\x07\xFF\xFF\xFF\x07'
ENEMY_X_POS_OFFSET = 0x5E
ENEMY_Y_POS_OFFSET = ENEMY_X_POS_OFFSET + 0x4
ENEMY_TURN_OFFSET = ENEMY_X_POS_OFFSET + 0xC
ENEMY_TURN_POSSIBLE_VALUES_LST = [9, 10, 11]

####### WIND DIGITS ####### SEEMS TO HAVE NO PROBLEMS --> SEEMS TO WORK ON EXPEDITION, WILL TRY TO TEST IT ON REGULAR PVP AND DIFFERENT CLIENT
WIND_BASE_AOB = rb'\x15\x4B\xAB\xFF\x04\x43\xBD\xFF\x02\x49\xD0\xFF\x0B\x2F\x82\xFF\x0D\x55\xDB\xFF\x01\x74\xF3\xFF\x42\x60\x1B\xFF\x01\x74\xF3\xFF\x01\x4E\xEA\xFF\x05\x32\xA2\xFF\x01\x65\xF2\xFF\x02\x7F\xF5\xFF'
WIND_FIRST_DIGIT_OFFSET = 0x140 # 0x180
WIND_SECOND_DIGIT_OFFSET = WIND_FIRST_DIGIT_OFFSET + 0x80
POSITIVE_CODE_DICT = {-12295612:'0', -15853544:'1', -8885938:'2', -11522257:'3', -15066568:'4', -7814008:'5', -14602207:'6', -12569827:'7', -15724537:'8', -14277040:'9'}
NEGATIVE_CODE_DICT = {-9982873:'0', -13412264:'1', -12166:'2', -4231570:'3', -1:'4', -11566001:'5', -16248824:'6', -4744347:'7', -1579152:'8', -9210961:'9'}


# pos			neg	
# 0	4282671684		0	4284984423
# 1	4279113752		1	4281555032
# 2	4286081358		2	4294955130
# 3	4283445039		3	4290735726
# 4	4279900728		4	UNKNOWN
# 5	4287153288		5	4283401295
# 6	4280365089		6	4278718472
# 7	4282397469		7	4290222949
# 8	4279242759		8	4293388144
# 9	4280690256		9	4285756335




def get_pids(process):
    pids = []
    for proc in psutil.process_iter():
        if process in proc.name():
            pids.append(proc.pid)
    return pids


def initialize_process(process_name, module_name):
    try:
        pids = get_pids(process_name)
        pm = pymem.Pymem(pids[0])
    except:
        print("ERROR: Process not found")
        exit()

    gameModule = pymem.process.module_from_name(pm.process_handle, module_name).lpBaseOfDll
    pid = pm.process_id

    return pm, gameModule, pid


def GetPtrAddr(pm, base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i != offsets[-1]:
            addr = pm.read_int(addr + i)

    return addr + offsets[-1]


def check_forbidden_pairs(value_x, value_y):
    forbidden_x = [19100, 19000]
    forbidden_pairs = [(19900, 8860), (13000, 3400), (4900, 4360), 
    (1520, 6200), (2580, 2100), (4800, 9080), (80, 4580), (7480, 9340), 
    (19100, 4180), (100, 3760), (12300, 3260), (10000, 8880), 
    (17480, 6000), (8220, 4540)]

    for pair in forbidden_pairs: ## FILTERING X AND Y CANNOT BE EQUAL TO FORBIDDEN PAIRS (CURSED AOB PATTERNS)
        if (value_x in forbidden_x):
            return True
        if (value_x == pair[0]) and (value_y == pair[1]):
            return True

    return False


def aob_to_data_enemy_pos(pid, aob, offset_x=0, offset_y=0, offset_turn=0, my_pos_x=0, my_pos_y=0):
    pm = pymem.Pymem(pid)
    aob_address = pymem.pattern.pattern_scan_all(pm.process_handle, aob, return_multiple=True)
    for i, addr in enumerate(aob_address):
        addr_x = addr + offset_x
        addr_y = addr + offset_y
        addr_turn = addr + offset_turn
        value_x = pm.read_int(addr_x)
        value_y = pm.read_int(addr_y)
        value_turn = pm.read_int(addr_turn)

        if not (value_turn in ENEMY_TURN_POSSIBLE_VALUES_LST): ## FILTERING ENEMY TURN MUST BE 10 or 11
            continue

        if not ((value_x >= 1) and (value_y >= 1)): ## FILTERING X AND Y CANNOT BE 0
            continue

        if not ((value_x != my_pos_x) and (value_y != my_pos_y)): ## FILTERING X AND Y CANNOT BE EQUAL TO MY POSITION
            continue
        
        if not (value_y >= 2000 and value_y <= 50000): ## FILTERING Y CANNOT BE <= 1000 (this will rarely be the case)
            continue

        if not (value_x >= 150 and value_x <= 80000): ## FILTERING X CANNOT BE <= 100 (this will rarely be the case)
            continue

        return addr_x, addr_y
    
    return 0, 0


## NOT WORKING CONSISTENTLY, WILL HAVE TO FIND A WAY TO GET A GOOD AOB FOR THE WIND, BE IT THIS VALUE, OR BE IT A DIFFERENT VALUE FOR WIND AS WELL
def read_wind_addr(pid, aob, wind_first_digit_offset=0, wind_second_digit_offset=0):
    print("READ WIND ADDR")
    pm = pymem.Pymem(pid)
    addr = pymem.pattern.pattern_scan_all(pm.process_handle, aob, return_multiple=False)
    if addr:
        addr_first_digit = addr + wind_first_digit_offset
        addr_second_digit = addr + wind_second_digit_offset
        print("ADDR FIRST DIGIT: ", hex(addr_first_digit))
        print("ADDR SECOND DIGIT: ", hex(addr_second_digit))
        value_first_digit = pm.read_int(addr_first_digit)
        value_second_digit = pm.read_int(addr_second_digit)

        print("VALUE FIRST DIGIT: ", value_first_digit)
        print("VALUE SECOND DIGIT: ", value_second_digit)



## NOT WORKING CONSISTENTLY, WILL HAVE TO FIND A WAY TO GET A GOOD AOB FOR THE WIND, BE IT THIS VALUE, OR BE IT A DIFFERENT VALUE FOR WIND AS WELL
def aob_to_data_wind_digit(pid, aob, wind_first_digit_offset=0, wind_second_digit_offset=0):
    pm = pymem.Pymem(pid)
    addr = pymem.pattern.pattern_scan_all(pm.process_handle, aob, return_multiple=False)
    flag_found = False
    if addr:
        addr_first_digit = addr + wind_first_digit_offset
        addr_second_digit = addr + wind_second_digit_offset
        print("ADDR FIRST DIGIT: ", hex(addr_first_digit))
        print("ADDR SECOND DIGIT: ", hex(addr_second_digit))
        value_first_digit = pm.read_int(addr_first_digit)
        value_second_digit = pm.read_int(addr_second_digit)


        if value_first_digit in POSITIVE_CODE_DICT.keys():
            value_first_digit = POSITIVE_CODE_DICT.get(value_first_digit, "Not found")
            value_second_digit = POSITIVE_CODE_DICT.get(value_second_digit, "Not found")
            flag_found = True
        elif value_first_digit in NEGATIVE_CODE_DICT.keys():
            value_first_digit = NEGATIVE_CODE_DICT.get(value_first_digit, "Not found")
            value_second_digit = NEGATIVE_CODE_DICT.get(value_second_digit, "4")
            value_first_digit = f'-{value_first_digit}'
            flag_found = True

        if flag_found:
            return value_first_digit, value_second_digit
    else:
        print("WIND ADDR: ", "NOT FOUND")
        
    return False, False



## FIND WINDOW POSITION AND DIMENTIONS
def find_window_region(window_name="SurfTank"):
    window_handle = pyautogui.getWindowsWithTitle(window_name)[0]
    window_rect = window_handle.topleft
    window_width = window_handle.width
    window_height = window_handle.height

    return (window_rect[0], window_rect[1], window_width, window_height)


def teleport_to_enemy_location(pm, player_x_pos_addr, player_y_pos_addr, enemy_x_pos_addr, enemy_y_pos_addr):
    if enemy_x_pos_addr != 0 and enemy_y_pos_addr != 0:
        enemy_x_pos = pm.read_int(enemy_x_pos_addr)
        enemy_y_pos = pm.read_int(enemy_y_pos_addr)
    
        time.sleep(1)
        pm.write_int(player_x_pos_addr, enemy_x_pos)
        pm.write_int(player_y_pos_addr, enemy_y_pos)

        time.sleep(0.5)
        keyboard.press_and_release("left")
        keyboard.press_and_release("right")
    


def print_game_info():
    pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")

    weapon_angle_addr = GetPtrAddr(pm, gameModule + ANGLE_PTR_OFFSET, [*ANGLE_OFFSETS]) ## DOUBLE
    is_player_turn_addr = GetPtrAddr(pm, gameModule + PLAYER_TURN_PTR_OFFSET, [*PLAYER_TURN_OFFSETS]) ## INT 4
    is_player_shooting_addr = GetPtrAddr(pm, gameModule + PLAYER_SHOOTING_PTR_OFFSET, [*PLAYER_SHOOTING_OFFSETS]) ## INT 4
    last_round_shot_force_addr = GetPtrAddr(pm, gameModule + LAST_ROUND_SHOT_FORCE_PTR_OFFSET, [*LAST_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    current_round_shot_force_addr = GetPtrAddr(pm, gameModule + CURRENT_ROUND_SHOT_FORCE_PTR_OFFSET, [*CURRENT_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    player_x_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_X_POS_PTR_OFFSET, [*PLAYER_X_POS_OFFSETS]) ## BYTE
    player_y_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_Y_POS_PTR_OFFSET, [*PLAYER_Y_POS_OFFSETS]) ## BYTE

    enemy_x_pos_addr, enemy_y_pos_addr = aob_to_data_enemy_pos(pid, AOB_ENEMY_POS, ENEMY_X_POS_OFFSET, ENEMY_Y_POS_OFFSET, ENEMY_TURN_OFFSET, pm.read_int(player_x_pos_addr), pm.read_int(player_y_pos_addr)) ## 4 BYTE (AOB TO DATA)
    wind_digit_first, wind_digit_second = aob_to_data_wind_digit(pid, WIND_BASE_AOB, WIND_FIRST_DIGIT_OFFSET, WIND_SECOND_DIGIT_OFFSET) ## 4 BYTE (AOB TO DATA)

    player_life_addr = GetPtrAddr(pm, gameModule + PLAYER_LIFE_PTR_OFFSET, [*PLAYER_LIFE_OFFSETS]) ## DOUBLE
    player_stamina_addr = GetPtrAddr(pm, gameModule + PLAYER_STAMINA_PTR_OFFSET, [*PLAYER_STAMINA_OFFSETS]) ## DOUBLE
    player_pow_addr = GetPtrAddr(pm, gameModule + PLAYER_POW_PTR_OFFSET, [*PLAYER_POW_OFFSETS]) ## INT 4
    # player_mp_addr = GetPtrAddr(pm, gameModule + PLAYER_MP_PTR_OFFSET, [*PLAYER_MP_OFFSETS]) ## INT 4

    # while True:
    print("PLAYER WEAPON ANGLE: ", pm.read_double(weapon_angle_addr))
    print("IS PLAYER TURN: ", pm.read_int(is_player_turn_addr))
    print("IS PLAYER SHOOTING: ", pm.read_int(is_player_shooting_addr))
    print("LAST ROUND SHOT FORCE: ", round((pm.read_double(last_round_shot_force_addr)*(100/500)), 0))
    print("CURRENT ROUND SHOT FORCE: ", round(pm.read_double(current_round_shot_force_addr)*(100/2000), 0))
    print("PLAYER X POS: ", pm.read_int(player_x_pos_addr))
    print("PLAYER Y POS: ", pm.read_int(player_y_pos_addr))

    print("PLAYER LIFE: ", pm.read_double(player_life_addr))
    print("PLAYER STAMINA: ", pm.read_double(player_stamina_addr))
    print("PLAYER POW: ", pm.read_int(player_pow_addr))
    # print("PLAYER MP: ", pm.read_int(player_mp_addr))

    if enemy_x_pos_addr != 0 and enemy_y_pos_addr != 0:
        teleport_to_enemy_location(pm, player_x_pos_addr, player_y_pos_addr, enemy_x_pos_addr, enemy_y_pos_addr)
        print("ENEMY X POS: ", pm.read_int(enemy_x_pos_addr))
        print("ENEMY Y POS: ", pm.read_int(enemy_y_pos_addr))
    else:
        print("ENEMY X POS: ", "NOT FOUND")
        print("ENEMY Y POS: ", "NOT FOUND")

    if wind_digit_first != False and wind_digit_second != False:
        print(f'WIND VALUE == {wind_digit_first}.{wind_digit_second}')
    else:
        print("WIND VALUE == NOT FOUND")

        # time.sleep(1)
        # os.system("cls")


def main():
    pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")

    weapon_angle_addr = GetPtrAddr(pm, gameModule + ANGLE_PTR_OFFSET, [*ANGLE_OFFSETS]) ## DOUBLE
    is_player_turn_addr = GetPtrAddr(pm, gameModule + PLAYER_TURN_PTR_OFFSET, [*PLAYER_TURN_OFFSETS]) ## INT 4
    is_player_shooting_addr = GetPtrAddr(pm, gameModule + PLAYER_SHOOTING_PTR_OFFSET, [*PLAYER_SHOOTING_OFFSETS]) ## INT 4
    last_round_shot_force_addr = GetPtrAddr(pm, gameModule + LAST_ROUND_SHOT_FORCE_PTR_OFFSET, [*LAST_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    current_round_shot_force_addr = GetPtrAddr(pm, gameModule + CURRENT_ROUND_SHOT_FORCE_PTR_OFFSET, [*CURRENT_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    player_x_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_X_POS_PTR_OFFSET, [*PLAYER_X_POS_OFFSETS]) ## BYTE
    player_y_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_Y_POS_PTR_OFFSET, [*PLAYER_Y_POS_OFFSETS]) ## BYTE

    enemy_x_pos_addr, enemy_y_pos_addr = aob_to_data_enemy_pos(pid, AOB_ENEMY_POS, ENEMY_X_POS_OFFSET, ENEMY_Y_POS_OFFSET, ENEMY_TURN_OFFSET, pm.read_int(player_x_pos_addr), pm.read_int(player_y_pos_addr)) ## 4 BYTE (AOB TO DATA)

    player_life_addr = GetPtrAddr(pm, gameModule + PLAYER_LIFE_PTR_OFFSET, [*PLAYER_LIFE_OFFSETS]) ## DOUBLE
    player_stamina_addr = GetPtrAddr(pm, gameModule + PLAYER_STAMINA_PTR_OFFSET, [*PLAYER_STAMINA_OFFSETS]) ## DOUBLE
    player_pow_addr = GetPtrAddr(pm, gameModule + PLAYER_POW_PTR_OFFSET, [*PLAYER_POW_OFFSETS]) ## INT 4
    # player_mp_addr = GetPtrAddr(pm, gameModule + PLAYER_MP_PTR_OFFSET, [*PLAYER_MP_OFFSETS]) ## INT 4


    while True:
        print("PLAYER X POS: ", pm.read_int(player_x_pos_addr))
        print("PLAYER Y POS: ", pm.read_int(player_y_pos_addr))
        time.sleep(1)
        if pm.read_int(is_player_turn_addr) == 1:
            weapon_angle = pm.read_double(weapon_angle_addr)
            is_player_shooting = pm.read_int(is_player_shooting_addr)
            if pm.read_int(is_player_turn_addr) == 1:
                (f"IS PLAYER SHOOTING: {'SHOOTING...' if is_player_shooting == 1 else 'NOT SHOOTING...'}")

            print(f"WEAPON ANGLE: {weapon_angle}")
            print(f"IS PLAYER TURN: {f'PLAYER TURN: {pm.read_int(is_player_turn_addr)}' if pm.read_int(is_player_turn_addr) == 1 else f'NOT PLAYER TURN: {pm.read_int(is_player_turn_addr)}'}")

            if pm.read_int(is_player_turn_addr):
                ## FOCUSING WINDOW
                region = find_window_region(window_name="SurfTank")
                pyautogui.moveTo(region[0]+region[2]/2, region[1]+region[3]/2)
                pyautogui.click()
                
                try:
                    last_round_shot_force = pm.read_double(last_round_shot_force_addr)
                    current_round_shot_force = pm.read_double(current_round_shot_force_addr)
                    while pm.read_double(current_round_shot_force_addr) == 0:
                        # ## WRITE A RANDOM VALUE BETWEEN 0 AND 2000 IN THE current_round_shot_force_addr3444
                        rand_power = np.random.randint(1000, 2000)
                        pm.write_double(current_round_shot_force_addr, float(rand_power)) ## DOUBLE
                        pm.write_double(last_round_shot_force_addr, float((500/2000) * rand_power)) ## DOUBLE

                        rand_angle = np.random.randint(15, 30)
                        pm.write_double(weapon_angle_addr, float(rand_angle))
                        # pm.write_int(is_player_shooting_addr, 1)
                        time.sleep(1)

                    time.sleep(0.5)
                    pydirectinput.press("3")
                    pydirectinput.press("4")
                    pydirectinput.press("4")
                    pydirectinput.press("space")
                    pm.write_int(is_player_turn_addr, 0)
                except Exception as e:
                    print(f"Excessão ao tentar atirar...: {e}")

                print(f"LAST ROUND SHOT FORCE: {last_round_shot_force}")
                print(f"CURRENT ROUND SHOT FORCE: {current_round_shot_force}")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            time.sleep(1)
            os.system("cls")
        else:
            print("NOT PLAYER TURN...")
            time.sleep(1)
            os.system("cls")
            

if __name__ == "__main__":
    # main()  
    print_game_info()
    # pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")
    # read_wind_addr(pid, WIND_BASE_AOB, WIND_FIRST_DIGIT_OFFSET, WIND_SECOND_DIGIT_OFFSET)