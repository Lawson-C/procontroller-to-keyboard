import mouse
from pyrobot import Robot

from controller import GameController
from procont_to_key import translate

gc = GameController()
r = Robot()

#tests buttons given a 8-bit byte
def test_buttons(byte):
    buttons = gc.__update_buttons__(0, byte)
    for b in buttons:
        if b.pressed:
            print(translate[b.bID])

#test right click
def right_trigger():
    test_buttons(0b10000000)

#test a click
def a():
    test_buttons(0b100)

#test right stick
def right_stick():
    rstick = gc.buttons['RSTICK']
    print('before')
    print((rstick.x, rstick.y))
    gc.__update_buttons__(5, -127.5)
    gc.__update_buttons__(6, 127.5)
    print('after')
    print((rstick.x, rstick.y))

def click():
    mouse.press('left')
    mouse.press('left')
    mouse.release('right')
