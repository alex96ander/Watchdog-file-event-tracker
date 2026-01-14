import time
import os
from watchdog.observers import Observer
from dotenv import load_dotenv
from Folder_watch import scan_existing_files, FolderHandler
from logger import log, initialize_log
from datetime import datetime

load_dotenv()
WATCH_FOLDER = os.getenv("WATCH_FOLDER")

def main():
    
    initialize_log()
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log(f"Watcher Script STARTED | {timestamp}")
    log(f"******************************************************************")
    
    scan_existing_files()

    observer = Observer()
    observer.schedule(FolderHandler(), WATCH_FOLDER, recursive=True)
    observer.start()

    log("Watching started")

    try:
        time.sleep(20)
    except KeyboardInterrupt:
        log("Stopped by user")
    finally:
        observer.stop()
        observer.join()
        log("Watchdog observer stopped")

    log(f"Watcher Script Stopped | {timestamp}")
    log(f"******************************************************************")


if __name__ == "__main__":
    main()
