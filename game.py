import sys
import pygame
from pygame.examples.scroll import scroll_view

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemaps import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        # Initialize the pygame library
        pygame.init()

        # Set the window name
        pygame.display.set_caption('Ninja Game')

        # Set output window resolution
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        # mass importing the following asset folders
        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds'),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        # Scrolling and camera handling
        self.scroll = [0, 0]

    def run(self):
        while True:
            # Clearing the screen
            self.display.blit(self.assets['background'], (0, 0))

            # Move towards the player at a dynamic rate
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1]) / 30
            # Fixing subpixel "jitter" during camera motion
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Draw the clouds before the tiles so they're in the background
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # Rendering the tilemap behind the player
            self.tilemap.render(self.display, offset=render_scroll)

            # Calculate the horizontal movement vector and account for physics and collisions
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) # in a platformer you move left to right

            # Rendering the moveable player sprite
            self.player.render(self.display, offset=render_scroll)

            # Event-handling logic
            for event in pygame.event.get():
                # Quitting the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: # Pressing a key
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP: # Jumping with the up key
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP: # Releasing a key
                    if event.key ==  pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # scaling up the display to the screen size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0,))

            pygame.display.update()
            self.clock.tick(60)  # ensures 60 FPS

Game().run()
