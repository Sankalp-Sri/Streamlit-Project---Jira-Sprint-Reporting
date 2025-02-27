import logging
import os 
from datetime import datetime as dt 
from dir_path import base_path

LOG_FILE = f"{dt.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(base_path,"log_files",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s -%(message)s",
    level=logging.INFO,
)

if __name__ == "__main__":
    #logging.info("logging started")
    print(LOG_FILE_PATH)
