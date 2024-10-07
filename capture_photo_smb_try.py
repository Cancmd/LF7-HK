import subprocess
from time import sleep
from datetime import datetime
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.file import File

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
    
    # Connect to the SMB server
    connection = Connection(uuid='my-connection', server=smb_server)
    connection.connect()
    
    session = Session(connection, username, password)
    session.connect()
    
    # Specify the share and path where you want to save the image
    remote_path = f'\\{share_name}\\{output_filename}'
    
    # Open the file on the SMB share
    with File(session, remote_path, "w") as remote_file:
        # Read the captured image file and write it to the remote file
        with open(output_filename, "rb") as local_file:
            remote_file.write(local_file.read())
    
    print(f"Image saved to SMB share at {remote_path}")

# Call the capture function
capture_image()
