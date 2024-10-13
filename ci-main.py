import subprocess
import smbclient                # Handles the network drive 
from config import smb_config   # import the smb credentials from config.py
from time import sleep

# Register the SMB client session
smbclient.register_session(**smb_config)
# Specify the SMB path to the .jpg file | This part needs to be reworked with either a directory scan and variable filenames or to run reguarly with the same filename (old ones would get overwriten)
smb_image_path = r"\\192.168.178.65\imgpool\image1.jpg"

def capture_image():
    
    # Command to capture the image with libcamera-still
    command = [
        "libcamera-still", 
        "-o", smb_image_path,  # Output file with unique name
        "--width", "1024",  # Resolution width
        "--height", "768",  # Resolution height
        "--brightness", "0.5"  # Adjust brightness if needed
    ]
    
    # Sleep to simulate a preview time
    print("Starting camera preview...")
    sleep(2)  # Sleep for 2 seconds to simulate camera warm-up/adjustment
    
    # Capture the image by running the libcamera-still command
    subprocess.run(command)
    print(f"Image captured and saved to {smb_image_path}")

# Call the capture function
capture_image()