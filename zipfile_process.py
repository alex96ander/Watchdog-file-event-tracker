import os
import time
import glob
import zipfile
from datetime import datetime
from logger import log
from dotenv import load_dotenv

load_dotenv()
WATCH_FOLDER = os.getenv("WATCH_FOLDER")
# PROCESSED_ZIPS = set()

def unzip_file(zip_path):
    try:
        log(f"ZIP file: {zip_path}")
        
        if not zipfile.is_zipfile(zip_path):
            log("Invalid ZIP file path")
            return
        
        base_path = os.path.dirname(WATCH_FOLDER)
        today_date = datetime.now().strftime("%Y-%m-%d") 
        output_folder = os.path.join(base_path, "unzippedfiles", today_date)
        os.makedirs(output_folder, exist_ok = True)   
        
        log(f"Unzip target folder: {output_folder}")
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_folder)
        log("ZIP extraction completed")
        
    except Exception as e:
        log(f"ZIP extraction error: {e}")
        
         