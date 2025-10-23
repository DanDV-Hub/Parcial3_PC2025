# core.py
import subprocess
import pyautogui
import time
import logging
from datetime import datetime
from pathlib import Path

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def run_powershell(cmd):
    try:
        result = subprocess.run(["powershell", "-Command", cmd],
                                capture_output=True, text=True, timeout=10)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def take_screenshot(name):
    out = Path("out")
    out.mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = out / f"{name}_{ts}.png"
    img = pyautogui.screenshot()
    img.save(path)
    return path

def fill_form(data, start_coords):
    required_fields = ["nombre", "correo", "equipo"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Campo faltante o vacío: {field}")

    take_screenshot("before")
    pyautogui.click(start_coords[0], start_coords[1])
    pyautogui.typewrite(data["nombre"])
    pyautogui.press("tab")
    pyautogui.typewrite(data["correo"])
    pyautogui.press("tab")
    pyautogui.typewrite(data["equipo"])
    pyautogui.press("enter")
    take_screenshot("during")
    time.sleep(1)
    take_screenshot("after")
