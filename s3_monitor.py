import boto3
import configparser
import os
import time
import logging
from datetime import datetime, timedelta

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Get settings from config.ini
RUNNING_INTERVAL = int(config['settings']['running_interval'])
CLEANUP_INTERVAL = int(config['settings']['cleanup_interval'])
LOG_PATH = config['settings']['log_path']
UPLOADED_FILES_RECORD = config['settings']['uploaded_files_db']
BUCKET_NAME = config['aws']['bucket_name']
DIRECTORY_TO_WATCH = config['aws']['directory_to_watch']

# Set up logging
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s:%(message)s')

def upload_file_to_s3(file_path, bucket_name, s3_client):
    try:
        file_name = os.path.basename(file_path)
        
        # Get the file's modification date
        file_mod_time = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(file_mod_time)
        
        # Create the folder path based on the file date
        year = file_date.strftime('%Y')
        month = file_date.strftime('%m')
        s3_folder = f"{year}/{month}/"
        
        # The full S3 path will include the folder structure
        s3_path = s3_folder + file_name
        
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, s3_path)
        logging.info(f"Uploaded: {file_name} to {s3_path}")
        
        # Record the uploaded file
        record_uploaded_file(file_path)
    except Exception as e:
        logging.error(f"Upload failed: {file_name}, Error: {e}")

def record_uploaded_file(file_path):
    with open(UPLOADED_FILES_RECORD, 'a') as f:
        f.write(f"{file_path}\n")

def has_been_uploaded(file_path):
    if not os.path.exists(UPLOADED_FILES_RECORD):
        return False
    
    with open(UPLOADED_FILES_RECORD, 'r') as f:
        uploaded_files = f.read().splitlines()
        return file_path in uploaded_files

def monitor_folder(directory, bucket_name, s3_client):
    last_cleanup = datetime.now()

    while True:
        # Check for new files in the directory
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            
            if os.path.isfile(file_path) and not has_been_uploaded(file_path):
                upload_file_to_s3(file_path, bucket_name, s3_client)
        
        # Clean up the folder according to the cleanup interval
        if datetime.now() - last_cleanup >= timedelta(seconds=CLEANUP_INTERVAL):
            cleanup_folder(directory)
            last_cleanup = datetime.now()

        time.sleep(RUNNING_INTERVAL)  # Check for new files according to the running interval

def cleanup_folder(directory):
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Removed: {file_name}")
        # Clear the record of uploaded files after cleanup
        if os.path.exists(UPLOADED_FILES_RECORD):
            os.remove(UPLOADED_FILES_RECORD)
    except Exception as e:
        logging.error(f"Cleanup failed: {e}")

def main():
    s3_client = boto3.client('s3')

    monitor_folder(DIRECTORY_TO_WATCH, BUCKET_NAME, s3_client)

if __name__ == "__main__":
    main()
