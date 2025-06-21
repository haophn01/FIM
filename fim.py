import hashlib
import os
import time 
import datetime

files_to_monitor = ['watched_file.txt', 'requirements.txt'] # List of files to monitor

# Exclusion lists
excluded_extensions = ['.log', '.tmp']
excluded_directories = ['logs', 'temp']


def is_excluded(file_path):
    # Check extension
    _, ext = os.path.splitext(file_path)
    if ext in excluded_extensions:
        return True
    # Check if file is in an excluded directory
    for ex_dir in excluded_directories:
        if os.path.commonpath([os.path.abspath(file_path), os.path.abspath(ex_dir)]) == os.path.abspath(ex_dir):
            return True
    return False
  

def calculate_file_hash(file_path):
  """Calculate and return the hash of the file."""
  hash_object = hashlib.sha256() # Create a new SHA-256 hash object
  with open(file_path,'rb') as file: # Open the file in binary mode
    file_data = file.read() # Read the file's content
    hash_object.update(file_data) # Add the file data to the hash
  return hash_object.hexdigest() # Return the hash as a string


def log_change(file_path):
    """Log the changes to a file in the log folder."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, 'file_changes.log')
    limit_size = 1 * 1024  # 3KB

    # Rotate log if needed before every write
    if os.path.exists(log_file) and os.path.getsize(log_file) > limit_size:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        rotated_log = os.path.join(log_dir, f'file_changes_{timestamp}.log')
        os.rename(log_file, rotated_log)

    with open(log_file, 'a') as f:
        f.write(f"{time.ctime()}: {file_path} has changed.\n")
        f.write(f"{os.stat(file_path)}\n")
        
        
def monitor_files():
    """Monitor files for changes by comparing their hashes."""
    previous_hashes = {}  # Stores previous hashes for each file
    while True:
        for file_path in files_to_monitor:
            if is_excluded(file_path):
                print(f"Excluded from monitoring: {file_path}")
                continue
            if os.path.exists(file_path):
                current_hash = calculate_file_hash(file_path)
                # Log and update hash only if the file has changed
                if file_path not in previous_hashes or previous_hashes[file_path] != current_hash:
                    print(f"File has changed: {file_path}")
                    log_change(file_path)
                    previous_hashes[file_path] = current_hash
                else:
                    print(f"No change detected for {file_path}")
            else:
                print(f"File does not exist: {file_path}")
        time.sleep(5)  # Wait before checking again

monitor_files()


'''

Challenge 2: Create a File Exclusion List

Sometimes we don’t want to monitor certain files or directories. Imagine you want to exclude files like .log or .tmp files, or perhaps files in a specific directory.

Challenge:

Modify the program to allow the user to specify a list of file types or specific directories to exclude from being monitored.
You’ll need to learn how to check the file extensions (like .txt, .log, etc.) and the directory the file is in.
Hint: The os.path.splitext() function can be helpful for getting the file extension.
Challenge 3: Implement Logging with Log Rotation

Imagine if the file changes every minute, and your log file keeps growing. It will eventually become too large to manage. We can prevent this by implementing log rotation.

Challenge:

Implement log rotation in the log file. When the log file reaches a certain size (for example, 1MB), create a new log file and start logging to the new file. You can name the new log file using the current timestamp so that each file has a unique name.
Hint: You will need to use the os.path.getsize() function to check the size of the log file, and datetime to get the current time.
Challenge 4: Track the File’s Previous Hash and Display Only Changes

Instead of simply printing when the file changes, let’s make it more useful by storing a history of changes for each file.

Challenge:

Modify the program so that when a file’s hash changes, it logs the previous hash as well, so you can compare the old and new values.
This way, you’ll have a complete history of what the file looked like at each change.
Hint: Use a dictionary to store each file’s hash history, with the file path as the key and a list of hashes as the value.
'''