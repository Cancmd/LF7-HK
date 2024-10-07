import smbclient                # Handles the network drive connection
import subprocess               # Runs shell commands from within the Python script
from time import sleep          # Pauses execution for a specified amount of time
from datetime import datetime   # Handles date and time functions

# Register the SMB client session | Provide server, username, and password for the SMB connection
smbclient.register_session(server="-", username="-", password="-")

# Define the path to the image on the network drive
smb_image_path = r"\\192.168.178.65\imgpool\image1.jpg"

def capture_image():
    """
    Captures an image using the libcamera-still command and saves it locally with a unique filename.
    After capturing, the image is uploaded to a network drive (SMB share).
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
    
    # Attempt to transfer the captured image to the SMB share
    try:
        # Open the image file on the SMB share in write-binary mode
        with smbclient.open_file(smb_image_path, mode='wb') as smb_file:
            # Open the local image file in read-binary mode and write it to the SMB share
            with open(output_path, 'rb') as local_file:
                smb_file.write(local_file.read())
        print(f"Image successfully copied to {smb_image_path}")
    except Exception as e:
        # Handle any exceptions during the file transfer process
        print(f"Failed to copy image to SMB share: {e}")

# Call the capture function to capture and transfer the image
capture_image()
