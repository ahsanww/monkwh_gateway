from app.utils import util
from app.data.Constant import *


def parse_lora_frame(rawData: bytes):
    crc = util.crc16_ccitt(rawData)
    print(crc)


def build_lora_frame(rawData: bytes):
    crc = util.crc16_ccitt(rawData)
    print(crc)
