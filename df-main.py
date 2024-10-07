import smbclient                # Handles the network drive 
import cv2                      # Library for working with imagefiles
import numpy as np              # Library for image conversion (the Image is converted into an array and decoded before being referenced by DeepFace)
from deepface import DeepFace   # Python Wrapper with a large variety of modules for machine learning facial recognition
import mysql.connector          # Module for connecting the script to the Database
import json                     # Module to interprete json arrays

# Register the SMB client session | This section needs to be updated!!!
smbclient.register_session(server="-", username="-", password="-")

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
    
    # Call Deepface to analyze the image. The "actions" parameter narrows down the response body to the one atribute we want
    results = DeepFace.analyze(img_path=image, actions=['emotion'])
    
    # Since we cant cant specify which of the emotion values we want we need to first turn the list into a json array
    jarray = json.dumps(results)
    # The json array then needs to be parsed
    jarrayparsed = json.loads(jarray)
    # In the return value of the function we can specify which value we need
    return jarrayparsed[0]["dominant_emotion"]

# Specify the SMB path to the .jpg file | This part needs to be reworked with either a directory scan and variable filenames or to run reguarly with the same filename (old ones would get overwriten)
smb_image_path = r"\\192.168.178.65\imgpool\image1.jpg"

# Analyze the image
analysis_results = analyze_image_from_smb(smb_image_path)
print(analysis_results)