#  _ _ _                           ()                   
# ' ) ) )         /                /\                _/_
#  / / / __.  _. /_  o ____  __.  /  )  _. __  o _   /  
# / ' (_(_/|_(__/ /_<_/ / <_(_/|_/__/__(__/ (_<_/_)_<__ 
#                                              /        
#                                             '         
#+------------------------------------------------------------------+
#|MachinaScript for Robots v0.1.2024                                |
#|                                                                  |
#|..:: BRAIN MODULE ::..                                            |
#|                                                                  |
#|This is the brain module, intended to be executed on a computer.  |
#|You may need to customize this code for your own robotic mount.   |
#|                                                                  |
#|Keep in mind this is just a very simple pipeline integration of   |
#|many concepts together:                                           |
#|                                                                  |
#|- Wake up word, followed by a voice command input from the user;  |
#|                                                                  |
#|- OpenAi implementation of the (newest) completions API,          |
#|teaching the system prompt to use the MachinaScript JSON-based    |
#|language;                                                         |
#|                                                                  |
#|- A MachinaScript parser that translates JSON into serial         |
#|for the Arduino;                                                  |
#|                                                                  |
#|- A map for skills and motors you need to customize               |
#|according to your project;                                        |
#|                                                                  |
#|You are free to use and modify this piece of code,                |
#|as well as to come up with something totally different.           |
#|                                                                  |
#|This is an initial proof-of-concept, more examples coming soon.   |
#|                                                                  |
#|Interested in contributing? Join the community!                   |
#|See the github repo for more infos.                               |
#+------------------------------------------------------------------+

# tip: if you have no idea what it all means, try pasting the contents
# of this file into GPT-4 or any other LLM and ask for a summary.
# Then you can start making your own modifications and modules precisely.

import json
import serial
import time
import speech_recognition as sr
import os
from openai import OpenAI
from groq import Groq

# Define the serial connection to Arduino
arduino_serial = serial.Serial('COM3', 9600, timeout=1)  #change COM3 with your arduino port
# arduino_serial = "/dev/ttyACM0"  # for Linux/Mac

# Mapping of motor names to their corresponding Arduino pins
motor_mapping = {
    "motor_neck_vertical": "A",
    "motor_neck_horizontal": "B",
    # Define additional motors and their Arduino pins here
}

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def listen_for_command():
    """Listens for a specific wake-up word and records the next spoken command."""
    with sr.Microphone() as source:
        print("Listening for the wake-up word 'hello robot' followed by your command.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            if "hello robot" in text:
                print("Wake-up word heard, what is your command?")
                audio = recognizer.listen(source)
                command_text = recognizer.recognize_google(audio)
                print(f"Command received: {command_text}")
                return command_text
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return None

def get_machina_script(command):
    """Queries the OpenAI API with the spoken command to generate a MachinaScript."""
    system_message = read_system_prompt()

    print("Compiling kinetic sequences...")
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    chat_completion = client.chat.completions.create(
        messages=[
            system_message,
            {
                "role": "user",
                "content": "input: " + command + " note: output machinascript code only. if you have to say anything else, do it on the *say* skill.",
            }
        ],
        # Use a Groq supported model.
        # Full list at https://console.groq.com/docs/models
        model="llama3-70b-8192",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


def read_system_prompt():
    """Reads instructions and project specifications from two files and prepares them for the LLM."""
    # Initialize an empty string to hold the combined content
    combined_content = ""
    
    # Read the first file (MachinaScript language instructions)
    with open('machinascript_language_large.txt', 'r') as file:
        combined_content += file.read() + "\n\n"  # Append file content with a newline for separation
    
    # Read the second file (Project specifications template)
    # Note: edit this file with your project specifications.
    with open('machinascript_project_specs.txt', 'r') as file:
        combined_content += file.read()  # Append second file content
    
    # Return the combined content in the expected format for the LLM
    return {"role": "system", "content": combined_content}

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
    """Generates and sends the combined movement commands to the Arduino."""
    # Initialize command strings for both motors
    commands_for_A = []
    commands_for_B = []

    # Translate speed from 'medium', 'slow', 'fast' to milliseconds or direct values
    speed_translation = {"slow": 30, "medium": 10, "fast": 4}

    for movement_key, movement in movements.items():
        if "motor_neck_vertical" in movement:
            # Add command for motor A
            speed_for_A = speed_translation[movement["speed"]]  # Translate speed
            commands_for_A.append(f"A:{movement['motor_neck_vertical']},{speed_for_A}")
        if "motor_neck_horizontal" in movement:
            # Add command for motor B
            speed_for_B = speed_translation[movement["speed"]]  # Translate speed
            commands_for_B.append(f"B:{movement['motor_neck_horizontal']},{speed_for_B}")

    # Combine commands for A and B
    combined_commands = ";".join(commands_for_A + commands_for_B) + ";" + "\n"

    # Send combined commands to Arduino
    send_to_arduino(combined_commands)
    time.sleep(1)  # Adjust as needed for movement duration

def execute_skills(skills_dict):
    """Executes the defined skills."""
    for skill_key, skill_info in skills_dict.items():
        if skill_key == "photograph":
            take_picture()
        elif skill_key == "blink_led":
            # Example skill, implementation would be similar to execute_movements
            print("Blinking LED (skill not implemented).")

def send_to_arduino(command):
    """Sends a command string to the Arduino via serial."""
    print(f"Sending to Arduino: {command}")
    arduino_serial.write(command.encode())

def take_picture():
    """Simulates taking a picture."""
    print("Taking a picture with the webcam...")

# Main function to listen for commands and process them
def main():
    while True:
        command = listen_for_command()
        if command:
            script = get_machina_script(command)
            execute_machina_script(script)

if __name__ == "__main__":
    main()
