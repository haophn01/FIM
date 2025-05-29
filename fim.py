import hashlib
import os
import time 

def calculate_file_hash(file_path):
  """Calculate and return the hash of the file."""
  hash_object = hashlib.sha256() # Create a new SHA-256 hash object
  with open(file_path,'rb') as file: # Open the file in binary mode
    file_data = file.read() # Read the file's content
    hash_object.update(file_data) # Add the file data to the hash
  return hash_object.hexdigest() # Return the hash as a string


files_to_monitor = ['watched_file.txt', 'requirements.txt'] # List of files to monitor

def monitor_files():
  """Monitor files for changes by comparing their hashes."""
  previous_hashes = {} # Dictionary to store previous hashes for each file
  
  while True: # This will make the code run continuously
    for file_path in files_to_monitor: # Loop through each file in the list
      if os.path.exists(file_path): # Check if the file exists
        current_hash = calculate_file_hash(file_path) # Get the current hash of the file
        # If the file's hash is different from the previous one, it has changed    
        if file_path not in previous_hashes or previous_hashes[file_path] != current_hash:
          print(f"File has changed: {file_path}") # Print that the file changed
          log_change(file_path) # Log the change
          previous_hashes[file_path] = current_hash #Update the stored hash for this file
        else: 
          print(f"No change detected for {file_path}") # Print that the file has not changed
    else: 
         print(f"File does not exist: {file_path}") # Print if the file doesn't exist
    time.sleep(5) # Wait for 5 second before checking again
    
    
def log_change(file_path):
  """Log the changes to a file in the log folder."""
  log_directory = 'logs' # The folder where we'll store the logs
  if not os.path.exists(log_directory): # Check if the folder exists
    os.makedirs(log_directory) # Create the folder if it doesn't exist

  log_file_path = os.path.join(log_directory,'file_changes.log') # Path to the log file
  
  with open(log_file_path, 'a') as log_file: # Open the log file in append mode
    log_file.write(f"{time.ctime()}: {file_path} has changed.\n") # Write the log with a timestamp
    
    
monitor_files()


print()