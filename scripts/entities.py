import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # using a list instead of a tuple for some reason
        self.size = size
        self.velocity = [0, 0] # rate of change in the X and Y axis
        self.collisions = {'up': False, 'down': False, 'right' : False, 'left' : False}

    def rect(self):
        """Dynamically generate the rectangle representing a physics entity's collision box

        :return: the hit box
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        """Update the physics entity in accordance to gravity, applied motion, and collision detection

        :param tilemap: Tilemap object of the current room
        :param movement: Tuple representing the x and y movement vectors (default (0,0))
        """
        # Reset adjacent collisions
        self.collisions = {'up': False, 'down': False, 'right' : False, 'left' : False}

        # Calculating the x,y change in a singe frame
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Applying movement to x position
        self.pos[0] += frame_movement[0]
        # Collision detection and handling logic for horizontal travel
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos): # check all nearby tiles
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # Applying movement to y position with corresponding gravity and collision handling
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        # Applying gravity to the y-coordinate
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Should stop when we hit the ground or the ceiling
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surface):
        surface.blit(self.game.assets['player'], self.pos)
