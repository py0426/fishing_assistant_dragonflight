import pyautogui as pg
import random
import time
from pyHM import mouse
from loguru import logger
from utility.interception_py.interception import *
from utility.key_codes import KEYBOARD_MAPPING
from win32api import GetSystemMetrics


class InputHelper:
    """Wrapper class to handle keyboard/mouse inputs based on input method."""
    def __init__(self, input_method, reaction_time_range, *args, **kwargs):
        self.INPUT_METHOD = input_method
        self.REACTION_TIME_RANGE = reaction_time_range

        if self.INPUT_METHOD == 'interception':
            self.driver = interception()
            self.mouse_driver = self.get_driver_mouse()
            self.keyboard_driver = self.get_driver_keyboard()
            self.screen_width = GetSystemMetrics(0)
            self.screen_height = GetSystemMetrics(1)


    def move_mouse(self, x, y):
        """Moves cursor to x,y on screen."""
        if self.INPUT_METHOD == 'virtual':
            time.sleep(random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
            try:
                mouse.move(x,y)
            except Exception:
                logger.warning('Failed to move mouse')
            time.sleep(random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
        elif self.INPUT_METHOD == 'interception':
            self.move_mouse_driver(x,y)
            pass
        elif self.INPUT_METHOD == 'arduino':
            pass


    def click_mouse(self):
        """Clicks mouse at current location."""
        if self.INPUT_METHOD == 'virtual':
            time.sleep(1 + random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
            try:
                mouse.click()
            except Exception:
                logger.warning('Failed to click mouse')
            time.sleep(1 + random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
        elif self.INPUT_METHOD == 'interception':
            self.click_mouse_driver()
        elif self.INPUT_METHOD == 'arduino':
            pass


    def press_key(self, key):
        """Presses key based on input type."""
        logger.info(f'Pressing key: {key}')
        if self.INPUT_METHOD == 'virtual':
            pg.keyDown(key)
            time.sleep(random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
            pg.keyUp(key)
        elif self.INPUT_METHOD == 'interception':
            self.press_key_driver(key)
        elif self.INPUT_METHOD == 'arduino':
            pass


    def get_driver_mouse(self):
        """Returns the first mouse device"""
        # loop through all devices and return the first mouse.
        mouse = 0
        for i in range(MAX_DEVICES):
            if interception.is_mouse(i):
                mouse = i
                return mouse

        # exit if we can't find a mouse.
        if (mouse == 0):
            logger.critical("No mouse found. Contact Gavin and disable the driver.")
            exit(0)


    def get_driver_keyboard(self):
        """Returns the first keyboard device"""
        # loop through all devices and return the first keyboard.
        for i in range(MAX_DEVICES):
            if interception.is_keyboard(i):
                keyboard = i
                return keyboard 


    def move_mouse_driver(self, x, y):
        """Moves the mouse to the screen coordinates and right clicks."""
        # we create a new mouse stroke, initially we use set right button down, we also use absolute move,
        # and for the coordinate (x and y) we use center screen
        mstroke = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_MOVE.value,
                                interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_ABSOLUTE.value,
                                0,
                                int((0xFFFF * x) / self.screen_width),
                                int((0xFFFF * y) / self.screen_height),
                                0)
        self.driver.send(self.mouse_driver,mstroke) # Move mouse


    def click_mouse_driver(self):
        """Moves the mouse to the screen coordinates and right clicks."""
        # we create a new mouse stroke, initially we use set right button down, we also use absolute move,
        # and for the coordinate (x and y) we use center screen
        x, y = pg.position()
        mstroke = mouse_stroke(interception_mouse_state.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN.value,
                                interception_mouse_flag.INTERCEPTION_MOUSE_MOVE_ABSOLUTE.value,
                                0,
                                int((0xFFFF * x) / self.screen_width),
                                int((0xFFFF * y) / self.screen_height),
                                0)
        self.driver.send(self.mouse_driver,mstroke) # we send the key stroke, now the right button is down
        # Add quick sleep so it's not instant
        time.sleep(random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
        mstroke.state = interception_mouse_state.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP.value # update the stroke to release the button
        self.driver.send(self.mouse_driver,mstroke) #button right is up


    def press_key_driver(self, hotkey):
        """Presses and releases the provided key"""
        # Get key code of hotkey to give to driver
        hotkey = KEYBOARD_MAPPING[hotkey]
        # Key down
        driver_press = key_stroke(hotkey, interception_key_state.INTERCEPTION_KEY_DOWN.value, 0)
        self.driver.send(self.keyboard_driver, driver_press)
        # Add quick sleep so it's not instant
        time.sleep(random.uniform(self.REACTION_TIME_RANGE[0], self.REACTION_TIME_RANGE[1]))
        # Key up
        driver_press.state = interception_key_state.INTERCEPTION_KEY_UP.value
        self.driver.send(self.keyboard_driver, driver_press)