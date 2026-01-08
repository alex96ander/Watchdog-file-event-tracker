from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.getenv("LOG_FILE")
STEP_COUNTER = 0

def initialize_log():
    global STEP_COUNTER
    STEP_COUNTER = 0
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

def log(message):
    global STEP_COUNTER
    STEP_COUNTER += 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] STEP {STEP_COUNTER}: {message}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)
