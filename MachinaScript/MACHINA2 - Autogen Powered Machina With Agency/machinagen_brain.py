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

import json
import serial
import time
import speech_recognition as sr
import os
import autogen

## ARDUINO
# Define the serial connection to Arduino
arduino_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Mapping of motor names to their corresponding Arduino pins
motor_mapping = {
    "motor_neck_vertical": 3,
    "motor_neck_horizontal": 5,
    # Define additional motors and their Arduino pins here
}

## SPEECH RECOGNITION
# Initialize the speech recognizer
recognizer = sr.Recognizer()

## MACHINASCRIPT
# Teach LLMs how to use MachinaScript via the system prompt
def read_system_prompt():
    """Reads instructions and project specifications from two files and prepares them for the LLM."""
    # Initialize an empty string to hold the combined content
    combined_content = ""
    
    # Read the first file (MachinaScript language instructions)
    with open('machinascript_language.txt', 'r') as file:
        combined_content += file.read() + "\n\n"  # Append file content with a newline for separation
    
    # Read the second file (Project specifications template)
    # Note: edit this file with your project specifications.
    with open('machinascript_project_specifics.txt', 'r') as file:
        combined_content += file.read()  # Append second file content
    
    # Return the combined content in the expected format for the LLM
    return {"role": "system", "content": combined_content}

## AUTOGEN
# Initialize autogen with your MachinaScript skills
config_list = autogen.config_list_from_json(
    "oai_config_list.json",
    filter_dict={
        "model": ["gpt-4"]
    },
)

llm_config = {
    "config_list": config_list,
    "seed": 42,
    "functions": [
        {
            "name": "take_picture",
            "description": "Simulates taking a picture",
            "parameters": {}
        },
        {
            "name": "blink_led",
            "description": "Blinks an LED",
            "parameters": {}
        }
    ]
}

# Create a MachinaScript agent
machina_script_agent = autogen.AssistantAgent(
    name="machina_script_agent",
    system_message=read_system_prompt(),
    llm_config=llm_config
)

# Initialize autogen agents for vision and user input
config_list_vision = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)

vision_agent = autogen.MultimodalConversableAgent(
    name="vision-agent",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": config_list_vision, "temperature": 0.5, "max_tokens": 300},
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="A human admin.",
    human_input_mode="NEVER", #warning: setting human_input_mode to NEVER may create skynet-style unstoppable terminator depending on the llm you are using
    max_consecutive_auto_reply=0,
    code_execution_config={
        "use_docker": False
    }
)

# MAIN FUNCTION
# it listen for commands and process them.
def main():
    while True:
        command = listen_for_command()
        if command:
            process_command(command)

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

def process_command(command):
    """Processes the user command and generates MachinaScript actions."""
    generate_and_execute_machina_script(command)

def generate_and_execute_machina_script(command):
    """Generates a MachinaScript action for the specified skill and executes it."""
    machina_script = generate_machina_script(command)
    if machina_script:
        execute_machina_script(machina_script)

def generate_machina_script(command):
    """Generates a MachinaScript action based on the specified skill."""
    # Use autogen to generate MachinaScript based on the skill name
    machina_script = machina_script_agent.generate_machina_script(command)
    return machina_script

def execute_machina_script(script):
    """Parses the MachinaScript and executes the actions by sending commands to Arduino."""
    actions = json.loads(script)["Machina_Actions"]
    for action in actions:
        # Check for 'movements' key and that it is not empty before execution
        if "movements" in action and action["movements"]:
            execute_movements(action["movements"])
        # Check for 'useSkills' key and that it is not empty before execution
        if "useSkills" in action and action["useSkills"]:
            execute_skills(action["useSkills"])

def execute_movements(movements):
    """Generates and sends the movement commands to the Arduino."""
    for movement_key, movement in movements.items():
        for motor_name, details in movement.items():
            if motor_name in motor_mapping:
                pin = motor_mapping[motor_name]
                command = f"{pin},{details['position']},{details['speed']}\n"
                send_to_arduino(command)
                time.sleep(1)  # Adjust as needed for movement duration

def send_to_arduino(command):
    """Sends a command string to the Arduino via serial."""
    print(f"Sending to Arduino: {command}")
    arduino_serial.write(command.encode())

## SKILLS
def execute_skills(skills_dict):
    """Executes the defined skills."""
    for skill_key, skill_info in skills_dict.items():
        if skill_key == "take_picture":
            take_picture()
        elif skill_key == "blink_led":
            blink_led()

def take_picture():
    """Simulates taking a picture."""
    # skill to take pictures is yet to be implemented here
    print("Taking a picture with the webcam...")

def blink_led():
    """Blinks an LED."""
    # skill to blink led is yet to be implemented here
    print("Blinking LED...")

if __name__ == "__main__":
    main()
