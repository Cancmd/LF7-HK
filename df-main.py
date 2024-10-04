import smbclient
import cv2  # OpenCV library for image handling
import numpy as np
from deepface import DeepFace

# Register the SMB client session
smbclient.register_session(server="192.168.178.65", username="smbuser", password="ChangeMe2024!")

# Function to read the image from SMB and analyze with DeepFace
def analyze_image_from_smb(smb_path):
    # Open the image from SMB as a binary stream
    with smbclient.open_file(smb_path, mode='rb') as file:
        # Read the image data
        image_data = file.read()
    
    # Convert binary data to a numpy array
    image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
    
    # Decode the image array to an OpenCV image format
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    # Use DeepFace to analyze the image
    results = DeepFace.analyze(img_path=image, actions=['age', 'gender', 'emotion', 'race'])
    
    return results

# Specify the SMB path to the .jpg file
smb_image_path = r"\\192.168.178.65\imgpool\image1.jpg"

# Analyze the image
analysis_results = analyze_image_from_smb(smb_image_path)
print(analysis_results)