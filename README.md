# S3 Uploader

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Boto3](https://img.shields.io/badge/Boto3-%3E%3D1.14-blue)

A Python-based utility that monitors a specified directory for new files, uploads them to an Amazon S3 bucket, and organizes them by date. The script runs as a systemd service and includes configurable options for periodic cleanup, logging, and file tracking.

## Features

- **Automated Monitoring:** Watches a directory for new files and uploads them to S3.
- **Date-Based Organization:** Files are organized in S3 by year and month based on their modification date.
- **Single Upload Guarantee:** Tracks uploaded files to ensure each file is uploaded only once.
- **Periodic Cleanup:** Configurable option to clean up the monitored directory periodically.
- **Configurable:** Easy-to-use `config.ini` file for customizing running intervals, cleanup schedules, log paths, and file tracking.

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/s3-uploader.git
cd s3-uploader
```

### 2. Install Dependencies

Ensure you have Python 3.8 or higher installed. Install the required Python packages using pip:

```bash
pip install boto3
```

### 3. Configure AWS CLI

Ensure your AWS CLI is configured with the correct credentials:

```bash
aws configure
```

### 4. Configure the Application

Copy the example configuration file and customize it for your setup:

```bash
cp config.ini.example config.ini
nano config.ini
```

Update the following fields in `config.ini`:
- **`running_interval`**: How often to check for new files (in seconds).
- **`cleanup_interval`**: How often to clean up the directory (in seconds).
- **`log_path`**: Path where the log file will be stored.
- **`uploaded_files_db`**: Path to the file that tracks uploaded files.
- **`bucket_name`**: Your Amazon S3 bucket name.
- **`directory_to_watch`**: Directory to monitor for new files.

### 5. Set Up the Systemd Service

To run the script as a service, copy the systemd service file to the appropriate directory:

```bash
sudo cp s3_uploader.service /etc/systemd/system/s3_uploader.service
```

Then, reload the systemd daemon, start the service, and enable it to start on boot:

```bash
sudo systemctl daemon-reload
sudo systemctl start s3_uploader.service
sudo systemctl enable s3_uploader.service
```

## Usage

Once the service is running, it will:
- Monitor the specified directory for new files.
- Upload new files to the configured S3 bucket, organizing them by year and month.
- Clean up the directory at the interval specified in `config.ini`.

### Logs

Logs are stored in the location specified in the `config.ini` file (`log_path`). You can view the logs with:

```bash
cat /var/log/s3_uploader.log
```

### Systemd Commands

To manage the service, use the following commands:

- **Start the service:**

  ```bash
  sudo systemctl start s3_uploader.service
  ```

- **Stop the service:**

  ```bash
  sudo systemctl stop s3_uploader.service
  ```

- **Check the service status:**

  ```bash
  sudo systemctl status s3_uploader.service
  ```

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests should be made against the `main` branch.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.