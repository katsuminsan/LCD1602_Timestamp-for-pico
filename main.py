import tpui_title
import time
import machine

tss = tpui_title.tpui_title()
KEY_SELECT = machine.Pin(8, machine.Pin.IN)
KEY_ENTER = machine.Pin(9, machine.Pin.IN)

while True:
    tss.update(tss.PAGEMODEL)
    
    if KEY_SELECT.value() == 1 and KEY_ENTER.value() == 0:
        tss.Clicked_Select()
        
    if KEY_SELECT.value() == 0 and KEY_ENTER.value() == 1:
        tss.Clicked_Enter()
        
    time.sleep_ms(24)