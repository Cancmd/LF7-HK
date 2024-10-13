import cv2                      # Library for working with image files
import numpy as np              # Library for image conversion
from deepface import DeepFace   # Python wrapper for machine learning facial recognition
import mysql.connector          # Module for connecting the script to the Database
import json                     # Module to interpret JSON arrays
from datetime import datetime   # Module for the date
from config import db_config    # Imports the database connection function from config.py

# Function to fetch rows with images where 'dominant_emotion' is NULL
def fetch_images_with_null_emotion():
    try:
        # Connect to the MySQL database using credentials from config.py
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to fetch rows where dominant_emotion is NULL
        query = """
        SELECT id, img FROM emotions WHERE dominant_emotion IS NULL
        """
        
        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()

        return results  # Returns a list of tuples (id, image_blob)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()


# Function to analyze the image using DeepFace
def analyze_image_from_blob(image_blob):
    # Convert the BLOB (binary data) to a numpy array
    image_array = np.asarray(bytearray(image_blob), dtype=np.uint8)
    
    # Decode the image array to an OpenCV image format
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    # Call DeepFace to analyze the image and detect emotion
    results = DeepFace.analyze(img_path=image, actions=['emotion'], enforce_detection=False)
    
    # Convert the DeepFace results into a JSON format
    jarray = json.dumps(results)
    
    # Parse the JSON array to extract the dominant emotion
    jarray_parsed = json.loads(jarray)
    return jarray_parsed[0]["dominant_emotion"]

# Function to update the database with the dominant emotion and timestamp
def update_emotion_in_db(image_id, dominant_emotion):
    try:
        # Connect to the MySQL database using credentials from config.py
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to update the dominant emotion and timestamp for a specific image ID
        query = """
        UPDATE emotions
        SET dominant_emotion = %s, timestamp = %s
        WHERE id = %s
        """
        
        # Fetch the current time in the DATETIME format
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Execute the query with the analysis result and timestamp
        cursor.execute(query, (dominant_emotion, current_time, image_id))
        
        # Commit the transaction
        conn.commit()

        # Print the result
        print(f"Updated image ID {image_id}: dominant_emotion = {dominant_emotion} at {current_time}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if conn.is_connected():
            cursor.close()
            conn.close()

# Main function to process images
def process_images():
    # Fetch the images where dominant_emotion is NULL
    images = fetch_images_with_null_emotion()

    if images:
        # Loop through each row
        for image_id, image_blob in images:
            print(f"Processing image ID {image_id}...")

            # Analyze the image to detect the dominant emotion
            dominant_emotion = analyze_image_from_blob(image_blob)

            # Update the database with the detected emotion
            update_emotion_in_db(image_id, dominant_emotion)
    else:
        print("No images with NULL dominant_emotion found.")

# Run the process
if __name__ == "__main__":
    process_images()
