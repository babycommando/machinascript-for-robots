#  _ _ _                           ()                   
# ' ) ) )         /                /\                _/_
#  / / / __.  _. /_  o ____  __.  /  )  _. __  o _   /  
# / ' (_(_/|_(__/ /_<_/ / <_(_/|_/__/__(__/ (_<_/_)_<__ 
#                                              /        
#                                             '         
#+----------------------------------------------------------------+
#|MachinaScript for Robots v0.1.2024                              |
#|                                                                |
#|..:: BODY MODULE ::..                                           |
#|                                                                |
#|This is the body module, intended to be executed on a           |
#|microcontroller. You may need to customize this code for        |
#|your own robotic mount.                                         |
#|                                                                |
#|Keep in mind this is just a very simple pipeline integration    |
#|of many concepts together:                                      |
#|                                                                |
#|- To receive and parse serial data received into a set of       |
#|ordered actions and movements and execute them.                 |
#|                                                                |
#|- Instructions for this code exactly are for moving a set of    |
#|servo motors and blinking LEDs when serial messages come up.    |
#|You may want to add sensors, other motors, change ports         |
#|and more as you feel.                                           |
#|                                                                |
#|You are free to use and modify this piece of code,              |
#|as well as to come up with something totally different.         |
#|                                                                |
#|This is an initial proof-of-concept, more examples coming soon. |
#|                                                                |
#|Interested in contributing? Join the community!                 |
#|See the github repo for more infos.                             |
#+----------------------------------------------------------------+

# tip: if you have no idea what it all means, try pasting the contents
# of this file into GPT or any other LLM and ask for a summary.
# Then you can start making your own modifications and modules precisely.

#include <Arduino.h>
#include <Servo.h>

// Servo configuration
const int numServos = 4;
Servo servos[numServos];
const int servoPins[numServos] = {3, 5, 6, 9}; // Servo pin assignments

// LED configuration
const int numLEDs = 2;
const int ledPins[numLEDs] = {10, 11}; // LED pin assignments

// Function declarations
void executeAction(const String& actionCommand);
void executeMovement(const String& movementCommand);
void moveServo(int motorID, int position, int speed);
int getMotorIDByPin(int pin);
int interpretSpeed(const String& speedStr);
void blinkLED(int ledPin, int duration, int times);

void setup() {
    Serial.begin(9600); // Initialize serial communication
    // Attach servos to their respective pins
    for (int i = 0; i < numServos; i++) {
        servos[i].attach(servoPins[i]);
    }
    // Set LED pins as output
    for (int i = 0; i < numLEDs; i++) {
        pinMode(ledPins[i], OUTPUT);
    }
}

void loop() {
    static String receivedData = ""; // Buffer for incoming data
    // Read serial data
    while (Serial.available() > 0) {
        char inChar = (char)Serial.read();
        // Check for end of command
        if (inChar == '\n') {
            executeAction(receivedData); // Execute received command
            receivedData = ""; // Clear buffer
        } else {
            receivedData += inChar; // Append received character
        }
    }
}

void executeAction(const String& actionCommand) {
    // Process each movement command within the received action
    int movementStart = 0, movementEnd;
    while ((movementEnd = actionCommand.indexOf(';', movementStart)) != -1) {
        executeMovement(actionCommand.substring(movementStart, movementEnd));
        movementStart = movementEnd + 1;
    }
}

void executeMovement(const String& movementCommand) {
    // Check and execute LED blink command
    if (movementCommand.startsWith("blinkLED")) {
        int ledPin, duration, times;
        sscanf(movementCommand.c_str(), "blinkLED,%d,%d,%d", &ledPin, &duration, &times);
        blinkLED(ledPin, duration, times);
    } else {
        // Parse and execute servo movement command
        int servoPin, position;
        char speedStr[10];
        if (sscanf(movementCommand.c_str(), "%d,%d,%s", &servoPin, &position, speedStr) == 3) {
            int motorID = getMotorIDByPin(servoPin);
            int speed = interpretSpeed(speedStr);
            if (motorID != -1) {
                moveServo(motorID, position, speed);
            }
        }
    }
}

void moveServo(int motorID, int position, int speed) {
    // Control servo to move to the specified position at the given speed
    Servo& servo = servos[motorID];
    int currentPosition = servo.read();
    for (int pos = currentPosition; pos != position; pos += (pos < position) ? 1 : -1) {
        servo.write(pos);
        delay(speed);
    }
}

int getMotorIDByPin(int pin) {
    // Identify the servo motor ID associated with the given pin
    for (int i = 0; i < numServos; i++) {
        if (servoPins[i] == pin) {
            return i;
        }
    }
    return -1;
}

int interpretSpeed(const String& speedStr) {
    // Convert speed string to delay time
    if (speedStr == "slow") return 20;
    if (speedStr == "medium") return 10;
    if (speedStr == "fast") return 5;
    return 10;
}

void blinkLED(int ledPin, int duration, int times) {
    // Blink the specified LED at the given duration and repeat times
    for (int i = 0; i < times; i++) {
        digitalWrite(ledPin, HIGH);
        delay(duration);
        digitalWrite(ledPin, LOW);
        delay(duration);
    }
}