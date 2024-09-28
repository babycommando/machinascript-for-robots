print("""
  _ _ _                           ()                   
 ' ) ) )         /                /\                _/_
  / / / __.  _. /_  o ____  __.  /  )  _. __  o _   /  
 / ' (_(_/|_(__/ /_<_/ / <_(_/|_/__/__(__/ (_<_/_)_<__ 
                                              /        
                                             '         
MachinaScript for Robots v0.3 
Apache License 2024 - Made by Babycommando.
      """)
# +--------------------------------------------------------------------+
# |  MachinaScript for Robots v0.3                               |
# |                                                                    |
# |  ..:: BRAIN MODULE ::..                                            |
# |                                                                    |
# |  This is the brain module, intended to be executed on a computer.  |
# |  You may need to customize this code for your own robotic mount.   |
# |                                                                    |
# |  Keep in mind this is just a very simple pipeline integration of   |
# |  many concepts together:                                           |
# |                                                                    |
# |  - The robot takes a picture from the environment,                 |
# |  uses a multimodal llm to generate a short "thoughtful analysis"   |
# |  on the environment and uses GROQ to generate ultra fast actions.  |
# |                                                                    |
# |  - A MachinaScript parser that translates JSON into serial         |
# |  for the Arduino;                                                  |
# |                                                                    |
# |  - A map for skills and motors you need to customize               |
# |  according to your project;                                        |
# |                                                                    |
# |  You are free to use and modify this piece of code,                |
# |  as well as to come up with something totally different.           |
# |                                                                    |
# |  This is an initial proof-of-concept, more examples coming soon.   |
# |                                                                    |
# |  Interested in contributing? Join the community!                   |
# |  See the github repo for more infos.                               |
# +--------------------------------------------------------------------+

import base64
from groq import Groq
import cv2
import json
import serial
import time
import os
import pyttsx3

# ╔════════════════ Initialize important code parts ═════════════════╗
# Mapping of motor names to their corresponding Arduino pins
motor_mapping = {
    "motor_neck_vertical": 3,
    "motor_neck_horizontal": 5,
    # Define additional motors and their Arduino pins here
}

# Define the serial connection to Arduino
# change COM3 with your Arduino port
arduino_serial = serial.Serial('COM3', 9600, timeout=1)
# arduino_serial = "/dev/ttyACM0"  # for Linux/Mac generally

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# ╚═════════════════════════════════════════════════════════════════╝

# ╔═════════════════ Defining functions to be used ═════════════════╗
def capture_image(image_filename='image.jpg'):
    """Captures an image using the default camera and saves it to the specified filename."""
    cap = cv2.VideoCapture(
        0)  # '0' is usually the default value for the default camera.
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    ret, frame = cap.read()  # Capture a single frame
    if ret:
        cv2.imwrite(image_filename, frame)  # Save the captured frame to disk
        print("Image captured and saved as", image_filename)
    else:
        print("Failed to capture image")
    cap.release()  # Release the camera


def encode_image_to_base64(path):
    """Encodes an image file to base64 format."""
    try:
        with open(path.replace("'", ""), "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error reading the image: {e}")
        exit()

# Function to generate MachinaScript using Groq Llama 3.2 model
def generate_machina_script(base64_image):
    print("Generating MachinaScript actions based on what the robot sees...")
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    try:
        # Get MachinaScript Template
        with open('prompts/machinascript_language_large.txt', 'r') as file:
            machina_template = file.read()
    
        # Get Project Specs
        with open('prompts/machinascript_project_specs.txt', 'r') as file:
            project_specs = file.read()

    except FileNotFoundError as e:
        print(f"Error opening the file: {e}")
        return
      
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                  #pass the txt files to the prompt
                    {"type": "text", "text": machina_template + "\n" + project_specs},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        model="llama-3.2-11b-vision-preview",
        response_format={"type": "json_object"}
    )
    print("MachinaScript generated:",
          chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

# Parse and execute MachinaScript
def execute_machina_script(script):
    """Parses the MachinaScript and executes the actions by sending commands to Arduino."""
    try:
        actions = json.loads(script)["Machina_Actions"]
        for action_key, action in actions.items():
            # Check if action is a dictionary
            if not isinstance(action, dict):
                print(f"Unexpected action format: {action}")
                continue

            # Check for 'movements' key and that it is a dictionary
            if "movements" in action and isinstance(action["movements"], dict):
                execute_movements(action["movements"])
            else:
                print(f"No valid movements found in action {action_key}.")

            # Check for 'useSkills' key and that it is a dictionary
            if "useSkills" in action and isinstance(action["useSkills"], dict):
                execute_skills(action["useSkills"])
            else:
                print(f"No valid skills found in action {action_key}.")

    except json.JSONDecodeError as e:
        print(f"Error parsing MachinaScript JSON: {e}")
    except KeyError as e:
        print(f"Missing expected key in MachinaScript: {e}")
    except TypeError as e:
        print(f"Type error while executing MachinaScript: {e}")

def execute_movements(movements):
    """Generates and sends the movement commands to the Arduino."""
    if not isinstance(movements, dict):
        print(f"Unexpected movements format: {movements}")
        return

    for movement_key, movement in movements.items():
        if not isinstance(movement, dict):
            print(f"Unexpected movement format: {movement}")
            continue

        for motor_name, details in movement.items():
            # Normalize details if it's not already a dictionary
            if isinstance(details, int):
                # Assume it's a position; set a default speed
                details = {"position": details, "speed": "medium"}
            elif isinstance(details, str):
                # Assume it's a speed command without position, set a default position
                details = {"position": 90, "speed": details}
            elif not isinstance(details, dict):
                print(f"Invalid motor details format: {details}")
                continue

            if motor_name in motor_mapping:
                pin = motor_mapping[motor_name]
                try:
                    # Validate details before accessing keys
                    position = details.get('position', None)
                    speed = details.get('speed', 'medium')
                    if isinstance(position, int) and isinstance(speed, str):
                        command = f"{pin},{position},{speed}\n"
                        print("Executing: ", command)
                        send_to_arduino(command)
                        time.sleep(1)  # Adjust as needed for movement duration
                    else:
                        print(f"Invalid data types in details: {details}")
                except KeyError as e:
                    print(f"Missing key in movement details: {e}")

def send_to_arduino(command):
    """Sends a command string to the Arduino via serial."""
    print(f"Sending to Arduino: {command}")
    arduino_serial.write(command.encode())

# ==== Skills ====
def execute_skills(skills_dict):
    """Executes the defined skills based on the MachinaScript output."""
    for skill_key, skill_info in skills_dict.items():
        if skill_key == "photograph":
            take_picture()
        elif skill_key == "blink_led":
            print("Blinking LED (skill not implemented).")
        elif skill_key == "say":
            text = skill_info.get("parameters", {}).get("text", "No text provided.")
            print(f"Executing: Saying '{text}'")
            say(text)

def take_picture():
    """Simulates taking a picture."""
    print("Taking a picture with the webcam and...")


def say(text):
    """Speaks the given text using text-to-speech."""
    engine.say(text)
    engine.runAndWait()

# ══════════════

# Main function to process an image and generate MachinaScript
def process_image(path):
    base64_image = encode_image_to_base64(path)
    machina_script = generate_machina_script(base64_image)
    return machina_script


# ╔═════════════════ Main loop function ═════════════════╗
if __name__ == "__main__":
    path = "image.jpg"

    # Start processing images in a loop
    while True:
        try:
            print("Starting pipeline.")
            capture_image(path)
            machina_script = process_image(path)
            cleaned_machina_script = machina_script.replace("\\", "")
            execute_machina_script(cleaned_machina_script)
        except Exception as e:
            print(f"An error occurred while processing the image: {e}")

# ╚══════════════════════════════════════════════════════╝
