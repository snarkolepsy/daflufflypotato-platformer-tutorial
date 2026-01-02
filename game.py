import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemaps import Tilemap

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
            'player' : load_image('entities/player.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

    def run(self):
        while True:
            # Clearing the screen
            self.display.fill((14, 219, 248))  # RGB for sky blue

            # Rendering the tilemap behind the player
            self.tilemap.render(self.display)

            # Calculate the horizontal movement vector and account for physics and collisions
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) # in a platformer you move left to right

            # Rendering the moveable player sprite
            self.player.render(self.display)

            # Event-handling logic
            for event in pygame.event.get():
                # Quitting the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # Pressing a key
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:  # Releasing a key
                    if event.key ==  pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # scaling up the display to the screen size
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0,))

            pygame.display.update()
            self.clock.tick(60)  # ensures 60 FPS

Game().run()
