import time


def create_timeStamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def normalize_hex(s: str) -> str:
    s = s.replace("0x", "").replace(" ", "").replace(",", "")
    return s


def create_return(status: str, timestamp: str, error: str, message: dict) -> dict:
    ret = {"status": status, "timestamp": timestamp, "error": error, "message": message}
    return ret


def crc16_ccitt(data: bytes, poly=0x1021, init_val=0xFFFF) -> int:
    crc = init_val
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc
