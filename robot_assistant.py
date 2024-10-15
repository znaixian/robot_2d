import speech_recognition as sr
import pyttsx3
import nltk
import logging
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import threading

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Set up logging
logging.basicConfig(filename='robot_assistant.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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
                    self.last_command = text
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                logging.warning("Speech recognition could not understand audio")
            except sr.RequestError as e:
                logging.error(f"Could not request results from speech recognition service; {e}")

    def process_command(self):
        if self.last_command is None:
            return None

        command = self.last_command
        self.last_command = None

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
        if text:
            logging.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()

    def stop_listening(self):
        self.listening = False

if __name__ == "__main__":
    robot = RobotAssistant()
    robot.start_listening()
    robot.run()
