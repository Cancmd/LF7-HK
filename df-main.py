import smbclient                # Handles the network drive 
import cv2                      # Library for working with imagefiles
import numpy as np              # Library for image conversion (the Image is converted into an array and decoded before being referenced by DeepFace)
from deepface import DeepFace   # Python Wrapper with a large variety of modules for machine learning facial recognition
import mysql.connector          # Module for connecting the script to the Database
import json                     # Module to interprete json arrays
from datetime import datetime   # Module for the date
from config import db_config    # imports the database connection function from config.py
from config import smb_config   # import the smb credentials from config.py


# Register the SMB client session
smbclient.register_session(**smb_config)

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

# Function to connect to the database and to create an object
def insert_into_database(analysis_result):
    # Connect to the server specified in config.py. This is done so that the connection credentials arent uploaded in the main code
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # SQL querry to insert values that werent specified yet into the table "emotions" with the collumns "dominant_emotion" and "timestamp"
    query = """
    INSERT INTO emotions (dominant_emotion, timestamp)
    VALUES (%s, %s)
    """
    
    # This pulls the current time | H M S are still not working - this might be due to the collumn properties 
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Execute the querry specified previously with the payload
    cursor.execute(query, (analysis_result, current_time))
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Print the result
    print(f"Inserted into database: {analysis_result} at {current_time}")

# Analyze the image
analysis_results = analyze_image_from_smb(smb_image_path)

# Insert the analysis result and current time into the database
insert_into_database(analysis_results)