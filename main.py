import pygame
import math
import random
import logging
from robot_assistant import RobotAssistant

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROBOT_WIDTH = 90
ROBOT_HEIGHT = 240
BASE_MOVE_SPEED = 2  # Reduced base speed for more visible movement

class RobotSimulation:
    def __init__(self):
        self.robot = RobotAssistant()
        self.screen = None
        self.clock = None
        self.font = None
        self.target_position = [400, 300]
        self.move_speed = 5
        self.stone_pos = (random.randint(100, 700), random.randint(100, 500))
        self.turtle_pos = (random.randint(100, 700), random.randint(100, 500))

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

            try:
                action, response = self.robot.process_command()
                if action:
                    last_action = action
                    self.robot.speak(response)
                    print(f"Action: {action}, Response: {response}")  # Debug print
                    self.target_position = self.robot.position.copy()
            except Exception as e:
                print(f"Error processing command: {e}")
                logging.error(f"Error processing command: {e}")

            self.update_robot_position()
            self.update_display(last_action)
            self.clock.tick(60)

        self.robot.stop_listening()
        pygame.quit()

    def draw_lawn(self):
        grass_color = (34, 139, 34)  # Forest green
        pygame.draw.rect(self.screen, grass_color, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw some random grass blades
        for _ in range(1000):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.line(self.screen, (0, 100, 0), (x, y), (x, y - 5), 1)

    def draw_stone(self):
        pygame.draw.circle(self.screen, (169, 169, 169), self.stone_pos, 30)  # Dark gray stone

    def draw_turtle(self):
        turtle_color = (0, 128, 0)  # Dark green
        shell_color = (139, 69, 19)  # Saddle brown
        x, y = self.turtle_pos

        # Draw turtle body
        pygame.draw.ellipse(self.screen, turtle_color, (x - 25, y - 15, 50, 30))
        
        # Draw turtle head
        pygame.draw.circle(self.screen, turtle_color, (x + 25, y), 10)
        
        # Draw turtle shell
        pygame.draw.circle(self.screen, shell_color, (x, y), 20)

    def draw_robot(self):
        x, y = self.robot.position
        
        # Colors
        body_color = (200, 200, 200)  # Light gray
        accent_color = (100, 100, 100)  # Dark gray
        highlight_color = (255, 0, 0)  # Red

        # Body
        pygame.draw.rect(self.screen, body_color, (x - 45, y - 120, 90, 240))
        
        # Head
        pygame.draw.rect(self.screen, body_color, (x - 40, y - 150, 80, 30))
        pygame.draw.rect(self.screen, accent_color, (x - 35, y - 145, 70, 20))
        
        # Eyes
        pygame.draw.circle(self.screen, highlight_color, (x - 15, y - 135), 5)
        pygame.draw.circle(self.screen, highlight_color, (x + 15, y - 135), 5)
        
        # Horns
        pygame.draw.polygon(self.screen, accent_color, [(x - 40, y - 150), (x - 65, y - 170), (x - 20, y - 150)])
        pygame.draw.polygon(self.screen, accent_color, [(x + 40, y - 150), (x + 65, y - 170), (x + 20, y - 150)])
        
        # Shoulders
        pygame.draw.circle(self.screen, body_color, (x - 45, y - 60), 15)
        pygame.draw.circle(self.screen, body_color, (x + 45, y - 60), 15)
        
        # Arms
        pygame.draw.rect(self.screen, body_color, (x - 60, y - 60, 15, 120))
        pygame.draw.rect(self.screen, body_color, (x + 45, y - 60, 15, 120))
        
        # Hands
        pygame.draw.circle(self.screen, accent_color, (x - 52, y + 60), 10)
        pygame.draw.circle(self.screen, accent_color, (x + 52, y + 60), 10)
        
        # Legs
        pygame.draw.rect(self.screen, body_color, (x - 30, y + 120, 20, 60))
        pygame.draw.rect(self.screen, body_color, (x + 10, y + 120, 20, 60))
        
        # Feet
        pygame.draw.rect(self.screen, accent_color, (x - 35, y + 180, 30, 10))
        pygame.draw.rect(self.screen, accent_color, (x, y + 180, 30, 10))

        # Chest detail
        pygame.draw.rect(self.screen, highlight_color, (x - 30, y - 90, 60, 20))
        
        # Waist
        pygame.draw.rect(self.screen, accent_color, (x - 35, y + 100, 70, 10))

    def update_display(self, action):
        self.draw_lawn()
        self.draw_stone()
        self.draw_turtle()
        self.draw_robot()
        
        # Display the action text
        text_surface = self.font.render(action, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def update_robot_position(self):
        dx = self.target_position[0] - self.robot.position[0]
        dy = self.target_position[1] - self.robot.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        move_speed = BASE_MOVE_SPEED * self.robot.speed_multiplier
        
        if distance > move_speed:
            ratio = move_speed / distance
            new_x = self.robot.position[0] + dx * ratio
            new_y = self.robot.position[1] + dy * ratio

            # Check for collision with stone
            if math.sqrt((new_x - self.stone_pos[0])**2 + (new_y - self.stone_pos[1])**2) < 60:
                return  # Don't move if colliding with stone

            # Check for collision with turtle
            if math.sqrt((new_x - self.turtle_pos[0])**2 + (new_y - self.turtle_pos[1])**2) < 60:
                return  # Don't move if colliding with turtle

            # Update position if no collision
            self.robot.position[0] = new_x
            self.robot.position[1] = new_y
        else:
            self.robot.position = self.target_position.copy()

if __name__ == "__main__":
    simulation = RobotSimulation()
    simulation.run()
