# 2D Robot Assistant Simulation

This project implements a basic 2D robot simulation using Python and Pygame. The robot can listen to voice commands and perform simple movements in a graphical interface.

## Features

- Voice command recognition
- 2D graphical interface using Pygame
- Simple movement commands (up, down, left, right)
- Text-to-speech feedback

## Requirements

- Python 3.7+
- Pygame
- SpeechRecognition
- pyttsx3
- NLTK
- OpenAI

For a complete list of dependencies, see `requirements.txt`.

## Installation

1. Clone the repository:   ```
   git clone https://github.com/znaixian/robot_2d.git
   cd robot_2d ```

2. Create a virtual environment:   ```
   python -m venv venv   ```

3. Activate the virtual environment:
   - On Windows:     ```
     venv\Scripts\activate     ```
   - On macOS and Linux:     ```
     source venv/bin/activate     ```

4. Install the required packages:   ```
   pip install -r requirements.txt   ```

## Usage

Run the main script to start the simulation:

## Quitting the Simulation

There are several ways to exit the simulation:

1. Voice Command: Say "stop" or "abort" to the robot.
2. Close Window: Click the close button (X) on the simulation window.
3. Keyboard Interrupt: Press Ctrl+C in the terminal where the script is running.
