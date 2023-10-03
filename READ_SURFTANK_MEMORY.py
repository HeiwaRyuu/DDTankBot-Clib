from pymem import *
from pymem.process import *
import time
import numpy as np
import pyautogui
import pydirectinput
from subprocess import Popen, PIPE
import win32com.client as comclt


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
    


def main():
    pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")

    weapon_angle_addr = GetPtrAddr(pm, gameModule + ANGLE_PTR_OFFSET, [*ANGLE_OFFSETS]) ## DOUBLE
    is_player_turn_addr = GetPtrAddr(pm, gameModule + PLAYER_TURN_PTR_OFFSET, [*PLAYER_TURN_OFFSETS]) ## INT 4
    is_player_shooting_addr = GetPtrAddr(pm, gameModule + PLAYER_SHOOTING_PTR_OFFSET, [*PLAYER_SHOOTING_OFFSETS]) ## INT 4
    last_round_shot_force_addr = GetPtrAddr(pm, gameModule + LAST_ROUND_SHOT_FORCE_PTR_OFFSET, [*LAST_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE
    current_round_shot_force_addr = GetPtrAddr(pm, gameModule + CURRENT_ROUND_SHOT_FORCE_PTR_OFFSET, [*CURRENT_ROUND_SHOT_FORCE_OFFSETS]) ## DOUBLE

    while True:
        is_player_turn = pm.read_int(is_player_turn_addr)
        if is_player_turn == 1:
            weapon_angle = pm.read_double(weapon_angle_addr)
            is_player_shooting = pm.read_int(is_player_shooting_addr)
            if is_player_turn == 1:
                (f"IS PLAYER SHOOTING: {'SHOOTING...' if is_player_shooting == 1 else 'NOT SHOOTING...'}")

            print(f"WEAPON ANGLE: {weapon_angle}")
            print(f"IS PLAYER TURN: {f'PLAYER TURN: {is_player_turn}' if is_player_turn == 1 else f'NOT PLAYER TURN: {is_player_turn}'}")

            if is_player_turn:
                ## FOCUSING WINDOW
                region = find_window_region(window_name="SurfTank")
                pyautogui.moveTo(region[0]+region[2]/2, region[1]+region[3]/2)
                pyautogui.click()
                
                try:
                    last_round_shot_force = pm.read_double(last_round_shot_force_addr)
                    current_round_shot_force = pm.read_double(current_round_shot_force_addr)
                    while pm.read_double(current_round_shot_force_addr) == 0:
                        # ## WRITE A RANDOM VALUE BETWEEN 0 AND 2000 IN THE current_round_shot_force_addr
                        rand_power = np.random.randint(1000, 2000)
                        pm.write_double(current_round_shot_force_addr, float(rand_power))
                        pm.write_double(last_round_shot_force_addr, float((500/2000) * rand_power))

                        rand_angle = np.random.randint(15, 65)
                        pm.write_double(weapon_angle_addr, float(rand_angle))
                        # pm.write_int(is_player_shooting_addr, 1)
                        time.sleep(1)

                    pydirectinput.press("space")
                except Exception as e:
                    print(f"Excessão ao tentar atirar...: {e}")

                print(f"LAST ROUND SHOT FORCE: {last_round_shot_force}")
                print(f"CURRENT ROUND SHOT FORCE: {current_round_shot_force}")
                
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        else:
            print("NOT PLAYER TURN...")

if __name__ == "__main__":
    main()  
    # hold_W("space", 20)