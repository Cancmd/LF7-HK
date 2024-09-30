import subprocess
from time import sleep
from datetime import datetime

def capture_image():
    # Generate a unique filename based on the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = f"/home/sula/Desktop/Photo/photo_{current_time}.jpg"
    
    # Command to capture the image with libcamera-still
    command = [
        "libcamera-still", 
        "-o", output_path,  # Output file with unique name
        "--width", "1024",  # Resolution width
        "--height", "768",  # Resolution height
        "--brightness", "0.5"  # Adjust brightness if needed
    ]
    
    # Sleep to simulate a preview time
    print("Starting camera preview...")
    sleep(2)  # Sleep for 2 seconds to simulate camera warm-up/adjustment
    
    # Capture the image by running the libcamera-still command
    subprocess.run(command)
    print(f"Image captured and saved to {output_path}")

# Call the capture function
capture_image()
