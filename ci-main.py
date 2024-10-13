import subprocess
from config import db_config   # import the db credentials from config.py
from time import sleep
import mysql.connector

output_path = f"/home/PI01/Desktop/Photo/image.jpg"
def capture_image():
    
    # Command to capture the image with libcamera-still
    command = [
        "libcamera-still", 
        "-o", output_path,  # Output file 
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

def binaryconversion(filename):
    with open(filename, 'rb') as file:
        binaryfile = file.read()
    return binaryfile


# Function to connect to the database and to create an object
def insert_into_database(capturejpg):
    # Connect to the server specified in config.py. This is done so that the connection credentials arent uploaded in the main code
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # SQL querry to insert values that werent specified yet into the table "emotions" with the collumn "img"
    query = """
    INSERT INTO emotions (img)
    VALUES (%s)
    """
    binaryimgfile = binaryconversion(capturejpg)

    # Execute the querry specified previously with the payload
    cursor.execute(query, (binaryimgfile))
    
    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Print the result
    print(f"BLOB inserted")

# Call the capture function
capture_image()
sleep(1)
insert_into_database("/home/PI01/Desktop/Photo/image.jpg")
