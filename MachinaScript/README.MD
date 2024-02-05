# MachinaScript For Robots - User Manual
Welcome, user! This is your guide for building LLM-powered robots in your garage.

To begin with a new project, you have to choose what framework you want to build your robot in:
- Machina1 - Simple MachinaScript Basics
- Machina2 - Autogen Agent-Based Robot (under development)

**note: Machina2 is still under early development. Recommended to start with Machina1.**

### Getting MachinaScript
1. Clone this repository
```
git clone https://github.com/babycommando/machinascript-for-robots.git
```

2. Browse the code to understand the architecture
```
MachinaBody -> the arduino code for the robot's body
MachinaBrain -> the computer code for the robot's brain
```

3. After cloning/downloading this repo, make sure you have the latest version of python 3 and the Arduino IDE.

## Getting Started: MACHINA1
Machina1 is a modular example that can grow into any project design.

![image](https://i.imgur.com/TOYmnXb.png)

## Robot FileSystem: Body and Brain
```
MACHINA1
  MachinaBody
    machinascript_body.ino //Arduino code
    test_serial.py //Tests program
  MachinaBrain
    brain_openai.py //powered by GPT3.5/4/4Vision
    brain_local_llms.py //powered by Local LLMs
    brain_huggingchat.py //powered by huggingchat unofficial api
    machinascript_language.txt //system prompt
    machinascript_language_large.txt //system prompt large
    machinascript_project_specs.txt //project specs
```

- The *machinascript_body.ino* represent all the things microcontroller/Arduino-related - sensors, motors, leds and serials.

- The *brain_(...).py* is where most of the work happens - query LLMs, parse the MachinaScript into serial and teach new skills for your robots. Choose the correct implementation for your project.

- *MachinaScript_Language.txt* the initial part of the system prompt. It contains basic understanding for the Ai to understand how to write in the MachinaScript JSON-based language format. You may only edit this part of the prompt if you want to speed up the process of prompt tokenization or modify the basics of the language itself based on your project. This may require changing the parsing functions in your python Brain file as well.

- *MachinaScript_Language.txt* 

- *MachinaScript_Project-Specs.txt* is where you will teach the Ai about your project specifications. You must edit this file after you finished implementing your body and brain code because they may contain variables and limitations in the code that the Ai may be unaware of. Example: servo motors can move 180 degrees, the normal pose is at 90 degrees. Note that the synthax in this is still in very early beta, so there is a lot of exploration ongoing for this part. It is important to make things clear and spend the less tokens possible to spare time and money on your project.

## Step 1: Assembling Your Robot
1. Hook two servos to your arduino as showed in the image above to be the `neck_horizontal` and `neck_vertical` servos, working as a `pan/tilt` base. With it you can test commands like ***"look up"*** or ***"say yes moving your head"***.

2. In your Arduino IDE choose the USB port you want to work and select your board, then test and inject the code in your little baby.

3. Testing your robot build:
  Test A) Test the code by sending serial commands via the arduino IDE in this format: `MotorID:degrees,speed;`.
    For example `A:45,10;B:0,10;` where:
      - `A and B` means the motors
      - `45 and 0`means the position in degrees for the motor to move to
      - `10 and 10` to be the velocity of the movement
      -`;` to be the separator that pipes multiple motors movements at the same time
  
  Test B) Test the code by sending serial commands via a python script `test_serial`.py
  Note: edit the code making sure to select the correct USB port.

## Step 2: Choosing a Brain For Your Unit
There are three kinds of brains currently to power your robot:
```
brain_openai.py //powered by GPT3.5/4/4Vision
brain_local_llms.py //powered by Local LLMs
brain_huggingchat.py //powered by huggingchat unofficial api
```
Choose the correct brain for your project design.

The brain module consists of several components that make the complete pipeline possible.

```
receive input -> LLM generates machinascript -> parse the machinascript for acions, movements and skills -> serialize to the body
```

During the LLM text generation, a piece text composed of two parts is added to the system prompt:
```
    machinascript_language.txt or machinascript_language_large.txt 
    +
    machinascript_project_specs.txt //project specs
```
Choose the correct language file for your project. Larger may produce more accurate results, but a bit slower because have more words to be tokenized.

### Declaring Project Specs
To define a set of "rules" your robot MUST follow, declare them on `machinascript_project_specs.txt`:
```
{
  "Motors": [
    {"id": "motor_neck_vertical", "range": [0, 180]},
    {"id": "motor_neck_horizontal", "range": [0, 180]}
  ],
  "Skills": [
    {"id": "photograph", "description": "Captures a photograph using an attached camera and send to a multimodal LLM."},
    {"id": "blink_led", "parameters": {"led_pin": 10, "duration": 500, "times": 3}, "description": "Blinks an LED to indicate action."}
  ],
  "Limitations": [
    {"motor": "motor_neck_vertical", "max_speed": "medium"},
    {"motor_speeds": ["slow", "medium", "fast"]},
    {"motors_normal_position": 90}
  ],
  "Personality": ["Funny", "delicate"],
  "Agency_Level": "high"
}
```
Note that the synthax in this is still in very early beta, so there is a lot of exploration ongoing for this part. You may write literally anything in any format you want. The JSON formatting is just to make it more human-readable.

### Skills: Function Calling the MachinaScript Way
During the parsing of the actions in the python code, skills can be ordered to be executed. 

You may declare skills as simple functions to be called when required.

```
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
```
Check the brain code for a complete example of skill usage.

---

#Getting Started: MACHINA2
Machina2 - the autogen agents-powered unit is still under active development and need some love from the contributors community. If you are getting started with MachinaScript try the MACHINA1. If you are interested in getting involved in the project don't hesitate to make your own designs and sharing out.

---

## Wrapping Up: Suggested Order For Building Robots

Starting with the arduino code, take a look at the template file included in this repo and modify it according to your project. Include any motors, ports and sensors as you like. In other words, start by making your robot move programatically before hooking it to an LLM to make sure the project works.

Proceed to editing the brain file and hooking with the arduino - map your project components and motors and pass them properly in the code. Then gently hook it with the serial arduino port. Try to make simple tests first, then you go complex. Explore new skills that only components could provide - for example radio frequency scan, RFID, infrared, web-related stuff... You name it.

Finally when you have the entire project set, teach the LLM how your robot works - pass all your specs in the MachinaScript_Project-Specs.txt and don't be afraid to explore new methods of doing it. In the file you will find a set of examples. We also recommend you having a quick read on the MachinaScript_Language.txt to understand better the synthax we initially came up with, however you may want to leave this intact for compatibility with the ready code parts in the body and brain.

If you are new to programming and have way too many questions, don't hesitate to paste the code on chatGPT-4 and ask about its structure as it may provide you some great insight for you to make your own modules. We really encourage you to get started debugging your code with the Ai pals.

Also reach us out in the github repo and in the discord group for bug reports and for sharing your projects!
