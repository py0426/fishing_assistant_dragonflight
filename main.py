import sys
import time

from loguru import logger

from modules.InputHelper import ArduinoHelper
from modules.SettingsHelper import SettingsHelper
from modules.NewFishBot import FishingBot

# Initialize SettingsHelper
settings_helper = SettingsHelper()

if not settings_helper.settings['user'].getboolean('debug'):
    # Set log level to INFO
    logger.remove()
    logger.add(sys.stderr, level="INFO")

# Initialize Fishing Bot
fishing_bot = FishingBot(settings_helper=settings_helper)

# Start bot1
# bot class checks for breaks and input method internally
try:
    fishing_bot.run()
except KeyboardInterrupt:
    fishing_bot.break_helper.stop()  # Stop break helper thread
    sys.exit("Got keyboard interrupt. Exiting.")

# if __name__ == "__main__":
#     arduinoHelper = ArduinoHelper(settings_helper=settings_helper)
#     time.sleep(1)
#     arduinoHelper.move_mouse(500, 600)
#     # print("移动鼠标")
#     # time.sleep(2)
#     arduinoHelper.click_mouse("right")
#     # time.sleep(1)
#     # arduinoHelper.move_mouse(1200, 900)
#     # arduinoHelper.type_string("a")


