import sys

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 10001

EMPTY_CHAR = "-"
LIVE_SHIP_CHAR = "*"
MISS_SHIP_CHAR = "%"
DEAD_SHIP_CHAR = "X"

DEFAULT_MAX_COUNT_SHIP_ON_BOARD = 6
DEFAULT_SIZE_BOARD = 5 # 5x5
EVERY_SECOND_WAIT_APPONENT = 5 # 5 second await apponent
MAX_COUNT_WAIT_APPONENT = 30 # 30 * EVERY_SECOND_WAIT_APPONENT seconds

if sys.platform == "linux" or sys.platform == "linux2":
    CLEAR_COMMAND = "clear"
elif sys.platform == "darwin":
    CLEAR_COMMAND = "clear"
elif sys.platform == "win32":
    CLEAR_COMMAND = "cls"
