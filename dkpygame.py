import pygame
import math
import sys
import time
import random

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escape the Maze with Rotating Rings and Slits")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Colors for the rings
ring_colors = [WHITE, RED, GREEN, YELLOW, CYAN]

# Ball (Player) settings
ball_radius = 9
ball_speed = 3.1

# Ring settings
num_rings = 5
ring_radius = 80
ring_center = (screen_width // 2, screen_height // 2)
ring_thickness = 10
ring_speeds = [0.5, -1, 0.75, -0.5, 1]
slit_angle = 45  # Size of the slit in degrees
ring_segments = 12  # Number of segments per ring

# Store the exploded segments for each ring
ring_explosions = [[] for _ in range(num_rings)]

# Function to initialize or reset game variables
def reset_game():
    global ball_x, ball_y, start_time, game_over, game_won, ring_passed, ring_explosions, angles
    ball_x, ball_y = screen_width // 2, screen_height // 2  # Start at center
    start_time = time.time()
    game_over = False
    game_won = False
    ring_passed = [False] * num_rings
    angles = [0] * num_rings
    ring_explosions = [[] for _ in range(num_rings)]

# Helper function to check collision between the ball and a point on the ring
def check_collision(ball_pos, angle, radius):
    x, y = ball_pos
    ring_x = ring_center[0] + radius * math.cos(math.radians(angle))
    ring_y = ring_center[1] + radius * math.sin(math.radians(angle))
    dist = math.hypot(x - ring_x, y - ring_y)
    return dist < ball_radius + ring_thickness / 2

# Function to create exploding segments for a ring
def create_explosion(ring_index, ring_color, ring_radius):
    segment_angle = 360 / ring_segments
    for j in range(ring_segments):
        angle = j * segment_angle
        speed = random.uniform(2, 4)  # Speed of each segment
        ring_explosions[ring_index].append({
            'angle': angle,
            'speed': speed,
            'distance': ring_radius,
            'color': ring_color
        })

# Call reset_game at the start
reset_game()
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Restart game if space is pressed after game over
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()

    # Display "Game Over" screen and wait for space press to restart
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
        restart_text = font.render("Press Space to Restart", True, WHITE)
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))
        pygame.display.flip()
        clock.tick(60)
        continue  # Skip the rest of the game loop if game over

    # Check if game is won
    if game_won:
        font = pygame.font.Font(None, 74)
        text = font.render("Hooray!", True, GREEN)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))
        
        # Display time taken to win the game
        elapsed_time = time.time() - start_time
        time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, WHITE)
        screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, screen_height // 2 + 30))
        
        pygame.display.flip()
        pygame.time.delay(2000)
        reset_game()
        continue

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_x - ball_speed > 0:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT] and ball_x + ball_speed < screen_width:
        ball_x += ball_speed
    if keys[pygame.K_UP] and ball_y - ball_speed > 0:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN] and ball_y + ball_speed < screen_height:
        ball_y += ball_speed

    # Track whether the player collides with any ring
    collided_with_ring = False

    # Draw rotating rings with a slit or exploding effect
    for i in range(num_rings):
        if not ring_passed[i] and not ring_explosions[i]:
            angles[i] = (angles[i] + ring_speeds[i]) % 360

            # Calculate start and end angles for the arc, leaving a slit
            start_angle = angles[i]
            end_angle = start_angle + 360 - slit_angle

            # Draw the ring as an arc with a slit
            pygame.draw.arc(
                screen,
                ring_colors[i],
                (ring_center[0] - ring_radius - i * 40,
                 ring_center[1] - ring_radius - i * 40,
                 (ring_radius + i * 40) * 2,
                 (ring_radius + i * 40) * 2),
                math.radians(start_angle),
                math.radians(end_angle),
                ring_thickness
            )

            # Check collision with solid part of the ring
            collision_angle = math.degrees(math.atan2(ball_y - ring_center[1], ball_x - ring_center[0]))
            if collision_angle < 0:
                collision_angle += 360

            if start_angle <= collision_angle <= end_angle and \
               check_collision((ball_x, ball_y), collision_angle, ring_radius + i * 40):
                collided_with_ring = True
                game_over = True
                break

            # Start explosion animation when ball passes the ring without collision
            if not game_over and math.hypot(ball_x - ring_center[0], ball_y - ring_center[1]) > ring_radius + i * 40 + ball_radius:
                ring_passed[i] = True
                create_explosion(i, ring_colors[i], ring_radius + i * 40)

        # Handle and draw exploding segments
        elif ring_explosions[i]:
            for segment in ring_explosions[i]:
                segment['distance'] += segment['speed']
                segment_x = ring_center[0] + segment['distance'] * math.cos(math.radians(segment['angle']))
                segment_y = ring_center[1] + segment['distance'] * math.sin(math.radians(segment['angle']))

                pygame.draw.line(
                    screen,
                    segment['color'],
                    (int(segment_x), int(segment_y)),
                    (int(segment_x + 5 * math.cos(math.radians(segment['angle']))),
                     int(segment_y + 5 * math.sin(math.radians(segment['angle'])))),
                    ring_thickness // 2
                )

    # Check if the player has escaped the maze without colliding with the last ring
    if not game_over and not collided_with_ring and \
       math.hypot(ball_x - ring_center[0], ball_y - ring_center[1]) > ring_radius + (num_rings - 1) * 40 + ball_radius:
        game_won = True

    # Draw the player (ball)
    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), ball_radius)

    # Display the elapsed time at the top of the screen
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, WHITE)
    screen.blit(time_text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
