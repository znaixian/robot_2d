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

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version="2023-09-01-preview",
    azure_endpoint="https://azure-llm.factset.com/",
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

    def start_listening(self):
        self.listening = True
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    logging.info(f"Recognized speech: {text}")
                    print(f"Recognized: {text}")  # Debug print
                    self.last_command = text.lower()  # Convert to lowercase here
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                logging.warning("Speech recognition could not understand audio")
            except sr.RequestError as e:
                logging.error(f"Could not request results from speech recognition service; {e}")

    def process_command(self):
        if self.last_command is None:
            return None, None

        command = self.last_command
        self.last_command = None

        logging.info(f"Processing command: {command}")
        print(f"Processing: {command}")  # Debug print

        try:
            result = client.chat.completions.create(
                model="gpt-4o-0513",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that helps control a robot. Interpret commands and respond with a JSON object containing 'action' and 'response' fields."
                    },
                    {
                        "role": "user",
                        "content": f"Interpret this robot command: '{command}'"
                    }
                ],
                temperature=0.1,
                max_tokens=100,
                top_p=0.5,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )

            response_content = result.choices[0].message.content.strip()
            result = json.loads(response_content)
            action_taken = result['action']
            speak_response = result['response']
        except Exception as e:
            logging.error(f"Error using Azure OpenAI API: {e}")
            return None, "I'm sorry, I couldn't process that command."

        # Update robot state based on interpreted action
        if 'up' in action_taken.lower():
            self.position[1] = max(20, self.position[1] - 20)
        elif 'down' in action_taken.lower():
            self.position[1] = min(580, self.position[1] + 20)
        elif 'left' in action_taken.lower():
            self.position[0] = max(20, self.position[0] - 20)
        elif 'right' in action_taken.lower():
            self.position[0] = min(780, self.position[0] + 20)
        elif 'stop' in action_taken.lower():
            self.running = False

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
