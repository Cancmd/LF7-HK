from smb.SMBConnection import SMBConnection  # Import pysmb for SMB connection
import subprocess               # Runs shell commands from within the Python script
from time import sleep          # Pauses execution for a specified amount of time
from datetime import datetime   # Handles date and time functions

# SMB connection setup
server_ip = "192.168.178.65"
share_name = "imgpool"
username = "-"
password = "-"
client_name = "client"  # Client name (can be any unique identifier)
server_name = "server"  # Server name (NetBIOS name of the server)

def capture_image():
    """
    Captures an image using the libcamera-still command and saves it locally with a unique filename.
    After capturing, the image is uploaded to a network drive (SMB share) using pysmb.
    """
    # Generate a unique filename based on the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"/home/sula/Desktop/Photo/photo_{current_time}.jpg"
