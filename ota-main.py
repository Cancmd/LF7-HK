import RPi.GPIO as GPIO
import time
import mysql.connector
from config import db_config  # Assuming db_config contains the MySQL credentials
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board
import busio

# GPIO setup for the LED
LED_PIN = 14  # Replace with the GPIO pin you've connected the LED to
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # Set the LED pin as output

# I2C setup for the OLED display (128x32)
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)  # 128x32 OLED display

# Clear the display at the start
display.fill(0)
display.show()

# Load a default font (ImageFont from Pillow)
font = ImageFont.load_default()

# Function to retrieve the latest dominant emotion from the database
def get_latest_emotion():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to get the latest entry with a non-null dominant emotion
    query = """
    SELECT dominant_emotion
    FROM emotions
    WHERE dominant_emotion IS NOT NULL
    ORDER BY id DESC
    LIMIT 1
    """
    cursor.execute(query)
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the dominant emotion (or None if no result)
    if result:
        return result[0]
    else:
        return None

# Function to control the LED based on the emotion
def control_led_based_on_emotion(emotion):
    if emotion == "happy":
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn the LED on
        print("LED ON (Happy detected)")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn the LED off
        print(f"Emotion detected: {emotion} - LED OFF")

# Function to display the emotion on the OLED screen
def display_emotion_on_oled(emotion):
    # Create a blank image for drawing
    width = display.width
    height = display.height
    image = Image.new("1", (width, height))  # Create a blank 1-bit image
    draw = ImageDraw.Draw(image)

    # Clear the screen
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Text to display
    text = f"Emotion: {emotion}"

    # Get text bounding box (instead of textsize), which returns (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # Draw the text on the image
    draw.text((x, y), text, font=font, fill=255)

    # Display the image on the OLED
    display.image(image)
    display.show()

# Main script logic
INTERVAL = 10  # Time interval in seconds

try:
    while True:
        # Get the latest emotion from the database
        latest_emotion = get_latest_emotion()

        if latest_emotion:
            print(f"Latest emotion: {latest_emotion}")
            
            # Control LED based on the emotion
            control_led_based_on_emotion(latest_emotion)
            
            # Display emotion on the OLED screen
            display_emotion_on_oled(latest_emotion)
        else:
            print("No emotion data available.")
        
        # Wait for the specified interval before the next check
        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("Script interrupted by user.")

finally:
    # Cleanup the GPIO settings before exiting
    GPIO.cleanup()
    # Clear the OLED display
    display.fill(0)
    display.show()
