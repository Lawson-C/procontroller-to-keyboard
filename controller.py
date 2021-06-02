class GameController:
    def __init__(self):
        self.order = [
            [ 'Y', 'B', 'A', 'X', 'LB', 'RB', 'LT', 'RT' ], # row 0
            [ '-', '+', 'LSTICK', 'RSTICK', 'HOME', 'SCREEN'], # row 1
            ['DPAD'], # row 2
            ['LSTICK'], # row 3
            ['LSTICK'], # row 4
            ['RSTICK'], # row 5
            ['RSTICK'] # row 6
            ]
        self.buttons = {
            'A': Button('A', False),
            'B': Button('B', False),
            'X': Button('X', False),
            'Y': Button('Y', False),
            '+': Button('+', False),
            '-': Button('-', False),
            'LB': Button('LB', False),
            'RB': Button('RB', False),
            'LT': Button('LT', False),
            'RT': Button('RT', False),
            'DPAD': Hat('DPAD', False, 0),
            'HOME': Button('HOME', False),
            'LSTICK': Stick('LSTICK', False, 0, 0, 0.10),
            'RSTICK': Stick('RSTICK', False, 0, 0, 0),
            'SCREEN': Button('SCREEN', False)
        }

    def __button__(self, bID):
        return self.buttons[bID]
    
    def __update_buttons__(self, row, val):
        out = []
        if isinstance(val, int):
            data = bin(val)
        # buttons
        if row <= 1:
            for i in range(len(self.order[row])):
                b = self.buttons[self.order[row][i]]
                if len(data) >= i + 3:
                    chng = b.change(data[len(data) - i - 1] == '1')
                    out.append(b)
                else:
                    chng = b.change(False)
                    out.append(b)
        # dpad
        elif row == 2:
            b = self.buttons[self.order[row][0]]
            chng = b.change(val)
            out.append(b)
        # joysticks x
        elif row % 2 == 1: # rows 3 and 5
            b = self.buttons[self.order[row][0]]
            b.move_x((val - 127.5) / 127.5)
            out.append(self.buttons['LSTICK'] if row == 3 else self.buttons['RSTICK'])
        # joysticks y
        elif row % 2 == 0: # rows 4 and 6
            b = self.buttons[self.order[row][0]]
            b.move_y((val - 127.5) / 127.5)
            out.append(self.buttons['LSTICK'] if row == 4 else self.buttons['RSTICK'])
        return out
    
class Button(object):
    def __init__(self, bID, pressed):
        self.bID = bID
        self.pressed = pressed

    def change(self, press):
        changed = self.pressed == press;
        self.pressed = press
        return changed

    def __str__(self):
        return self.bID

class Hat(Button):
    def __init__(self, bID, pressed, val):
        self.val = 0
        super().__init__(bID, pressed)

    def change(self, val):
        changed = self.val == val
        self.val = val
        return changed

class Stick(Button):
    def __init__(self, bID, pressed, x, y, deadZone):
        self.x = x
        self.y = y
        self.deadZone = deadZone
        super().__init__(bID, pressed)

    def move_x(self, x):
        if abs(x) >= self.deadZone:
            self.x = x
        elif abs(x) < self.deadZone:
            self.x = 0

    def move_y(self, y):
        if abs(y) >= self.deadZone:
            self.y = y
        elif abs(y) < self.deadZone:
            self.y = 0

    def __in_range__(self):
        return abs(self.x) >= self.deadZone or abs(self.y) >= self.deadZone
