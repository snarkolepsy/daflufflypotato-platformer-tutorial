import sys
import math
import pygame
import random

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemaps import Tilemap
from scripts.clouds import Clouds
from scripts.particles import Particle

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
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run' : Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump' : Animation(load_images('entities/player/jump')),
            'player/slide' : Animation(load_images('entities/player/slide')),
            'player/wall_slide' : Animation(load_images('entities/player/wall_slide')),
            'particle/leaf' : Animation(load_images('particles/leaf'), img_dur=20, loop=False),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        # TEMPORARY: load the map we made to playtest
        self.tilemap.load('map.json')

        # Locate the trees on the tilemap from which we can spawn leaves particles
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        print(self.leaf_spawners)

        # Particles system
        self.particles = []

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

            # Spawning particles
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    # Any random space within bounds of the rectangle
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            # Draw the clouds before the tiles so they're in the background
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # Rendering the tilemap behind the player
            self.tilemap.render(self.display, offset=render_scroll)

            # Calculate the horizontal movement vector and account for physics and collisions
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) # in a platformer you move left to right

            # Rendering the moveable player sprite
            self.player.render(self.display, offset=render_scroll)

            # Managing the particles system
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.position[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

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
