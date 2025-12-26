from Folder_watch import scan_existing_files
from Folder_watch import FolderHandler
from watchdog.observers import Observer
from Folder_watch import log
from dotenv import load_dotenv
import time, os

load_dotenv()
WATCH_FOLDER = os.getenv("WATCH_FOLDER")

def main():
    log("***** SCRIPT STARTED *****")

    scan_existing_files()

    observer = Observer()
    observer.schedule(FolderHandler(), WATCH_FOLDER, recursive=True)
    observer.start()

    log("Watchdog started")

    try:
        time.sleep(10)
    except KeyboardInterrupt:
        log("Stopped by user")
    finally:
        observer.stop()
        observer.join()
        log("Watchdog observer stopped")

    log("***** SCRIPT TERMINATED *****\n")


if __name__ == "__main__":
    main()