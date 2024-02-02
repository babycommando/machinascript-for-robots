

![MachinaScript For Robots](https://github.com/babycommando/machinascript/assets/71618056/9cf321ae-187f-414d-84a2-c2690c78394a)
![example – 2](https://github.com/babycommando/machinascript/assets/71618056/c00c28eb-20e2-466e-8991-62a821cc2408)
![example – 3](https://github.com/babycommando/machinascript/assets/71618056/f4e3f545-a4f6-4731-bbb9-474b75670b7f)
![example](https://github.com/babycommando/machinascript/assets/71618056/5ef748bc-8334-4e10-99bd-19dcc6229021)
![example – 4](https://github.com/babycommando/machinascript-for-robots/assets/71618056/2c18b953-bf94-4559-825a-da5fd5c61295)
![example – 5](https://github.com/babycommando/machinascript-for-robots/assets/71618056/2427ca37-47b5-45a1-8b44-8af446bac698)
![example – 6](https://github.com/babycommando/machinascript-for-robots/assets/71618056/f6c761c3-caca-42e0-865d-37b8002fa512)
![example – 7](https://github.com/babycommando/machinascript-for-robots/assets/71618056/a6cd7442-2705-49fc-87ed-263b809feb1d)

# MachinaScript For Robots 
MachinaScript is a set of tools and a LLM-JSON-based language that enable humans to build their own robots right now.
Animate generative movements, give it personality and teach new skills with high agency level.
Control arduinos, raspberrypis, servo motors, cameras, sensors or any other compatible pieces of electronics. You name it.

MachinaScript for Robots aims to democratize the access of bleeding edge intelligent robotics for everyone.

## Getting started
### Make the robot first
The easiest way to get started is to begin with the arduino code first.
Mount your robot and make it move first with programmed orders.
Then, modify the arduino code to listen for movements instead of pre-programming them (like a remote controller on a toy car).
You may use as many components as you wish, like servo motors, sensors, buttons, LEDs and more.

### Handle the control to the Ai
Next we hook the arduino to a computer of your choice. It can be a raspberry pi, your daily computer or even an old laptop that have internet connection.

Editing the brain code should be straight forward - map the arduino components in your code and define their set of rules and functions to interact with it (for example a servo motor can move 180 degrees). Make sure to name it in a way that makes sense for example: "head_motor_vertical".

Next, modify the "system prompt" passed to the LLM based on your set of rules. Add the motors and sensors names.

### Learning new skills
Skills can be anything inside a function that can be called from the LLM. It can range from a complete set of movements (making a drink, dancing) to taking pictures and talking (text-to-speech).

## Installation
- clone/download this repo in a folder of your choice
- edit the brain code system prompt describing your robot
- hook your robot locomotive and sensorial systems to the brain as described before

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
