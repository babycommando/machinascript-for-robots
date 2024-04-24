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

#include <Servo.h>

Servo servoA; // Servo for motor A connected to pin 9
Servo servoB; // Servo for motor B connected to pin 8

// Target positions for servo A and B
int targetPositionA = 0, targetPositionB = 0;
// Speeds for servo A and B movement in milliseconds
int speedA = 0, speedB = 0;
// Timestamps for the last movement update for servo A and B
unsigned long lastUpdateA = 0, lastUpdateB = 0;
// Flags to track if servo A and B are currently moving
bool movingA = false, movingB = false;

void setup() {
  servoA.attach(9); // Attach servo motor A to pin 9
  servoB.attach(8); // Attach servo motor B to pin 8
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
}

void loop() {
  static String receivedData = ""; // Buffer to accumulate received serial data
  while (Serial.available() > 0) { // Check if data is available to read
    char inChar = (char)Serial.read(); // Read the incoming character
    if (inChar == '\n') { // Check if the character signifies end of command
      parseCommands(receivedData); // Parse and execute the received commands
      receivedData = ""; // Reset buffer for next command
    } else {
      receivedData += inChar; // Accumulate the incoming data
    }
  }

  // Continuously update servo positions based on the current commands
  updateServo(servoA, targetPositionA, speedA, lastUpdateA, movingA);
  updateServo(servoB, targetPositionB, speedB, lastUpdateB, movingB);
}

void parseCommands(const String& commands) {
  // Expected command format: "A:position,speed;B:position,speed"
  // Speed is passed directly in milliseconds
  sscanf(commands.c_str(), "A:%d,%d;B:%d,%d", &targetPositionA, &speedA, &targetPositionB, &speedB);

  // Mark both servos as moving and record the start time of movement
  lastUpdateA = millis();
  lastUpdateB = millis();
  movingA = true;
  movingB = true;
}

void updateServo(Servo& servo, int targetPosition, int speed, unsigned long& lastUpdate, bool& moving) {
  if (moving) { // Check if the servo is supposed to be moving
    unsigned long currentTime = millis(); // Get current time
    // Update the servo position if the specified speed interval has elapsed
    if (currentTime - lastUpdate >= speed) {
      int currentPosition = servo.read(); // Read current position
      // Move servo towards target position
      if (currentPosition < targetPosition) {
        servo.write(++currentPosition);
      } else if (currentPosition > targetPosition) {
        servo.write(--currentPosition);
      } else {
        moving = false; // Stop moving if target position is reached
      }
      lastUpdate = currentTime; // Update the last movement time
    }
  }
}
