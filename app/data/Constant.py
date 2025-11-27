from enum import IntEnum
from typing import Final, Dict, Tuple
from dotenv import load_dotenv
import os

# user = os.getenv("USER")
# load_dotenv(f"/home/{user}/dms/.env")

# DFR_DIR = os.getenv("DFR_DIR")

STX = b"\xaa"  # START OF TEXT
ETX = b"\xbb"  # END OF TEXT


class STATUS_API(IntEnum):
    OK = 0
    ERROR = 1
    TIMEOUT = 2
    BAD_FORMAT = 3


class CMD_TYPE:
    """
    COMMAND TYPE DATA:
        0x00 : STATUS
        0x01 : INSTANT DATA
        0x02 : LOAD PROFILE DATA
        0x03 : MONTHLY PROFILE DATA

    COMMAND TYPE CONTROL:
        0x11 : RELAY OUTPUT CONTROL
    """

    CMD_STATUS: Final[bytes] = 0x00
    CMD_INSTANT: Final[bytes] = 0x01
    CMD_LOADPROFILE: Final[bytes] = 0x02
    CMD_MONTHPROFILE: Final[bytes] = 0x03

    CMD_CONTROL_RELAY: Final[bytes] = 0x11
