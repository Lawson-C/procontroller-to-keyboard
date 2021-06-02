import usb.core
import usb.util

import pyrobot
import mouse
import keyboard

import time

from controller import GameController

robot = pyrobot.Robot()

def __mouse__(b):
    if b.bID == 'RSTICK':
        mouse.move(5*b.x, 5*b.y, False, 0)    

def __keyboard__(b):
    s = b.bID
    if s == 'DPAD':
        s = str(b.val) + b.bID
        if s in translate:
            if translate[s][1:len(translate[s])] == 'scroll':
                if translate[s][0] == '+':
                    robot._scrollup()
                elif translate[s][0] == '-':
                    robot._scrolldown()
            elif translate[s].endswith('arrow'):
                keyboard.press_and_release(translate[s])
    elif s[1 : len(s)] == 'STICK' and s == 'LSTICK':
        if b.__in_range__():
            if b.y < 0:
                robot.press_and_release('w')
            elif b.y > 0:
                robot.press_and_release('s')
            if b.x > 0:
                robot.press_and_release('d')
            elif b.x < 0:
                robot.press_and_release('a')
    elif b.pressed:
        __press__(b)
    elif not b.pressed:
        __release__(b)

def __press__(b):
    s = ''
    if isinstance(b, str):
        s = b
    else:
        s = b.bID
    if not s in translate:
        return None
    if (translate[s] == 'right' or translate[s] == 'left') and not mouse.is_pressed():
        robot.click_mouse(translate[s])
    elif translate[s] != 'right' and translate[s] != 'left':
        try:
            robot.key_press(translate[s])
        except:
            try:
                keyboard.press(translate[s])
            except:
                try:
                    keyboard.write(translate[s])
                except:
                    print('uh oh press: ' + translate[s])

def __release__(b):
    s = ''
    if isinstance(b, str):
        s = b
    else:
        s = b.bID
    if not s in translate:
        return None
    if translate[s] == 'right' or translate[s] == 'left':
        agjfa = 9
        #robot.releasemoUse(translate[s])
    else:
        try:
            robot.key_release(translate[s])
        except:
            try:
                keyboard.release(translate[s])
            except:
                print('uh oh release: ' + translate[s])

# find our device
dev = usb.core.find(idVendor = 0x20D6, idProduct = 0xA711)

# was it found?
if dev is None:
    raise ValueError('Device not found')

#setup controller
controller = GameController()
dev.set_configuration()

translate = {
    'A':' ',
    'B':'ctrl',
    '+':'volume_up',
    '-':'volume_down',
    'RB':'enter',
    'RT':'left',
    'LT':'right',
    '0DPAD':'+scroll',
    '2DPAD':'right arrow',
    '4DPAD':'-scroll',
    '6DPAD':'left arrow',
    'HOME':'winleft',
    'SCREEN':'hbomax.com'
}

def main():
    run = 0
    start = time.monotonic()
    o = []
    while not controller.__button__('Y').pressed:
        po = o
        o = dev.read(0x81, 8, 100)
        while len(po) < len(o):
            po.append(None)
        for i in range(len(o) - 1):
            if o[i] != po[i] or i >= 3:
                bs = controller.__update_buttons__(i, o[i])
                for b in bs:
                    if b!= None:
                        __mouse__(b)
                        if int((time.monotonic() - start) / .0001) >= run:
                            __keyboard__(b)
                            run += 1
                        else:
                            exit
