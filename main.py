import pygame
from robot_assistant import RobotAssistant

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROBOT_RADIUS = 20
MOVE_DISTANCE = 20  # 20 centimeters (scaled to pixels)

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

        while self.robot.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.robot.running = False

            command = self.robot.listen()
            response = self.robot.process_command(command)
            self.robot.speak(response)

            self.update_display(response)
            self.clock.tick(30)

            if not self.robot.running:
                print("Program is stopping...")
                break

        pygame.quit()

    def update_display(self, response):
        self.screen.fill((255, 255, 255))
        
        # Draw the robot
        pygame.draw.circle(self.screen, (255, 0, 0), self.robot.position, ROBOT_RADIUS)
        
        # Display the response text
        text_surface = self.font.render(response, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

if __name__ == "__main__":
    simulation = RobotSimulation()
    simulation.run()
