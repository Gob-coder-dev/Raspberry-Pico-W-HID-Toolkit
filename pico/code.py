import asyncio
import board
import digitalio
import supervisor
import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from keyboard_layout_win_fr import KeyboardLayout
from action import shutdown, launch_weblink, pdf_download, pdf_download_and_open, import_data_on_website

supervisor.runtime.autoreload = False

# --- LED onboard ---
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def init_input(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.DOWN
    return io

# GPIO utilisés comme déclencheurs
gp0 = init_input(board.GP0)
gp1 = init_input(board.GP1)
gp2 = init_input(board.GP2)
gp3 = init_input(board.GP3)
gp4 = init_input(board.GP4)

async def blink_task(stop_event, period=0.15):
    """Fait clignoter la LED jusqu'à ce que stop_event soit déclenché."""
    while not stop_event.is_set():
        led.value = not led.value
        await asyncio.sleep(period)
    led.value = False

async def main():
    stop_blink = asyncio.Event()
    asyncio.create_task(blink_task(stop_blink, period=0.12))
    
    await asyncio.sleep(2.0)  # Attente initialisation USB
    
    kbd = Keyboard(usb_hid.devices, timeout=10)
    layout = KeyboardLayout(kbd)

    # Mapping GPIO -> actions
    if gp0.value:
        shutdown(kbd, layout)
    if gp1.value:
        launch_weblink(kbd, layout, "https://www.youtube.com/watch?v=xvFZjo5PgG0")
    if gp2.value:
        pdf_download(kbd, layout)
    if gp3.value:
        pdf_download_and_open(kbd, layout)
    if gp4.value:
        import_data_on_website(kbd, layout)
    
    await asyncio.sleep(0.6)
    stop_blink.set()
    await asyncio.sleep(5.0)
    
    while True:
        await asyncio.sleep(1)

asyncio.run(main())