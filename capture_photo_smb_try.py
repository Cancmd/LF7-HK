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
    
    # Command to capture the image using libcamera-still
    command = [
        "libcamera-still", 
        "-o", output_path,  # Output file with unique name
        "--width", "1024",  # Resolution width
        "--height", "768",  # Resolution height
        "--brightness", "0.5"  # Adjust brightness if needed
    ]
    
    # Simulate a short camera preview before capturing the image
    print("Starting camera preview...")
    sleep(2)  # Sleep for 2 seconds to simulate camera warm-up/adjustment
    
    # Capture the image by executing the libcamera-still command
    subprocess.run(command)
    print(f"Image captured and saved to {output_path}")
    
    # SMB file transfer setup using pysmb
    try:
        # Establish SMB connection
        conn = SMBConnection(username, password, client_name, server_name, use_ntlm_v2=True)
        assert conn.connect(server_ip, 139)  # Port 139 is for SMB
        
        # Transfer the file to the SMB share
        with open(output_path, 'rb') as local_file:
            conn.storeFile(share_name, "image1.jpg", local_file)
        
        print(f"Image successfully copied to SMB share {share_name}")
        
    except Exception as e:
        # Handle exceptions during the file transfer process
        print(f"Failed to copy image to SMB share: {e}")

# Call the capture function to capture and transfer the image
capture_image()
