import asyncio
import board
import digitalio
import supervisor
import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode  # for GUI/R/ENTER/CTRL+A
from keyboard_layout_win_fr import KeyboardLayout  # FR Windows layout (Neradoc)

supervisor.runtime.autoreload = False


Ascii = """
        .+=::...........:-*+++++=
       +=.    =    ===- ...    ...-@*
     .#=   : -: :----=:  ..:::    : .++.
    .#:   ... .:::::  -     -     .   +*
   :*-      :*@@@@:*#=.     .:++++:   .#:.
 :+*:#%%+=+ ++++@*+=.=+.  .=%+++++-:.==-.*=
=+*.*=.=+.-=#*%::    .     %+   =-++:-*. +%
%=*.#::#*#=::      :==-     +*- :--.@.  .+%
-#-.+-:+#.::**+++:.-* =::  .-+=  = =##:::%-
 =@:    +@#@+#.   =@@@=.  -+    -@@=@%. @-
  .++.   .+-+%***=+#:-..@.-=%+--%-=*%%. %
    -#    .=%- .::@+*@##@###@%#@@@@@@%. %
     =%:     ++-.#*    *=**#@*#@*@#@+*  %
       =++:.: --=+.+++=%   %-:*%+@**=   %
         :=#*.:=.:=...::::::::::...-  . %:
            :++==---. --:::-.   .=....: %-
                ::-++:::   ..       .  -#.
                     =%%%#-..       ..*#
                            =++++++++
"""

# --- LED onboard ---
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def init_input(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.DOWN
    return io

gp0 = init_input(board.GP0)
gp1 = init_input(board.GP1)
gp2 = init_input(board.GP2)
gp3 = init_input(board.GP3)

async def blink_task(stop_event, period=0.15):
    """Blink LED until stop_event is set."""
    while not stop_event.is_set():
        led.value = not led.value
        await asyncio.sleep(period)
    led.value = False

def shutdown(kbd, layout, timeShutdown = 0):
    # Win+R
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("shutdown /s /t " + str(timeShutdown))
    kbd.send(Keycode.ENTER)
    time.sleep(0.3)
    kbd.send(Keycode.ENTER)

def write_ascii(kbd, layout):
    # notepad + Enter
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("notepad")
    kbd.send(Keycode.ENTER)
    time.sleep(1.0)

    # write ASCII art
    layout.write("I got you !")
    kbd.send(Keycode.ENTER)
    layout.write(Ascii)

async def main():
   
    # Indicate mode with LED
    stop_blink = asyncio.Event()
    asyncio.create_task(blink_task(stop_blink, period=0.12))

    # Let USB settle
    await asyncio.sleep(2.0)

    kbd = Keyboard(usb_hid.devices, timeout=10)
    layout = KeyboardLayout(kbd)

    # Instant Shutdown on GP0
    if gp0.value:
        shutdown(kbd, layout)

    # Shutdown in 10 seconds on GP1, then write ASCII art
    if gp1.value:
        shutdown(kbd, layout, timeShutdown=20)
        await asyncio.sleep(2.0)
        write_ascii(kbd, layout)

    # Shutdown in 5 minutes on GP2
    if gp2.value:
        shutdown(kbd, layout, timeShutdown=300)

    # ASCII art only on GP3
    if gp3.value:
        await asyncio.sleep(2.0)
        write_ascii(kbd, layout)

    
    await asyncio.sleep(0.6)

    # Stop blink
    stop_blink.set()
    await asyncio.sleep(5.0)

    # Idle
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
