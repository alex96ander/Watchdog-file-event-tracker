import os
import time, glob
import smtplib
from email.message import EmailMessage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WATCH_FOLDER = os.getenv("WATCH_FOLDER")
SENDER = os.getenv("SENDER")
RECEIVER = os.getenv("RECEIVER")
APP_PASSWORD = os.getenv("APP_PASSWORD")
LOG_FILE = os.getenv("LOG_FILE")


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)


def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SENDER
        msg["To"] = RECEIVER
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, APP_PASSWORD)
            server.send_message(msg)

        log(f"Email sent successfully | Subject: {subject}")

    except smtplib.SMTPAuthenticationError:
        log("ERROR: Email authentication failed")

    except smtplib.SMTPException as e:
        log(f"SMTP ERROR: {e}")

    except Exception as e:
        log(f"UNKNOWN EMAIL ERROR: {e}")


def scan_existing_files():
    log("Scanning existing files...")
    try:
        all_files = glob.glob(os.path.join(WATCH_FOLDER, "**", "*"), recursive=True)

        files_found = False
        for path in all_files:
            if os.path.isfile(path):
                log(f"Existing file: {path}")
                files_found = True

        if not files_found:
            log("No files found in folder")
            # send_email("No Files Found",f"No files present in folder: {WATCH_FOLDER}")

    except Exception as e:
        log(f"ERROR during scanning: {e}")


class FolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            # print(event)
            if not event.is_directory:
                file_path = event.src_path
                log(f"New file: {file_path}")
                # send_email("New File Received",f"A new file was added:\n{file_path}")
        except Exception as e:
            log(f"ERROR in on_created: {e}")
            
    def on_deleted(self, event):
        try:
            if not event.is_directory:
                log(f"File deleted: {event.src_path}")

        except Exception as e:
            log(f"ERROR in on_deleted: {e}")


if __name__ == "__main__":

    log("***** SCRIPT STARTED *****")

    scan_existing_files()

    event_handler = FolderHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()

    log("Watchdog started")

    try:
        time.sleep(10)
    except Exception as e:
        log(f"ERROR during sleep: {e}")
    finally:
        observer.stop()
        observer.join()
        log("Watchdog observer stopped")

    log("***** SCRIPT TERMINATED *****\n")
