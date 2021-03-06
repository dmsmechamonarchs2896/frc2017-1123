from wpilib import Joystick, XboxController
from wpilib.buttons.joystickbutton import JoystickButton

import robotmap

joystick = None
controller = None
start_btn = None
divider = None


def init():
    """
    Initialize operator input (OI) objects.
    """
    global joystick, controller, start_btn, divider

    joystick = Joystick(robotmap.joystick.port)
    controller = XboxController(robotmap.joystick.port)

    start_btn = JoystickButton(joystick, 7)

    divider = 1
