import board, digitalio, storage

gp15 = digitalio.DigitalInOut(board.GP15)
gp15.direction = digitalio.Direction.INPUT
gp15.pull = digitalio.Pull.DOWN

# If GP15 is not held high at boot, disable the USB drive
if not gp15.value:
    storage.disable_usb_drive()

