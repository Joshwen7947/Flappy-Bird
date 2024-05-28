import pygame
import random

from objects import Bird, Pipe, Ground


pygame.init()
WIDTH, HEIGHT = 288, 512
display_height = 0.80 * HEIGHT


SCREEN = pygame.display.set_mode((WIDTH,HEIGHT),pygame.NOFRAME)
clock = pygame.time.Clock()
FPS = 20

# COLORS

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Backgrounds

bg = pygame.image.load('Assets/background-day.png')

pipe_img = pygame.image.load('Assets/pipe-green.png')

gameover_img =  pygame.image.load('Assets/gameover.png')
flappybird_img =  pygame.image.load('Assets/flappybird.png')
flappybird_img = pygame.transform.scale(flappybird_img, (200,80))

# Sounds & fx
die_fx = pygame.mixer.Sound('Sounds/die.wav')
hit_fx = pygame.mixer.Sound('Sounds/hit.wav')
point_fx = pygame.mixer.Sound('Sounds/point.wav')
swoosh_fx = pygame.mixer.Sound('Sounds/swoosh.wav')
wing_fx = pygame.mixer.Sound('Sounds/wing.wav')

# Objects
pipe_group = pygame.sprite.Group()
base = Ground()
# score_img = Score(WIDTH // 2, 50, win)
bird = Bird()

# Variables
base_height = 0.80 * HEIGHT
speed = 0
game_started = False
game_over = False
restart = False
score = 0
start_screen = True
pipe_pass = False
pipe_frequency = 4750 # 4700 or 4900

# Main game loop
running = True
while running:
    SCREEN.blit(bg, (0, 0))
    
    if start_screen:
        speed = 0
        bird.make_flap()
        base.update(speed)
        
        SCREEN.blit(flappybird_img, (40, 50))
    else:
        # Generate pipes
        if game_started and not game_over:
            next_pipe = pygame.time.get_ticks()
            print(next_pipe)
            if next_pipe - last_pipe >= pipe_frequency:
                y = display_height // 2
                pipe_pos = random.choice(range(-150, 150, 4))
                height = y + pipe_pos
                
                top = Pipe(pipe_img, height, 1)
                bottom = Pipe(pipe_img, height, -1)
                pipe_group.add(top)
                pipe_group.add(bottom)
                
                # Find the rightmost position of the last pipe in the pipe group
                rightmost_pipe_x = max(pipe.rect.right for pipe in pipe_group.sprites())
                
                # Set the x position for the next set of pipes with a buffer space of 200px
                next_pipe_x = rightmost_pipe_x + 200
                
                last_pipe = next_pipe

        # Update pipes and other objects
        pipe_group.update(speed)
        base.update(speed)
        bird.update()
        # score_img.update(score)

        # Check collisions and update score
        for pipe in pipe_group:
            if bird.rect.colliderect(pipe.rect):
                if bird.alive:
                    hit_fx.play()
                    die_fx.play()
                    game_over = True
                bird.alive = False
                bird.theta = bird.vel * -2
            elif bird.rect.left > pipe.rect.left and bird.rect.right < pipe.rect.right and not pipe_pass and bird.alive:
                pipe_pass = True
                if pipe_pass:
                    if bird.rect.left > pipe.rect.right:
                        pipe_pass = False
                        score += 1
                        point_fx.play()
    
    # Display game over screen if the bird is not alive
    if not bird.alive:
        SCREEN.blit(gameover_img, (50, 200))
        
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
                
                
                
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_screen:
                game_started = True
                speed = 2
                start_screen = False
                game_over = False
                last_pipe = pygame.time.get_ticks() - pipe_frequency
                next_pipe = 0
                pipe_group.empty()
                score = 0
            elif game_over:
                start_screen = True
                bird = Bird()
                pipe_img = pygame.image.load('Assets/pipe-green.png')
                bg = pygame.image.load('Assets/background-day.png')
    
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
