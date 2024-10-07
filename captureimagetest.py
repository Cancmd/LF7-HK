import subprocess
from time import sleep
from datetime import datetime
from smb.SMBConnection import SMBConnection

def capture_image():
    # Generate a unique filename based on the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"photo_{current_time}.jpg"
    
    # Command to capture the image with libcamera-still
    command = [
        "libcamera-still", 
        "-o", output_filename,  # Output file with unique name
        "--width", "1024",  # Resolution width
        "--height", "768",  # Resolution height
        "--brightness", "0.5"  # Adjust brightness if needed
    ]
    
    # Sleep to simulate a preview time
    print("Starting camera preview...")
    sleep(2)  # Sleep for 2 seconds to simulate camera warm-up/adjustment
    
    # Capture the image by running the libcamera-still command
    subprocess.run(command)
    print(f"Image captured and saved as {output_filename}")
    
    # Set up SMB connection
    smb_server = '192.168.178.65'  # e.g., '192.168.1.100'
    share_name = 'imgpool'      # e.g., 'photos'
    username = 'smbuser'           # Your SMB username
    password = 'ChangeMe2024!'           # Your SMB password
    
    # Establish a connection to the SMB server
    conn = SMBConnection(username, password, "RaspberryPi", smb_server, use_ntlm_v2=True)
    conn.connect(smb_server)

    # Specify the path where you want to save the image
    remote_path = f"{share_name}/{output_filename}"
    
    # Write the captured image to the SMB share
    with open(output_filename, "rb") as local_file:
        conn.storeFile(share_name, output_filename, local_file)
    
    print(f"Image saved to SMB share at {remote_path}")

# Call the capture function
capture_image()
