"""
Project : Pong Game using Pygame
@author : M.Raahim Rizwan
This project is made with the help of a youtube video. Below is the link to that video.
https://www.youtube.com/playlist?list=PLr-iRXN7HiJjSqV2D16A0ql9kQB5TfKQ5
"""


# Importing the libraries
import pygame, sys

# Creating Ball Class
class Ball:
    # Creating our constructor
    def __init__(self, window, color, posx, posy, radius):
        self.window = window
        self.color = color
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.show()
        self.dx = 0
        self.dy = 0

    def show(self):
        """
        Showing the ball on the screen.
        """
        pygame.draw.circle(self.window, self.color, (self.posx, self.posy), self.radius)

    def start_moving(self):
        """
        Gives a starting velocity to our ball.
        """
        self.dx = 0.8
        self.dy = 0.2

    def move(self):
        """
        Responsible for moving the ball.
        """
        self.posx += self.dx
        self.posy += self.dy

    def paddle_collision(self):
        """
        Collision between ball and paddle.
        """
        self.dx = -self.dx
    def wall_collision(self):
        """
        Collision between ball and walls.
        """
        self.dy = -self.dy

    def restart_position(self):
        """
        Respawning the ball when the player scores a goal.
        """
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.dx = 0
        self.dy = 0
        self.show()


# Creating Paddle Class
class Paddle:
    def __init__(self, window, color, posx, posy, width, height):
        self.window = window
        self.color = color
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.state = 'stopped'
        self.show()

    def show(self):
        """
        Showing the paddle.
        """
        pygame.draw.rect(self.window, self.color, (self.posx, self.posy, self.width, self.height))

    def move(self):
        """
        Responsible for moving the paddle
        """
        if self.state == 'up':
            self.posy -= 0.5
        elif self.state == 'down':
            self.posy += 0.5

    def clamp(self):
        """
        Checking for paddle and wall colllision.
        """
        # Collision for top boundary and paddle
        if self.posy <= 0:
            self.posy = 0
        # Collision for bottom boundary and paddle
        if self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

    def restart_position(self):
        """
        Restarting the paddles position.
        """
        self.posy = HEIGHT//2 - self.height//2
        self.state = 'stopped'
        self.show()

# Creating Score Class
class Score:
    def __init__(self, window, points, posx, posy):
        self.window = window
        self.points = points
        self.posx = posx
        self.posy = posy
        self.font = pygame.font.SysFont("Helvetica", 80, bold=True)
        self.label = self.font.render(self.points, 0, WHITE)
        self.show()

    def show(self):
        """
        Showing the score on the screen.
        """
        self.window.blit(self.label, (self.posx - self.label.get_rect().width//2, self.posy))

    def increase(self):
        """
        Increasing the score.
        """
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, WHITE)

    def restart(self):
        """
        Restarting the scores.
        """
        self.points = '0'
        self.label = self.font.render(self.points, 0, WHITE)


        
        
# Creating Collision Class
class Collision:
    def between_ball_and_paddle_one(self, ball, paddle_one):
        """
        Checks collision between ball and left paddle.
        """
        if ball.posy + ball.radius > paddle_one.posy and ball.posy - ball.radius < paddle_one.posy + paddle_one.height:
            if ball.posx - ball.radius <= paddle_one.posx + paddle_one.width:
                return True
        return False

    def between_ball_and_paddle_two(self, ball, paddle_two):
        """
        Checks collision between ball and right paddle.
        """
        if ball.posy + ball.radius > paddle_two.posy and ball.posy - ball.radius < paddle_two.posy + paddle_two.height:
            if ball.posx + ball.radius >= paddle_two.posx:
                return True
        return False
    def between_ball_and_walls(self, ball):
        """
        Checks collision between ball and all the walls.
        """
        # Top
        if ball.posy - ball.radius <= 0:
            return True
        # Bottom
        if ball.posy + ball.radius >= HEIGHT:
            return True
        return False

    def check_goal_player_one(self, ball):
        """
        Checking for the goal for the player on the left side.
        """
        return ball.posx - ball.radius >= WIDTH   

    def check_goal_player_two(self, ball):
        """
        Checking for the goal for the player on the right side.
        """
        return ball.posx - ball.radius <= 0

# Initializing pygame
pygame.init()

# Game Constants
WIDTH = 900
HEIGHT = 500
icon = pygame.image.load('Asset/icon.png')
pygame.display.set_icon(icon)
BLUE = (0, 134, 207)
DARK_BLUE = (15, 63, 140)
WHITE = (255, 255, 255)

# Creating game window and setting title
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

def paint_back():
    """
    Filling our screen with blue color and creating a line in the middle of the screen.
    """
    window.fill(BLUE)
    pygame.draw.line(window, DARK_BLUE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)

def restart():
    """
    Restarting all the objects in the game.
    """
    paint_back()
    score_one.restart()
    score_two.restart()
    ball.restart_position()
    paddle_one.restart_position()
    paddle_two.restart_position()

paint_back()

# Objects
ball = Ball(window, DARK_BLUE, WIDTH//2, HEIGHT//2, 15)
paddle_one = Paddle(window, DARK_BLUE, 15, HEIGHT//2 - 60, 20, 120)
paddle_two = Paddle(window, DARK_BLUE, WIDTH - 20 - 15, HEIGHT//2 - 60, 20, 120)
collision = Collision()
score_one = Score(window, '0', WIDTH // 4, 15)
score_two = Score(window, '0', WIDTH - WIDTH // 4, 15)

playing = False

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.start_moving()
                playing = True
            if event.key == pygame.K_ESCAPE:
                restart()
                playing = False
            if event.key == pygame.K_w:
                paddle_one.state = 'up'
            if event.key == pygame.K_s:
                paddle_one.state = 'down'
            if event.key == pygame.K_UP:
                paddle_two.state = 'up'
            if event.key == pygame.K_DOWN:
                paddle_two.state = 'down'
        if event.type == pygame.KEYUP:
            paddle_one.state = 'stopped'
            paddle_two.state = 'stopped'
        
    if playing:
        paint_back()
        # Ball movement
        ball.move()
        ball.show()
        # Paddle one 
        paddle_one.move()
        paddle_one.clamp()
        paddle_one.show()
        # Paddle two 
        paddle_two.move()
        paddle_two.clamp()
        paddle_two.show()
        # Check for collisions
        if collision.between_ball_and_paddle_one(ball, paddle_one):
            ball.paddle_collision()

        if collision.between_ball_and_paddle_two(ball, paddle_two):
            ball.paddle_collision()

        if collision.between_ball_and_walls(ball):
            ball.wall_collision()

        if collision.check_goal_player_one(ball):
            paint_back()
            score_one.increase()
            ball.restart_position()
            paddle_one.restart_position()
            paddle_two.restart_position()
            playing = False

        if collision.check_goal_player_two(ball):
            paint_back()
            score_two.increase()
            ball.restart_position()
            paddle_one.restart_position()
            paddle_two.restart_position()
            playing = False
            

    # Showing the scores
    score_one.show()
    score_two.show()
    # Updating the display
    pygame.display.update()
