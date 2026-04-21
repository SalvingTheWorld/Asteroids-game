import pygame
from constants import *
from logger import log_state, log_event
from player import *
from asteroid import *
from asteroidfield import *
import sys
from shot import *

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    #Set up window name
    pygame.display.set_caption('Asteroids')

    #Set up the window size
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    #Set up the game clock
    clock = pygame.time.Clock()
    dt = 0

    #Initializing font 
    pygame.font.init()
    font = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 30)

    #Menu state and score variables
    game_state = 'menu'
    game_score = 0

    updatable = pygame.sprite.Group() #holds all objects that can be updated
    drawable = pygame.sprite.Group() #holds all objects that can be drawn
    asteroids = pygame.sprite.Group() #holds all Asteroids objects
    shots = pygame.sprite.Group() #holds all shots sprits for the player ship
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, drawable, updatable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    #Resets game's sprites and player after player retries
    def reset_state():
        for shot in shots:
            shot.kill()
        
        for asteroid in asteroids:
            asteroid.kill()
        
        asteroid_field.kill()
        player.kill()

        new_player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        new_asteroid_field = AsteroidField()

        return new_player, new_asteroid_field

    #Game logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and game_state == 'menu':
                if event.key == pygame.K_SPACE:
                    game_state = 'playing'
            elif event.type == pygame.KEYDOWN and game_state == 'game_over':
                if event.key == pygame.K_SPACE:
                    game_state = 'playing'
                    game_score = 0
                    player, asteroid_field = reset_state()
        screen.fill('black')

        if game_state == 'menu':
            menu_msg = font.render('Press Space to Start', False, 'white')
            menu_msg_surface_pos = menu_msg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(menu_msg, menu_msg_surface_pos)
        elif game_state == 'playing':
            updatable.update(dt)
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event('player_hit')
                    game_state = 'game_over'
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event('asteroid_shot')
                        shot.kill()
                        if asteroid.radius == ASTEROID_MAX_RADIUS:
                            game_score += 3
                        elif asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                            game_score += 2
                        else:
                            game_score += 1
                        asteroid.split()               
            for draw in drawable:
                draw.draw(screen)
            score_msg = font.render(f'Score: {game_score}', False, 'White')
            screen.blit(score_msg, (0,0))
        elif game_state == 'game_over':
            game_over_text_1 = font.render('Game Over!', False, 'white')
            game_over_surface_pos_1 = game_over_text_1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(game_over_text_1, game_over_surface_pos_1)
            
            game_over_text_2 = font.render('Press Space to retry!', False, 'white')
            game_over_surface_pos_2 = game_over_text_2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
            screen.blit(game_over_text_2, game_over_surface_pos_2)

            game_over_text_3 = font.render(f'Your score was {game_score}', False, 'white')
            game_over_surface_pos_3 = game_over_text_3.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))
            screen.blit(game_over_text_3, game_over_surface_pos_3)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    #Legacy code for reference
    # while True:
    #     log_state()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             return
    #     updatable.update(dt)
    #     for asteroid in asteroids:
    #         if asteroid.collides_with(player):
    #             log_event('player_hit')
    #             print('Game Over!')
    #             sys.exit()
    #         for shot in shots:
    #             if shot.collides_with(asteroid):
    #                 log_event('asteroid_shot')
    #                 shot.kill()
    #                 asteroid.split()
    #     screen.fill('black')
    #     for draw in drawable:
    #         draw.draw(screen)
    #     pygame.display.flip()
    #     dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
