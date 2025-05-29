# FIM (File Integrity Monitor)

This project is a simple File Integrity Monitor written in Python. It continuously monitors specified files for any changes by calculating and comparing their SHA-256 hashes. When a change is detected, it logs the event with a timestamp.

## Features

- Monitors a list of files for changes
- Uses SHA-256 hashing to detect modifications
- Logs all detected changes to `logs/file_changes.log`
- Automatically creates the log directory if it does not exist

## Usage

1. **Install Python dependencies**  
   (No external dependencies are required for the current version.)

2. **Configure files to monitor**  
   Edit the `files_to_monitor` list in [`fim.py`](fim.py) to include the files you want to watch.

3. **Run the monitor**  
   ```sh
   python fim.py
   ```

