import speech_recognition as sr
import pyttsx3
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Set up logging
logging.basicConfig(filename='robot_assistant.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class RobotAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.position = [400, 300]  # Starting position (center of the screen)
        self.running = True

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                logging.info(f"Recognized speech: {text}")
                return text
        except sr.UnknownValueError:
            logging.warning("Speech recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logging.error(f"Could not request results from speech recognition service; {e}")
            return None

    def process_command(self, command):
        if command is None:
            return "I'm sorry, I couldn't understand that."

        tokens = word_tokenize(command.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        if 'move' in filtered_tokens:
            if 'up' in filtered_tokens:
                self.position[1] = max(20, self.position[1] - 20)
                return "Moving up 20 centimeters"
            elif 'down' in filtered_tokens:
                self.position[1] = min(580, self.position[1] + 20)
                return "Moving down 20 centimeters"
            elif 'left' in filtered_tokens:
                self.position[0] = max(20, self.position[0] - 20)
                return "Moving left 20 centimeters"
            elif 'right' in filtered_tokens:
                self.position[0] = min(780, self.position[0] + 20)
                return "Moving right 20 centimeters"
        elif 'stop' in filtered_tokens or 'abort' in filtered_tokens:
            self.running = False
            return "Stopping the program"

        return "I'm sorry, I don't understand that command."

    def speak(self, text):
        logging.info(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    robot = RobotAssistant()
    robot.run()
