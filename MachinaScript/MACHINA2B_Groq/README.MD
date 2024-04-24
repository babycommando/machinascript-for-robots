# Patch 0.2.2 Release Notes - Introducing MACHINA2B

---

![banner0 2 2](https://github.com/babycommando/machinascript-for-robots/assets/71618056/3de6a27c-c506-477d-95c1-2e0758594f45)

![comics2](https://github.com/babycommando/machinascript-for-robots/assets/71618056/6a42eec3-1140-4121-810e-0c6cfca856f9)

# A Symphony of Thought and Action

We are thrilled to unveil Patch 0.2.2, bringing to life MACHINA2B— a milestone in the mission to make sophisticated robotics accessible to everyone, from hobbyists to innovators, enabling the creation of autonomous robots right from your garage.

MACHINA2B extends the pioneering spirit of MACHINA2A of autonomous self-prompting based on world scanning. Keeping the structure of actions, skills, and movements, this new iteration harnesses the synergy between multimodal vision LLMs and the innovative GROQ inference API.

Leveraging the latest advancements in multimodal vision LLMs and the rapid inference capabilities of GROQ API powered by LPUs chips, MACHINA2B represents a leap in processing power and operational efficiency for homemade DIY robots.

**_MACHINA2B embodies a loop of perception and action that simulates the flow of human thought._**

Through the integration of a vision systems and a serial to analogic signals parser, MACHINA2B interprets visual data and crafts responses in near real-time, enabling machines to perform complex tasks with elegance and some level of precision - a fantastic achievement for such an early stage of the technology.

Feeling excited? Join the MachinaScript for Robots community and help redefine what's possible in the world of DIY robotics.

Anakin built C3PO when he was 9, how about you?

Robots 💘 Groq

## Technical Overview

MACHINA2B works on a the premise of a looped set of functions that scans the world, generates a thought, produces a set of actions and send them over serial to your arduino. As Groq still don't support multimodal models, we must have an initial stage of analyzing an image apart from the groq main prompt.

1. The robot takes a picture to scan the world around it
2. Then generate a thought on it using a multimodal LLM, being a local very fast server like LMstudio or Ollama runnign LLaVA, Obsidian 3B or something else.
3. After analyzing the image and generating the description for the environment, the brain uses it to query the groq api and generate the MachinaScript code.
4. Finally the parser serializes the code for the arduino to be executed. Make sure to also take a look in the C++ "body" piece of the code, as it is super simple to modify and expand to your project needs.

#### Tips for stage 2 (vision analysis):

Analyzing images can vary speed depending on a lot of factors, not only if your host machine is a NASA supercomputer. Make sure to use LMstudio, Ollama or other llm serving software that enables you to offload the model to the GPU vRAM. Small models like Obsidian 3B, tiny LLaVA or others under 4GB tend to fit in almost any GPU's vRAM entirely, even the old 1050ti series from nvidia - producing reasonable 4-11 tokens per second.

You should also take in account the size of images being produced by the camera in pixels and megabytes, as well as making sure you just need a very simple one liner response from the vision model.

## Safety and Usage

Please follow all safety guidelines when deploying MACHINA2B, ensuring that your environment is suitable for autonomous operations. Regular updates and patches will be provided to enhance functionality and security.

### Get Started

To begin using MACHINA2B, please refer to our installation guide and user manual provided in the root of the machinas repository.
