# MachinaScript Deep Installation Guide

After cloning/downloading this repo, make sure you have the latest version of python 3 and the Arduino IDE.

For better understanding of the project it is recommended to start working with the Machina1 project, as Machina2 is still under development. Instructions below.

Install the following python libs:

```
pip install pyserial SpeechRecognition openai
```

## Building a Robot
Next we must build the robot. 

Try taking a look at all the files in this repository first.

```
- Body.ino
- Brain.py
- MachinaScript_Language.txt
- MachinaScript_Project-Specs.txt
```

- The *Body* represent all the things microcontroller/Arduino-related - sensors, motors, leds and serials.

- The *Brain* is where most of the work happens - query LLMs, parse the MachinaScript into serial and teach new skills for your robots. Don't forget to properly set up your openAi api keys, or hook it to a local LLM server running in your machine like LMStudio.

- *MachinaScript_Language.txt* the initial part of the system prompt. It contains basic understanding for the Ai to understand how to write in the MachinaScript JSON-based language format. You may only edit this part of the prompt if you want to expand or modify the basics of the language itself based on your project. This would require changing the parsing functions in your python Brain file.

- *MachinaScript_Project-Specs.txt* is where you will teach the Ai about your project specifications. You must edit this file after you finished implementing your body and brain code because they may contain variables and limitations in the code that the Ai may be unaware of. Example: servo motors can move 180 degrees, the normal pose is at 90 degrees. Note that the synthax in this is still in very early beta, so there is a lot of exploration ongoing for this part. It is important to make things clear and spend the less tokens possible to spare time and money on your project.

## Suggested Order

Starting with the arduino "body.ino" code, take a look at the template file included in this repo and modify it according to your project. Include any motors, ports and sensors as you like. In other words, start by making your robot move programatically before hooking it to an LLM to make sure the project works.

Proceed to editing the brain.py file and hooking with the arduino - map your project components and motors and pass them properly in the code. Then gently hook it with the serial arduino port. Try to make simple tests first, then you go complex. Explore new skills that only components could provide - for example radio frequency scan, RFID, infrared, web-related stuff... You name it.

Finally when you have the entire project set, teach the LLM how your robot works - pass all your specs in the MachinaScript_Project-Specs.txt and don't be afraid to explore new methods of doing it. In the file you will find a set of examples. We also recommend you having a quick read on the MachinaScript_Language.txt to understand better the synthax we initially came up with, however you may want to leave this intact for compatibility with the ready code parts in the body and brain.

If you are new to programming and have way too many questions, don't hesitate to paste the code on chatGPT-4 and ask about its structure as it may provide you some great insight for you to make your own modules. We really encourage you to get started debugging your code with the Ai pals.

Also reach us out in the github repo and in the discord group for bug reports and for sharing your projects!
