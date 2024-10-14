import speech_recognition as sr
import pyttsx3
import nltk
import pygame
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
        self.screen = None
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
                self.position[1] -= 50
                return "Moving up"
            elif 'down' in filtered_tokens:
                self.position[1] += 50
                return "Moving down"
            elif 'left' in filtered_tokens:
                self.position[0] -= 50
                return "Moving left"
            elif 'right' in filtered_tokens:
                self.position[0] += 50
                return "Moving right"
        elif 'stop' in filtered_tokens:
            self.running = False
            return "Stopping the program"

        return "I'm sorry, I don't understand that command."

    def speak(self, text):
        logging.info(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def update_display(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (255, 0, 0), self.position, 20)
        pygame.display.flip()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Robot Assistant")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            command = self.listen()
            response = self.process_command(command)
            self.speak(response)
            self.update_display()

        pygame.quit()

if __name__ == "__main__":
    robot = RobotAssistant()
    robot.run()
