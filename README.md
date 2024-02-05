![MachinaScript For Robots](https://github.com/babycommando/machinascript/assets/71618056/9cf321ae-187f-414d-84a2-c2690c78394a)
![example – 2](https://github.com/babycommando/machinascript/assets/71618056/c00c28eb-20e2-466e-8991-62a821cc2408)
![example – 3](https://github.com/babycommando/machinascript/assets/71618056/f4e3f545-a4f6-4731-bbb9-474b75670b7f)
![example](https://github.com/babycommando/machinascript/assets/71618056/5ef748bc-8334-4e10-99bd-19dcc6229021)
![example – 4](https://github.com/babycommando/machinascript-for-robots/assets/71618056/2c18b953-bf94-4559-825a-da5fd5c61295)
![example – 7](https://github.com/babycommando/machinascript-for-robots/assets/71618056/a6cd7442-2705-49fc-87ed-263b809feb1d)

# Patch 0.2 - Presenting Machina2: Autogen Self-Controlled Robots
![Prancheta – 3](https://github.com/babycommando/machinascript-for-robots/assets/71618056/45e63e99-14d3-45a7-be26-fe0f6b6b6b65)

<br>

<h1 align="center">
  <br>
  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="https://github.com/babycommando/machinascript-for-robots/assets/71618056/f03cd787-6ead-4414-bc54-b0628faa29a8" alt="Markdownify" width="200"></a>
  <br>
  MachinaScript For Robots (early beta)

  <br>
</h1>

<h4 align="center">Build modular ai-powered robots in your garage right now.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.2.1-limegreen">
  <a href="https://discord.gg/2GqU225n"><img src="https://discordapp.com/api/guilds/1202776762820468806/widget.png?style=shield" alt="Discord"/></a>
  <a href="https://ko-fi.com/babycommando">
    <img src="https://img.shields.io/badge/$-donate-ff69b4.svg?maxAge=2592000&amp;style=flat">
  </a>
</p>

<p align="center">
  <a href="#meet-machinascript-for-robots">Intro</a> •
  <a href="#a-new-way-to-build-robots">How MachinaScript Works</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#installation">Installation</a> •
  <a href="#community">Community</a> •
</p>

<br>

<h6 align="center"> The future is not a gift. It is an achievement.</h4>

<br><br>

# Meet MachinaScript For Robots
MachinaScript is a dynamic set of tools and a LLM-JSON-based language designed to empower humans in the creation of their own robots. 

It facilitates the animation of generative movements, the integration of personality, and the teaching of new skills with a high degree of autonomy. With MachinaScript, you can control a wide range of electronic components, including Arduinos, Raspberry Pis, servo motors, cameras, sensors, and much more. 

MachinaScript's mission is to make cutting-edge intelligent robotics accessible for everyone.

## Read all about it on the [medium article](https://medium.com/@babycmd/introducing-llm-powered-robots-machinascript-for-robots-2dc8d76704b6)

![bar1](https://github.com/babycommando/machinascript-for-robots/assets/71618056/7bd469a2-6edd-4732-aade-9ef4c5beb060)
![bar git 2](https://github.com/babycommando/machinascript-for-robots/assets/71618056/7712bac9-7fa5-420c-8f40-64fbbe50f642)
![bar git 3](https://github.com/babycommando/machinascript-for-robots/assets/71618056/ea0f79c2-c534-4a76-81e1-8bde8d98c5a4)

<br><br>

## Installation: 
### Read the user manual in the [code directory here](https://github.com/babycommando/machinascript-for-robots/tree/main/MachinaScript).

<br><br>

# A New Way to Build Robots

## A Simple, Modular Pipeline
1. Input Reception: Upon receiving an input, the brain unit, (a central processing unit like a raspberry pi or a computer of your choice) initiates the process. For example listen for a wake up word, or a function to keep reading images in real time on a multimodal LLM.

2. Instruction Generation: A Language Model (LLM) then crafts a sequence of instructions for actions, movements and skills. These are formatted in MachinaScript, optimized for sequential execution.

3. Instruction Parsing: The robot's brain unit interprets the generated MachinaScript instructions.

4. Action Serialization: Instructions are relayed to the microcontroller, the entity governing the robot's physical operations like servo motors and sensors.

![example – 6](https://github.com/babycommando/machinascript-for-robots/assets/71618056/f6c761c3-caca-42e0-865d-37b8002fa512)

<br><br>

## MachinaScript LLM-JSON-Language Basics
![bar git](https://github.com/babycommando/machinascript-for-robots/assets/71618056/f5b604ba-f487-4e3c-8bb7-2f138502901d)

The MachinaScript language LLM-JSON-based synthax is incredibly modular because it is generative. It is composed of three major nested components: Actions, Movements and Skills.

### Actions, Movements, Skills
**Actions**: a set of instructions to be executed in a specific order. They may contain multiple movements and multiple skill usages.

**Movements**: they address motors to move and parameters like degrees and the speed. This can be used to create very personal animations.

**Skills**: function calling the MachinaScript way, to make use of cameras, sensors and even to speak with text-to-speech. 

As long as your brain unit code is adapted to interpret it, you have no ending for your creativity.

![example – 5](https://github.com/babycommando/machinascript-for-robots/assets/71618056/2427ca37-47b5-45a1-8b44-8af446bac698)

This is an example of the complete language structure in its current latest version. Note you can change the complete synthax for the language structure for your needs, no strings attached. Just make sure it will work with your brain module generating, parsing and serializing.

### Teaching MachinaScript to LLMs
The project was designed to be used accross the wide ecosystem of large language models, multimodals and non-multimodals, locals and non-locals. Note that autopilot units like Machina2 would require some form of multi-modality to sense the world via images and plan actions by itself.

To instruct a LLM to talk in the MachinaScript Synthax, we pass a system message that looks like this:
```
You are a MachinaScript for Robots generator.
MachinaScript is a LLM-JSON-based format used to define robotic actions, including 
motor movements and skill usage, under specific contexts given by the user. 

Each action can involve multiple movements, motors and skills, with defined parameters 
like motor positions, speeds, and skill-specific details, like this:
(...)
Please generate a new MachinaScript using the exact given format and project specifications.
```

This piece of code is refered as [machinascript_language.txt](https://github.com/babycommando/machinascript-for-robots/blob/main/MachinaScript/MACHINA1%20-%20Simple%20MachinaScript%20For%20Robots/machinascript_language.txt) and is recommended to stay unchanged.

Ideally you will only change the specs of your project.

<br>

### Declaring Specs: Teaching the LLM about your unique robot design - and personality.
No artisanal robot is the same. They are all beautifully unique.

One of the most mind blowing things about MachinaScript is that it can embody any design ever. You just need to tell it in a set of specs what are their phisical properties and limitations, as well as instructions for the behavior of the LLM. Should it be funny? Serious? What are its goals? Favorite color? The [machinascript_project_specs.txt](https://github.com/babycommando/machinascript-for-robots/blob/main/MachinaScript/MACHINA1%20-%20Simple%20MachinaScript%20For%20Robots/machinascript_project_specs.txt) is where you put everything related to your robot personality.

For this to work, we will append a little extra information in the system message containing the following information:
```
Project specs:
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
    {"motor": "motor_neck_vertical", "max_speed": "medium"}
    {"motor speeds": [slow, medium, high]}
  ]
  Personality: Funny, delicate
  Agency Level: high
}
```

note the JSON-style here can be completely reworked into any kind of text you want. You can even describe it in a single paragraph if you feel like. However for sake of human readability and developer experience, you can use this template for better "mental mapping" your project specs. This is all in very early beta so take it with a grain of salt.

### Finetuned Models

We are releasing a set of finetuned models for MachinaScript soon to make its generations even better. You can also finetune models for your own specific usecase too.

### Bonus: Animated Movements and Motion Design Principles
An action can contain multiple movements in an order to perform animations (set of movements). It may even contain embodied personality in the motion. 

Check out [Disney's latest robot that combines engineering with their team of motion designers](https://youtu.be/-cfIm06tcfA) to create a more human friendly machine in the style of BD-1.

You can learn more about the 12 principles of animation [here](https://www.youtube.com/watch?v=yiGY0qiy8fY&pp=ygUXcHJpbmNpcGxlcyBvZiBhbmltYXRpb24%3D).

![bar git 3](https://github.com/babycommando/machinascript-for-robots/assets/71618056/ea0f79c2-c534-4a76-81e1-8bde8d98c5a4)

<br><br>

## Getting Started

### Step 1: Make the Robot First

- **Begin with Arduino**: The easiest entry point is to start by programming your robot with Arduino code. 
  - Construct your robot and get it moving with simple programmed commands.
  - Modify the Arduino code to accept dynamic commands, similar to how a remote-controlled car operates.

- **Components**: Utilize a variety of components to enhance your robot:
  - Servo motors, sensors, buttons, LEDs, and any other compatible electronics.

### Step 2: Hand Over Control to the AI

- **Connect the Hardware**: Link your Arduino to a computing device of your choice. This could be a Raspberry Pi, a personal computer, or even an older laptop with internet access.

- **Edit the Brain Code**:
  - Map Arduino components within your code and establish their rules and functions for interaction. For instance, a servo motor might be named `head_motor_vertical` and programmed to move up to 180 degrees.
  - Modify the "system prompt" passed to the LLM with your defined rules and component names.

### Step 3: Learning New Skills

- Skills encompass any function callable from the LLM, ranging from complex movement sequences (e.g., making a drink, dancing) to interactive tasks like taking pictures or utilizing text-to-speech.

Here's a quick overview:
1. **Clone/Download**: Clone or download this repository into a chosen directory.
3. **Edit the Brain Code**: Customize the brain code's system prompt to describe your robot's capabilities.
4. **Connect Hardware**: Integrate your robot's locomotion and sensory systems as previously outlined.

## Community
Ready to share your projects to the world?
Join our community on discord:
https://discord.gg/CszE7JN3

## Note from the author
```
MachinaScript is my gift for the maker community,
wich has teached me so much about being a human.
Let the robots live forever.

Made with love for all the makers out there!
This project is and always will be free and open source for everyone.

babycommando
```

<img src="https://github.com/babycommando/machinascript-for-robots/assets/71618056/9b9463ba-c32c-4169-acbe-2f2418a8116a" width="100" height="100">
