# Windows PC Shutdown (Raspberry Pi Pico)

The Pico emulates a USB keyboard to trigger a Windows shutdown or type an ASCII message. Inputs use pull-down resistors; drive the pin to 3V3 to enable a mode.

## Hardware used
- Raspberry Pi Pico W
- Micro USB cable
- Dupont jumper wire
- Resistor for pull-down (per input)

## Pin usage
- `GP0`: instant shutdown (`shutdown /s /t 0`).
- `GP1`: shutdown in 10 s, then open Notepad and type the ASCII art.
- `GP2`: shutdown in 5 minutes (`shutdown /s /t 300`).
- `GP3`: open Notepad and type the ASCII art only (no shutdown).
- `GP15` (handled in `boot.py`): if this pin is **not** high at boot, the Pico's USB mass storage is disabled. Hold `GP15` to 3V3 before plugging in if you need the drive.
- Onboard LED: blinks during execution, then turns off when actions finish.

## Runtime flow (`code.py`)
1) LED blinks while USB enumerates (about 2 s).
2) HID keyboard and layout are initialized.
3) For each pin that is high (conditions are independent, they can combine):
   - `GP0` high: immediate shutdown.
   - `GP1` high: shutdown in 10 s, wait 2 s, then write the ASCII art in Notepad.
   - `GP2` high: shutdown in 5 minutes.
   - `GP3` high: wait 2 s, then write the ASCII art in Notepad.
4) LED stops blinking and the loop idles.

