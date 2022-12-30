from enum import Enum

PROJECT_DIR = __file__.replace("/lib/config.py", "")


class HistoricalPrice(Enum):
    TIME_FRAME = 1  # second
    CHANNEL_WIDTH = 30


class DATABASE(Enum):
    class TRADINGBOT(Enum):
        HOST = 'localhost'
        USER = '*********'
        PASSWORD = '*********'
        DATABASE = '*********'


class Bitflyer(Enum):
    class Api(Enum):
        KEY = "*********"
        SECRET = "*********"


class DirPath(Enum):
    PROJECT = PROJECT_DIR


class FilePath(Enum):
    WARNING_MP3 = PROJECT_DIR + "/sound/WARNING.mp3"
    ERROR_MP3 = PROJECT_DIR + "/sound/ERROR.mp3"
    SYSTEM_LOG = PROJECT_DIR + "/log/system.log"
    AA = PROJECT_DIR + "/document/AA.txt"
