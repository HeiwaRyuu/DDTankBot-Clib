from pymem import *
from pymem.process import *
import time

pm = pymem.Pymem("LoadingAir.exe")

gameModule = pymem.process.module_from_name(pm.process_handle, "Adobe AIR.dll").lpBaseOfDll


def GetPtrAddr(base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i != offsets[-1]:
            addr = pm.read_int(addr + i)

    return addr + offsets[-1]


OFFSET_WITHIN_ADOBE_AIR_DLL = 0xDD44F0
ANGLE_OFFSETS = [0X0, 0X508, 0X3A0, 0X4, 0XD4, 0X158, 0X320]

print(f"GAMEMODULE: {hex(gameModule)}")
print(f"GAMEMODULE + OFFSET_WITHIN_ADOBE_AIR_DLL: {hex(gameModule + OFFSET_WITHIN_ADOBE_AIR_DLL)}")
print(f"ANGLE_OFFSET: {hex(ANGLE_OFFSETS[-1])}")

while True:
    
    print(f"READ FROM MEM VALUE: {pm.read_double(GetPtrAddr(gameModule + OFFSET_WITHIN_ADOBE_AIR_DLL, [*ANGLE_OFFSETS]))}")
    # time.sleep(1)