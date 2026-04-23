# Windows PC Shutdown / Rick Roll (Raspberry Pi Pico)

The Pico emulates a USB keyboard to trigger a Windows shutdown or open a Rick Astley YouTube link in Microsoft Edge. Inputs use pull-down resistors; drive the pin to 3V3 to enable a mode.

## Hardware used
- Raspberry Pi Pico W
- Micro USB cable
- Dupont jumper wire
- Resistor for pull-down (per input)
![image1](https://github.com/user-attachments/assets/2eda4abf-9943-4d0f-996c-f3f7a612090e)
![image2](https://github.com/user-attachments/assets/59bde83e-e670-4c38-8761-3cdb4eb2a399)

## Initial setup (flash + copy libs)
1) Flash CircuitPython: hold the Pico's BOOTSEL button, plug it in via USB, then drag `adafruit-circuitpython-raspberry_pi_pico_w-fr-10.0.3.uf2` onto the `RPI-RP2` drive. The board will reboot and mount as `CIRCUITPY`.
2) Copy project files: place `boot.py` and `code.py` at the root of `CIRCUITPY`.
3) Install required libraries: copy the `lib` folder to `CIRCUITPY` (contains `adafruit_hid/`, `asyncio/`, `adafruit_ticks.mpy`, `keyboard_layout_win_fr.py`, `keycode_win_fr.py`).
4) Safely eject the drive, then power-cycle or reset the Pico. The device will enumerate as a USB keyboard on next boot.

## Pin usage
- `GP0`: instant shutdown (`shutdown /s /t 0`).
- `GP1`: open Microsoft Edge on `https://www.youtube.com/watch?v=dQw4w9WgXcQ`.
- `GP2`: initialized in `code.py`, but currently has no action.
- `GP3`: initialized in `code.py`, but currently has no action.
- `GP15` (handled in `boot.py`): if this pin is **not** high at boot, the Pico's USB mass storage is disabled. Hold `GP15` to 3V3 before plugging in if you need the drive.
- Onboard LED: blinks during execution, then turns off when actions finish.

## Runtime flow (`code.py`)
1) LED blinks while USB enumerates (about 2 s).
2) HID keyboard and layout are initialized.
3) For each pin that is high (conditions are independent, they can combine):
   - `GP0` high: immediate shutdown.
   - `GP1` high: open Microsoft Edge with the Rick Astley YouTube URL.
   - `GP2` and `GP3` high: no action in the current code.
4) LED stops blinking and the loop idles.

