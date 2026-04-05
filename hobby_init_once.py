#!/usr/bin/env python3
import os
import time
from datetime import datetime

import serial

DEV = "/dev/ttyUSB0"
BAUD = 115200
LOG = "/var/log/hobby-init.log"


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%F %T')}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def wait_for_device() -> None:
    log(f"Warte auf {DEV} ...")
    while not os.path.exists(DEV):
        time.sleep(1)
    time.sleep(2)
    log(f"{DEV} gefunden")


def send(ser: serial.Serial, cmd: str) -> None:
    ser.write((cmd + "\n").encode("ascii"))
    ser.flush()
    log(f"TX {cmd}")


def main() -> None:
    os.makedirs("/var/log", exist_ok=True)
    wait_for_device()

    with serial.Serial(
        DEV,
        BAUD,
        timeout=0.2,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
    ) as ser:
        log(f"Port offen: {DEV} @ {BAUD}")
        time.sleep(1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        send(ser, "!sys")
        time.sleep(0.5)
        send(ser, "!sof")
        time.sleep(0.5)
        send(ser, "!gvl")

        log("Warte auf !end ...")
        deadline = time.time() + 20
        end_seen = False

        while time.time() < deadline:
            line = ser.readline().decode("utf-8", errors="replace").strip()
            if not line:
                continue
            if "!end" in line:
                end_seen = True
                break

        if end_seen:
            log("Initialisierung abgeschlossen (!end erkannt)")
        else:
            log("Warnung: !end nicht innerhalb Timeout erkannt")

        send(ser, "!son")
        time.sleep(1)
        log("Streaming aktiviert (!son gesendet)")
        log("Init abgeschlossen, Port wird geschlossen")


if __name__ == "__main__":
    main()
