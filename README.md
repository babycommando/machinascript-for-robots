

![MachinaScript For Robots](https://github.com/babycommando/machinascript/assets/71618056/9cf321ae-187f-414d-84a2-c2690c78394a)
![example – 2](https://github.com/babycommando/machinascript/assets/71618056/c00c28eb-20e2-466e-8991-62a821cc2408)
![example – 3](https://github.com/babycommando/machinascript/assets/71618056/f4e3f545-a4f6-4731-bbb9-474b75670b7f)
![example](https://github.com/babycommando/machinascript/assets/71618056/5ef748bc-8334-4e10-99bd-19dcc6229021)
![example – 4](https://github.com/babycommando/machinascript-for-robots/assets/71618056/2c18b953-bf94-4559-825a-da5fd5c61295)
![example – 5](https://github.com/babycommando/machinascript-for-robots/assets/71618056/2427ca37-47b5-45a1-8b44-8af446bac698)
![example – 6](https://github.com/babycommando/machinascript-for-robots/assets/71618056/f6c761c3-caca-42e0-865d-37b8002fa512)
![example – 7](https://github.com/babycommando/machinascript-for-robots/assets/71618056/a6cd7442-2705-49fc-87ed-263b809feb1d)

# Read all about it on the [medium article](https://medium.com/@babycmd/introducing-llm-powered-robots-machinascript-for-robots-2dc8d76704b6)

# MachinaScript For Robots

MachinaScript is a dynamic set of tools and a LLM-JSON-based language designed to empower humans in the creation of their own robots. It facilitates the animation of generative movements, the integration of personality, and the teaching of new skills with a high degree of autonomy. With MachinaScript, you can control a wide range of electronic components, including Arduinos, Raspberry Pis, servo motors, cameras, sensors, and much more. Our goal is to make cutting-edge intelligent robotics accessible to everyone.

## MachinaScript Language Basics
The MachinaScript language LLM-JSON-based synthax is incredibly modular because it is generative. As long as your brain code is adapted to understand it, you literally have no ending for your creativity.

You can change the complete synthax for the language structure for your needs, no strings attached. Just make sure it will work with your code.

This is an example of the complete language structure
```
{
  "Machina_Actions": {
    "action_1": {
      "description": "Positioning before taking a picture",
      "movements": {
        "1": {
          "motor_neck_vertical": 45,
          "motor_neck_horizontal": 0,
          "speed": "medium"
        }
      },
      "useSkills": {}
    },
    "action_2": {
      "description": "Taking picture and indicating completion",
      "movements": {},
      "useSkills": {
        "1": {
          "skill": "photograph"
        },
      }
    },
    "action_3": {
      "description": "Returning to normal position",
      "movements": {
        "1": {
          "motor_neck_vertical": 0,
          "speed": "medium"
        }
      },
      "useSkills": {}
    }
  }
}
```

### Animated Movements
An action can contain multiple movements in an order to perform an animation (set of movements). It may contain personality in the motion.

Here's a robot dance:
```
{
  "Machina_Actions": {
    "action_1": {
      "description": "Robot dance - classic arm wave",
      "movements": {
        "1": {
          "motor_right_shoulder_vertical": 90,
          "motor_right_elbow_horizontal": 90,
          "motor_left_shoulder_vertical": -90,
          "motor_left_elbow_horizontal": -90,
          "speed": "medium"
        },
        "2": {
          "motor_torso_twist": 25,
          "speed": "slow"
        },
        "3": {
          "motor_right_shoulder_vertical": -90,
          "motor_right_elbow_horizontal": -90,
          "motor_left_shoulder_vertical": 90,
          "motor_left_elbow_horizontal": 90,
          "speed": "medium"
        }
      }
    }
  }
}
```


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

## Installation

1. **Clone/Download**: Clone or download this repository into a chosen directory.
2. **Edit the Brain Code**: Customize the brain code's system prompt to describe your robot's capabilities.
3. **Connect Hardware**: Integrate your robot's locomotion and sensory systems as previously outlined.



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
