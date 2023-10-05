from pymem import *
from pymem.process import *
import time
import numpy as np
import pyautogui
import pydirectinput
import os

def initialize_process(process_name, module_name):
    try:
        pm = pymem.Pymem(process_name)
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


####### ENEMY #######
ENEMY_X_POS_PTR_OFFSET = 0xDD46C4 ## NOT CONSISTENT
ENEMY_X_POS_OFFSETS = [0x16C, 0x270, 0x9C, 0x10C, 0x160, 0x2BC, 0x3C] ## NOT CONSISTENT

ENEMY_Y_POS_PTR_OFFSET = 0xDD46C4  ## NOT CONSISTENT 
ENEMY_Y_POS_OFFSETS = [0x16C, 0x270, 0x9C, 0x10C, 0x160, 0x2BC, 0x40] ## NOT CONSISTENT

####### WINDDIGIT #######
WIND_FIRST_DIGIT_PTR_OFFSET = 0 ## NOT FOUND
WIND_FIRST_DIGIT_OFFSETS = []

WIND_SECOND_DIGIT_PTR_OFFSET = 0 ## NOT FOUND
WIND_SECOND_DIGIT_OFFSETS = []


# WIND DIGIT  POSITIVE CODE	 NEGATIVE	
#    0	       4282087544	4280696896	ok
#    1	       4286595650	4278190080	problem
#    2	       4285839988	4282873671	ok
#    3	       4290746449	4290746449	problem
#    4	       4294957199	4278190080	problem
#    5	       4285553203	4291269686	ok
#    6	       4281686837	4278190080	problem
#    7	       4286611530	4290756462	ok
#    8	       4284769479	4280492888	ok
#    9	       4290728787	4287577405	ok



def hold_W(key, hold_time):
    start = time.time()
    while time.time() - start < hold_time:
        pydirectinput.press(key)


## FIND WINDOW POSITION AND DIMENTIONS
def find_window_region(window_name="SurfTank"):
    window_handle = pyautogui.getWindowsWithTitle(window_name)[0]
    window_rect = window_handle.topleft
    window_width = window_handle.width
    window_height = window_handle.height

    return (window_rect[0], window_rect[1], window_width, window_height)


def teleport_to_enemy_location(pm, player_x_pos_addr, player_y_pos_addr, enemy_x_pos_addr, enemy_y_pos_addr):
    print("PLAYER X POS: ", pm.read_int(player_x_pos_addr))
    print("PLAYER Y POS: ", pm.read_int(player_y_pos_addr))
    enemy_x_pos = pm.read_int(enemy_x_pos_addr)
    enemy_y_pos = pm.read_int(enemy_y_pos_addr)
    print("ENERMY X POS: ", enemy_x_pos)
    print("ENERMY Y POS: ", enemy_y_pos)
    
    time.sleep(1)
    pm.write_int(player_x_pos_addr, enemy_x_pos)
    pm.write_int(player_y_pos_addr, enemy_y_pos)

    print("PLAYER X POS: ", pm.read_int(player_x_pos_addr))
    print("PLAYER Y POS: ", pm.read_int(player_y_pos_addr))
    print("ENERMY X POS: ", enemy_x_pos)
    print("ENERMY Y POS: ", enemy_y_pos)
    time.sleep(0.5)
    for i in range(0, 3):
        pydirectinput.press("left")
        time.sleep(0.5)


def print_game_info():
    pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")

    weapon_angle_addr = GetPtrAddr(pm, gameModule + ANGLE_PTR_OFFSET, [*ANGLE_OFFSETS]) ## DOUBLE
    is_player_turn_addr = GetPtrAddr(pm, gameModule + PLAYER_TURN_PTR_OFFSET, [*PLAYER_TURN_OFFSETS]) ## INT 4
    is_player_shooting_addr = GetPtrAddr(pm, gameModule + PLAYER_SHOOTING_PTR_OFFSET, [*PLAYER_SHOOTING_OFFSETS]) ## INT 4
    last_round_shot_force_addr = GetPtrAddr(pm, gameModule + LAST_ROUND_SHOT_FORCE_PTR_OFFSET, [*LAST_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    current_round_shot_force_addr = GetPtrAddr(pm, gameModule + CURRENT_ROUND_SHOT_FORCE_PTR_OFFSET, [*CURRENT_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    player_x_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_X_POS_PTR_OFFSET, [*PLAYER_X_POS_OFFSETS]) ## BYTE
    player_y_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_Y_POS_PTR_OFFSET, [*PLAYER_Y_POS_OFFSETS]) ## BYTE
    enemy_x_pos_addr = GetPtrAddr(pm, gameModule + ENEMY_X_POS_PTR_OFFSET, [*ENEMY_X_POS_OFFSETS]) ## BYTE
    enemy_y_pos_addr = GetPtrAddr(pm, gameModule + ENEMY_Y_POS_PTR_OFFSET, [*ENEMY_Y_POS_OFFSETS]) ## BYTE
    player_life_addr = GetPtrAddr(pm, gameModule + PLAYER_LIFE_PTR_OFFSET, [*PLAYER_LIFE_OFFSETS]) ## DOUBLE
    player_stamina_addr = GetPtrAddr(pm, gameModule + PLAYER_STAMINA_PTR_OFFSET, [*PLAYER_STAMINA_OFFSETS]) ## DOUBLE
    player_pow_addr = GetPtrAddr(pm, gameModule + PLAYER_POW_PTR_OFFSET, [*PLAYER_POW_OFFSETS]) ## INT 4
    player_mp_addr = GetPtrAddr(pm, gameModule + PLAYER_MP_PTR_OFFSET, [*PLAYER_MP_OFFSETS]) ## INT 4

    while True:
        print("PLAYER WEAPON ANGLE: ", pm.read_double(weapon_angle_addr))
        print("IS PLAYER TURN: ", pm.read_int(is_player_turn_addr))
        print("IS PLAYER SHOOTING: ", pm.read_int(is_player_shooting_addr))
        print("LAST ROUND SHOT FORCE: ", round((pm.read_double(last_round_shot_force_addr)*(100/500)), 0))
        print("CURRENT ROUND SHOT FORCE: ", round(pm.read_double(current_round_shot_force_addr)*(100/2000), 0))
        print("PLAYER X POS: ", pm.read_int(player_x_pos_addr))
        print("PLAYER Y POS: ", pm.read_int(player_y_pos_addr))

        # print("ENEMY X POS: ", pm.read_int(enemy_x_pos_addr))
        # print("ENEMY Y POS: ", pm.read_int(enemy_y_pos_addr))

        print("PLAYER LIFE: ", pm.read_double(player_life_addr))
        print("PLAYER STAMINA: ", pm.read_double(player_stamina_addr))
        print("PLAYER POW: ", pm.read_int(player_pow_addr))
        print("PLAYER MP: ", pm.read_int(player_mp_addr))
        time.sleep(1)
        os.system("cls")


def main():
    pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")

    weapon_angle_addr = GetPtrAddr(pm, gameModule + ANGLE_PTR_OFFSET, [*ANGLE_OFFSETS]) ## DOUBLE
    is_player_turn_addr = GetPtrAddr(pm, gameModule + PLAYER_TURN_PTR_OFFSET, [*PLAYER_TURN_OFFSETS]) ## INT 4
    is_player_shooting_addr = GetPtrAddr(pm, gameModule + PLAYER_SHOOTING_PTR_OFFSET, [*PLAYER_SHOOTING_OFFSETS]) ## INT 4
    last_round_shot_force_addr = GetPtrAddr(pm, gameModule + LAST_ROUND_SHOT_FORCE_PTR_OFFSET, [*LAST_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    current_round_shot_force_addr = GetPtrAddr(pm, gameModule + CURRENT_ROUND_SHOT_FORCE_PTR_OFFSET, [*CURRENT_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    player_x_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_X_POS_PTR_OFFSET, [*PLAYER_X_POS_OFFSETS]) ## BYTE
    player_y_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_Y_POS_PTR_OFFSET, [*PLAYER_Y_POS_OFFSETS]) ## BYTE
    enemy_x_pos_addr = GetPtrAddr(pm, gameModule + ENEMY_X_POS_PTR_OFFSET, [*ENEMY_X_POS_OFFSETS]) ## BYTE
    enemy_y_pos_addr = GetPtrAddr(pm, gameModule + ENEMY_Y_POS_PTR_OFFSET, [*ENEMY_Y_POS_OFFSETS]) ## BYTE
    player_life_addr = GetPtrAddr(pm, gameModule + PLAYER_LIFE_PTR_OFFSET, [*PLAYER_LIFE_OFFSETS]) ## DOUBLE
    player_stamina_addr = GetPtrAddr(pm, gameModule + PLAYER_STAMINA_PTR_OFFSET, [*PLAYER_STAMINA_OFFSETS]) ## DOUBLE
    player_pow_addr = GetPtrAddr(pm, gameModule + PLAYER_POW_PTR_OFFSET, [*PLAYER_POW_OFFSETS]) ## INT 4
    player_mp_addr = GetPtrAddr(pm, gameModule + PLAYER_MP_PTR_OFFSET, [*PLAYER_MP_OFFSETS]) ## INT 4

    teleport_to_enemy_location(pm, player_x_pos_addr, player_y_pos_addr, enemy_x_pos_addr, enemy_y_pos_addr)

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
        else:
            pass
            # print("NOT PLAYER TURN...")



if __name__ == "__main__":
    # main()  
    print_game_info()