#  _ _ _                           ()                   
# ' ) ) )         /                /\                _/_
#  / / / __.  _. /_  o ____  __.  /  )  _. __  o _   /  
# / ' (_(_/|_(__/ /_<_/ / <_(_/|_/__/__(__/ (_<_/_)_<__ 
#                                              /        
#                                             '         
#+--------------------------------------------------------------------+
#|  MachinaScript for Robots v0.3.2024                                |
#|                                                                    |
#|  ..:: BRAIN MODULE ::..                                            |
#|                                                                    |
#|  This is the brain module, intended to be executed on a computer.  |
#|  You may need to customize this code for your own robotic mount.   |
#|                                                                    |
#|  Keep in mind this is just a very simple pipeline integration of   |
#|  many concepts together:                                           |
#|                                                                    |
#|  - The robot takes a picture from the environment,                 |
#|  uses a multimodal llm to generate a short "thoughtful analysis"   |
#|  on the environment and uses GROQ to generate ultra fast actions.  |
#|                                                                    |
#|  - A MachinaScript parser that translates JSON into serial         |
#|  for the Arduino;                                                  |
#|                                                                    |
#|  - A map for skills and motors you need to customize               |
#|  according to your project;                                        |
#|                                                                    |
#|  You are free to use and modify this piece of code,                |
#|  as well as to come up with something totally different.           |
#|                                                                    |
#|  This is an initial proof-of-concept, more examples coming soon.   |
#|                                                                    |
#|  Interested in contributing? Join the community!                   |
#|  See the github repo for more infos.                               |
#+--------------------------------------------------------------------+

# tip: if you have no idea what it all means, try pasting the contents
# of this file into GPT-4 or any other LLM and ask for a summary.
# Then you can start making your own modifications and modules precisely.

import base64
import requests
from groq import Groq
from openai import OpenAI
import cv2
import json
import serial
import time
import os
import pyttsx3

#╔════════════════ Initialize important code parts ═════════════════╗

# Mapping of motor names to their corresponding Arduino pins
motor_mapping = {
    "motor_neck_vertical": 3,
    "motor_neck_horizontal": 5,
    # Define additional motors and their Arduino pins here
}

# Define the serial connection to Arduino
arduino_serial = serial.Serial('COM3', 9600, timeout=1) #change COM3 with your arduino port
# arduino_serial = "/dev/ttyACM0"  # for Linux/Mac generally

# Initialize the text-to-speech engine
engine = pyttsx3.init()

#╚═════════════════════════════════════════════════════════════════╝

#╔═════════════════ Defining functions to be used ═════════════════╗
def capture_image(image_filename='image.jpg'):
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # '0' is usually the default value for the default camera.
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    ret, frame = cap.read()  # Capture a single frame
    if ret:
        cv2.imwrite(image_filename, frame)  # Save the captured frame to disk
        print("Image captured and saved as", image_filename)
    else:
        print("Failed to capture image")
    cap.release()  # Release the camera

# Encodes an image to base64.
def encode_image_to_base64(path):
    try:
        with open(path.replace("'", ""), "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error reading the image: {e}")
        exit()

# Sends the encoded image to the GPT4-VISION AI model for generating a thought / environment analysis.
# This example requires you to have access to GPT-4-Vision API. Make sure you have access.
# If you do not have access, or find it too expensive to run, 
# try out a very small local model using the "brain_groq_llava.py";
def get_image_thought(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the objects' positions in the image very shortly."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    thought = response.json()["choices"][0]["message"]["content"]
    print("Cognitive synthesis complete.")
    return thought

# Uses the Groq client to send the thought from the image analysis to generate a MachinaScript.
# More info about Groq limits: https://console.groq.com/docs/rate-limits
def generate_machina_script(thought):
    print("Compiling kinetic sequences...")
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

    # Combine the template and project specs with the new system prompt
    combined_content = machina_template + " " + project_specs

    # Generate text from Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": combined_content
            },
            {
                "role": "user",
                "content": "input: " + thought + 
                """
                note: output machinascript code only. 
                If you have to say anything else, do it on the *say* skill.
                """,
            }
        ],
        # Use a Groq supported model. Full list at https://console.groq.com/docs/models
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

# Parse and execute MachinaScript
def execute_machina_script(script):
    """Parses the MachinaScript and executes the actions by sending commands to Arduino."""
    actions = json.loads(script)["Machina_Actions"]
    for action_key, action in actions.items():
        # Check for 'movements' key and that it is not empty before execution
        if "movements" in action and action["movements"]:
            execute_movements(action["movements"])
        # Check for 'useSkills' key and that it is not empty before execution
        if "useSkills" in action and action["useSkills"]:
            execute_skills(action["useSkills"])

def execute_movements(movements):
    #Generates and sends the movement commands to the Arduino.
    for movement_key, movement in movements.items():
        for motor_name, details in movement.items():
            if motor_name in motor_mapping:
                pin = motor_mapping[motor_name]
                command = f"{pin},{details['position']},{details['speed']}\n"
                send_to_arduino(command)
                time.sleep(1)  # Adjust as needed for movement duration

def send_to_arduino(command):
    #Sends a command string to the Arduino via serial.
    print(f"Sending to Arduino: {command}")
    arduino_serial.write(command.encode())

# ==== Skills ====
#function to execute the skills if they come up in the machinascript output
def execute_skills(skills_dict):
    #Executes the defined skills.
    for skill_key, skill_info in skills_dict.items():
        if skill_key == "photograph":
            take_picture()
        elif skill_key == "blink_led":
            # Example skill, implementation would be similar to execute_movements
            print("Blinking LED (skill not implemented).")
        elif skill_key == "say":
            say(skill_info["text"])

#actual functions for the skills to be executed
def take_picture():
    #Simulates taking a picture.
    print("Taking a picture with the webcam and...")

def say(text):
    #Speaks the given text using text-to-speech.
    engine.say(text)
    engine.runAndWait()

# ===============

# Pipeline of encoding an image to base64, gets a thought from it, and then generates a MachinaScript.
def process_image(path):
    base64_image = encode_image_to_base64(path)
    thought = get_image_thought(base64_image)
    print("thought: " + thought)
    machina_script = generate_machina_script(thought)
    return machina_script

#╚═════════════════════════════════════════════════════════════════╝

#╔═════════════════ Main loop function ═════════════════╗
# Wake the fuck up, samurai.
if __name__ == "__main__":
    path = "image.jpg"

    # Boot Machinascript For Robots
    with open('msc.txt', 'r') as file:
        # Read the contents of the file
        file_contents = file.read()
    
        # Print the contents
        print(file_contents)

    # Start processing images in a loop
    while True:
        # Start processing the image:
        try:
            print("Starting pipeline.")
            capture_image()
            machina_script = process_image(path)
            cleaned_machina_script = machina_script.replace("\\", "")
            execute_machina_script(cleaned_machina_script)

            # Optionally, add here any other conditions or logic that
            # you may want to apply before the next iteration.

        except Exception as e:
            print(f"An error occurred while processing the image: {e}")

#╚══════════════════════════════════════════════════════╝

"""
⡿⡿⣻⢿⢿⢿⢿⢿⣿⣿⣿⠟⡋⠍⠊⠌⠌⠌⠂⠊⠄⠂⠙⠿⠻⡻⠻⢛⠻⠿⢿⣿⣿⣿⣿⢿⢿⢿⢿⣻
⣗⡽⡮⡷⣽⣺⣽⣿⣾⠟⠈⠄⠄⡀⢁⠂⢘⠈⡈⡠⠁⠄⢀⠘⠄⠄⠈⠄⠄⠄⠈⠈⠳⠻⣯⣿⣽⣞⣵⡳
⣗⢯⢫⢯⣷⡿⣽⠏⡁⠁⠄⠄⠄⢄⠅⠐⡂⠁⠁⠄⠄⠄⠐⡑⠄⠌⡄⠅⠄⡀⠄⠄⠄⠄⠘⢿⣻⣾⣳⢯
⣿⡴⣤⠅⢓⢹⢜⠁⡀⠄⠄⡡⠈⠂⡀⠄⠄⠄⠄⠄⠄⠄⠐⠘⢀⠄⠄⡀⠄⠠⠁⡀⠄⠄⠄⠄⠙⣿⣿⣟
⠿⢿⠻⢝⣿⡿⢢⢁⢀⢑⠌⠄⡈⠄⠄⠄⠄⢀⣰⣴⣴⣬⣄⣀⠂⠄⠂⠄⢀⠄⠄⠄⠄⠄⠄⠄⠄⢟⣿⣿
⡀⠄⠄⣸⣾⣛⢈⠄⢸⠐⠄⠨⠄⠄⠄⡀⣜⣞⣾⣿⣯⣿⣿⣿⣄⡀⢴⢼⣐⢬⠠⠄⠐⠄⠄⠄⠄⠘⣿⣿
⠋⣀⣵⣿⣽⡇⢃⢘⠜⠅⠈⠄⠄⢀⢔⣿⣿⣿⣿⣿⡿⣽⢾⢿⣳⢷⢿⡯⣷⣿⡌⠄⠄⠨⠄⠄⠄⠄⣻⣿
⠄⣿⣿⡟⣾⠇⢠⠧⠁⠄⠄⡀⠄⣰⣿⣿⣯⡏⣯⢿⢽⡹⣏⢿⡺⡱⢑⠽⡹⡺⣜⢄⠅⠄⠈⡀⠄⠄⢸⣿
⣾⣻⢳⣝⡯⢡⢹⣇⠄⠐⠄⠄⢠⣺⣿⣿⣿⢾⣿⢽⡵⣽⡺⣝⢎⢎⢶⢕⢌⢭⢣⢑⠄⠄⠄⠈⠄⠄⢸⣿
⣿⠧⢃⡳⠉⡈⢮⠃⠄⠄⠇⠄⣔⣿⣿⣿⣾⣿⣯⣯⢿⢼⡪⡎⡯⡝⢵⣓⢱⢱⡱⡪⡂⠄⠐⠄⠂⠄⠰⣿
⡿⢡⢪⠄⢰⠨⣿⠁⢈⣸⠄⠄⢿⢿⣻⢿⣽⣿⣿⣿⣿⣻⣮⢮⣯⣾⡵⣪⡪⡱⣹⣪⡂⠄⠄⢈⠄⠄⠄⣿
⣈⡖⡅⠄⢪⢴⢊⠁⢐⢸⠄⠄⡨⡢⡈⠈⠉⠻⢟⣷⡿⣟⢗⣽⡷⣿⢯⣞⣕⣧⣷⡳⠅⠄⠅⢐⠄⠄⠄⣿
⡣⡟⠜⠸⡁⣷⠁⠄⢅⢸⡀⠄⠄⠈⡀⠥⠄⡀⠄⠄⠈⠐⣷⡳⠙⠕⠩⠘⠁⠃⠁⠄⠄⠄⡂⢆⠄⠄⠄⣸
⣻⠍⠄⢣⣣⠏⠠⠐⠌⣪⠃⡐⢔⢌⡛⡎⡢⠄⢀⢄⢠⣳⣿⡎⠄⠄⢀⠤⠄⡈⠌⠊⠄⢀⠘⠨⠄⠄⠄⢸
⠑⠠⢂⢮⡳⠠⠂⠁⡅⡯⠐⢨⡺⡌⡯⡪⣞⣼⣵⡧⣟⣿⣿⣗⠄⠄⠐⡢⣒⢆⢐⢠⠁⠄⠄⠈⠄⠄⠄⢻
⢅⢢⠫⡫⠙⠨⠄⣃⢎⡗⢈⠰⠸⡸⡸⣝⣿⣿⡗⡽⣽⣿⣿⣿⠄⢐⣔⢽⣼⣗⣷⢱⠁⠄⠅⠁⠐⠄⠄⢾
⡵⣰⠏⡐⠱⡑⢨⡬⢻⡕⠐⠈⡪⡣⡳⡱⡳⠱⢍⣳⢳⣿⣿⣿⠄⢐⢵⢻⣳⣟⢎⠪⠄⠄⠐⠄⠄⠄⠄⣿
⡷⠁⡀⠄⠨⢂⣸⢉⠆⢑⠌⢠⢣⢏⢜⠜⡀⡤⣿⣿⣿⣿⣿⣟⠠⠄⠨⡗⡧⡳⡑⠄⠄⠄⠄⠄⠄⠄⠄⣿
⢖⠠⠄⢰⠁⢴⣃⠞⠄⠕⣈⣺⣵⡫⡢⣕⣷⣷⡀⠄⡈⢟⠝⠈⢉⡢⡕⡭⣇⠣⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿
⢻⡐⢔⢠⠪⡌⢌⠆⠐⢐⢨⣾⣷⡙⠌⠊⠕⠁⠄⠊⡀⠄⠠⠄⠡⠁⠓⡝⡜⡈⠄⠄⠄⠄⠄⠄⡮⡀⠄⣿
⠘⢨⢪⠼⠘⠅⠄⠂⠄⡀⢻⣿⣇⠃⠑⠄⠒⠁⢂⠑⡔⠄⠌⡐⠄⠂⠠⢰⡑⠄⠄⠄⠄⠄⠄⢠⣡⢱⣶⣿
⢢⢂⠫⡪⣊⠄⠣⡂⠂⡀⠨⠹⡐⣜⡾⡯⡯⢷⢶⢶⠶⣖⢦⢢⢪⠢⡂⡇⠅⠄⠄⠈⠄⢰⠡⣷⣿⣿⣿⣿
⢑⠄⠧⣟⡎⢆⡃⡊⠔⢀⠄⠈⣮⢟⡽⣿⣝⡆⠅⠐⡁⠐⠔⣀⢣⢑⠐⠁⡐⠈⡀⢐⠁⠄⠈⠃⢻⣿⣿⣿
⢑⠁⢮⣾⡎⢰⢐⠈⢌⢂⠐⡀⠂⡝⡽⣟⣿⣽⡪⢢⠂⡨⢪⠸⠨⢀⠂⡁⢀⠂⠄⢂⢊⠖⢄⠄⢀⢨⠉⠛
⡰⢺⣾⡗⠄⡜⢔⠡⢊⠢⢅⢀⠑⠨⡪⠩⠣⠃⠜⡈⡐⡈⡊⡈⡐⢄⠣⢀⠂⡂⡁⢂⠄⢱⢨⠝⠄⠄⠄⠄
"""