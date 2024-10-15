import pygame
from robot_assistant import RobotAssistant

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROBOT_WIDTH = 40
ROBOT_HEIGHT = 80

class RobotSimulation:
    def __init__(self):
        self.robot = RobotAssistant()
        self.screen = None
        self.clock = None
        self.font = None

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Robot Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def run(self):
        self.initialize_pygame()
        self.robot.start_listening()

        last_action = "Waiting for command..."
        while self.robot.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.robot.running = False

            action, response = self.robot.process_command()
            if action:
                last_action = action
                self.robot.speak(response)
                print(f"Action: {action}, Response: {response}")  # Debug print

            self.update_display(last_action)
            self.clock.tick(30)

        self.robot.stop_listening()
        pygame.quit()

    def draw_robot(self):
        x, y = self.robot.position
        
        # Body (rectangle)
        pygame.draw.rect(self.screen, (0, 0, 255), (x - ROBOT_WIDTH//2, y - ROBOT_HEIGHT//2, ROBOT_WIDTH, ROBOT_HEIGHT))
        
        # Head (smaller square)
        head_size = ROBOT_WIDTH * 0.8
        pygame.draw.rect(self.screen, (0, 0, 255), (x - head_size//2, y - ROBOT_HEIGHT//2 - head_size, head_size, head_size))
        
        # Arms (rectangles)
        arm_width = ROBOT_WIDTH * 0.6
        arm_height = ROBOT_HEIGHT * 0.4
        pygame.draw.rect(self.screen, (0, 0, 255), (x - ROBOT_WIDTH//2 - arm_width, y - ROBOT_HEIGHT//4, arm_width, arm_height))
        pygame.draw.rect(self.screen, (0, 0, 255), (x + ROBOT_WIDTH//2, y - ROBOT_HEIGHT//4, arm_width, arm_height))
        
        # Legs (rectangles)
        leg_width = ROBOT_WIDTH * 0.4
        leg_height = ROBOT_HEIGHT * 0.5
        pygame.draw.rect(self.screen, (0, 0, 255), (x - ROBOT_WIDTH//4, y + ROBOT_HEIGHT//2, leg_width, leg_height))
        pygame.draw.rect(self.screen, (0, 0, 255), (x + ROBOT_WIDTH//4 - leg_width, y + ROBOT_HEIGHT//2, leg_width, leg_height))

    def update_display(self, action):
        self.screen.fill((255, 255, 255))
        
        # Draw the robot
        self.draw_robot()
        
        # Display the action text
        text_surface = self.font.render(action, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

if __name__ == "__main__":
    simulation = RobotSimulation()
    simulation.run()
