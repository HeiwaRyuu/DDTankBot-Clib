import pymem
import keyboard
import time


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


def pointer_injection():
    
    pm, gameModule, pid = initialize_process(process_name="LoadingAir.exe", module_name="Adobe AIR.dll")

    PLAYER_X_POS_PTR_OFFSET = 0xDD46C4
    PLAYER_X_POS_OFFSETS = [0x16C, 0x270, 0x9C, 0x10C, 0x160, 0x2C, 0x3C]

    PLAYER_Y_POS_PTR_OFFSET = 0xDD46C4
    PLAYER_Y_POS_OFFSETS = [0x16C, 0x270, 0x9C, 0x10C, 0x160, 0x2C, 0x40]

    player_x_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_X_POS_PTR_OFFSET, [*PLAYER_X_POS_OFFSETS]) ## BYTE
    player_y_pos_addr = GetPtrAddr(pm, gameModule + PLAYER_Y_POS_PTR_OFFSET, [*PLAYER_Y_POS_OFFSETS]) ## BYTE

    move_char_x = 500
    move_char_y = 500

    time_to_sleep = 0.05

    def tp_right():
        current_value = pm.read_int(player_x_pos_addr)
        new_value = current_value + move_char_x
        pm.write_int(player_x_pos_addr, new_value)
        print("tp_right")

    def tp_left():
        current_value = pm.read_int(player_x_pos_addr)
        new_value = current_value - move_char_x
        pm.write_int(player_x_pos_addr, new_value)
        print("tp_left")

    def tp_up():
        current_value = pm.read_int(player_y_pos_addr)
        new_value = current_value - move_char_y
        pm.write_int(player_y_pos_addr, new_value)
        print("tp_up")

    def tp_down():
        current_value = pm.read_int(player_y_pos_addr)
        new_value = current_value + move_char_y
        pm.write_int(player_y_pos_addr, new_value)
        print("tp_down")

    while True:
        if keyboard.is_pressed('w') and keyboard.is_pressed('d'):
            tp_up()
            tp_right()
            time.sleep(time_to_sleep*2)
            continue

        if keyboard.is_pressed('w') and keyboard.is_pressed('a'):
            tp_up()
            tp_left()
            time.sleep(time_to_sleep*2)
            continue

        if keyboard.is_pressed('s') and keyboard.is_pressed('d'):
            tp_down()
            tp_right()
            time.sleep(time_to_sleep*2)
            continue

        if keyboard.is_pressed('s') and keyboard.is_pressed('a'):
            tp_down()
            tp_left()
            time.sleep(time_to_sleep*2)
            continue

        if keyboard.is_pressed('w'):
            tp_up()
            time.sleep(time_to_sleep)
            continue

        if keyboard.is_pressed('s'):
            tp_down()
            time.sleep(time_to_sleep)
            continue

        if keyboard.is_pressed('d'):
            tp_right()
            time.sleep(time_to_sleep)
            continue

        if keyboard.is_pressed('a'):
            tp_left()
            time.sleep(time_to_sleep)
            continue


if __name__ == "__main__":
    pointer_injection()