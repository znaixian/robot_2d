import speech_recognition as sr
import pyttsx3
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import threading
import os
import json
from openai import AzureOpenAI

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Set up logging
logging.basicConfig(filename='robot_assistant.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set SSL certificate file
os.environ['SSL_CERT_FILE'] = 'ca-bundle-full.crt'

# Load configuration from JSON file
with open('config.json') as f:
    config = json.load(f)

# Near the top of the file
os.environ['AZURE_OPENAI_ENDPOINT'] = "https://azure-llm.factset.com/"

# Then use it when initializing the client
client = AzureOpenAI(
    api_version="2023-09-01-preview",
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
    api_key=config['AZURE_OPENAI_API_KEY']
)

class RobotAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.position = [400, 300]  # Starting position (center of the screen)
        self.running = True
        self.listening = False
        self.last_command = None
        self.speed_multiplier = 1  # New attribute for speed control

    def start_listening(self):
        self.listening = True
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    logging.info(f"Recognized speech: {text}")
                    print(f"Recognized: {text}")  # Debug print
                    self.last_command = text.lower()  # Convert to lowercase here
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio")
                self.speak("I'm sorry, I didn't catch that. Could you please repeat?")
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition service; {e}")
                self.speak("I'm having trouble with speech recognition. Please try again.")

    def process_command(self):
        if self.last_command is None:
            return None, None

        command = self.last_command
        self.last_command = None

        logging.info(f"Processing command: {command}")
        print(f"Processing: {command}")  # Debug print

        # In the process_command method, before making the API call
        print(f"Making API call with model: gpt-4o-0513")

        try:
            result = client.chat.completions.create(
                model="gpt-4o-0513",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an AI assistant that controls a robot's movement. 
                        Interpret commands and respond with a JSON object containing 'action', 'response', and 'speed' fields.
                        The 'action' field should be a list of movement instructions, each with 'direction' and 'distance' keys.
                        Valid directions are 'up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right'.
                        If no distance is specified, use 10 pixels as default. The 'response' field should be a natural language description of the action.
                        The 'speed' field should be 'normal' for walk/move/zigzag, 'fast' for jog/faster, and 'very_fast' for run.
                        IMPORTANT: Your entire response must be valid JSON."""
                    },
                    {
                        "role": "user",
                        "content": f"Interpret this robot command: '{command}'"
                    }
                ],
                temperature=0.3,
                max_tokens=150,
                top_p=0.9,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )

            response_content = result.choices[0].message.content.strip()
            print(f"AI response: {response_content}")  # Debug print
            result = json.loads(response_content)
            actions = result['action']
            speak_response = result['response']
            speed = result['speed']

            # Set speed multiplier based on the command
            if speed == 'very_fast':
                self.speed_multiplier = 3
            elif speed == 'fast':
                self.speed_multiplier = 2
            else:
                self.speed_multiplier = 1

        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error: {e}")
            logging.error(f"Response content: {response_content}")
            error_message = "I'm having trouble understanding the command. Could you please rephrase it?"
            self.speak(error_message)
            return None, error_message
        except KeyError as e:
            logging.error(f"KeyError: {e}")
            logging.error(f"Result: {result}")
            error_message = "I'm having trouble processing the command. Could you please try again?"
            self.speak(error_message)
            return None, error_message
        except Exception as e:
            logging.error(f"Error using Azure OpenAI API: {e}")
            error_message = "I'm sorry, I encountered an error processing that command. Could you try again?"
            self.speak(error_message)
            return None, error_message

        # Update robot state based on interpreted actions
        for action in actions:
            direction = action['direction']
            distance = action.get('distance', 10) * self.speed_multiplier  # Apply speed multiplier
            
            new_x, new_y = self.position[0], self.position[1]
            
            if 'up' in direction:
                new_y = max(20, new_y - distance)
            if 'down' in direction:
                new_y = min(580, new_y + distance)
            if 'left' in direction:
                new_x = max(20, new_x - distance)
            if 'right' in direction:
                new_x = min(780, new_x + distance)
            
            # Check if the robot has hit the border
            if new_x == self.position[0] and new_y == self.position[1]:
                speak_response += " The robot has reached the border and cannot move further in that direction."
            
            self.position = [new_x, new_y]

        if 'stop' in command.lower():
            self.running = False

        action_taken = ', '.join([f"{a['direction']} {a.get('distance', 10) * self.speed_multiplier}px" for a in actions])
        logging.info(f"Action taken: {action_taken}")
        print(f"Action: {action_taken}")  # Debug print
        return action_taken, speak_response

    def speak(self, text):
        if text:
            logging.info(f"Speaking: {text}")
            print(f"Speaking: {text}")  # Debug print
            self.engine.say(text)
            self.engine.runAndWait()

    def stop_listening(self):
        self.listening = False

if __name__ == "__main__":
    robot = RobotAssistant()
    robot.start_listening()
    while robot.running:
        action, response = robot.process_command()
        if action:
            robot.speak(response)
    robot.stop_listening()
