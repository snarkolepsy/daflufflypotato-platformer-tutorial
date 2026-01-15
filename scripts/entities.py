import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos) # using a list instead of a tuple for some reason
        self.size = size
        self.velocity = [0, 0] # rate of change in the X and Y axis
        self.collisions = {'up': False, 'down': False, 'right' : False, 'left' : False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0, 0]

    def rect(self):
        """Dynamically generate the rectangle representing a physics entity's collision box

        :return: the hit box
        """
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        # If the action is different than the current state
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy() # EXAMPLE: looking for key `player/run`

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

        # If we're moving the right, use the same sprite. If we're moving left, mirror it so it's facing the right way
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Keeping track of the last intended movement, regardless of whether we successfully moved or not
        self.last_movement = movement

        # Applying gravity to the y-coordinate and cap at terminal velocity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Should stop when we hit the ground or the ceiling
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface, offset=(0, 0)):
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] - self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1
        if self.collisions['down']: # If we collide with the ground, air_time and jumps counter are reset
            self.air_time = 0
            self.jumps = 1

        # Wall-sliding logic
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            # Animate in the correct direction while sliding down the wall
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        # If we're in the middle of a wall slide, we should ignore the other animation states
        if not self.wall_slide:
            # If we're in the air for a significant amount of time, we're in a jump state
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0: # Otherwise if we are moving horizontally, we're in run state
                self.set_action('run')
            else: # Or we might not be moving at all
                self.set_action('idle')

        # Reduce horizontal speed down to zero over time from either direction (like friction or air resistance)
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def jump(self):
        """Jumping away from a wall we're sliding on or up from the ground

        :return: True after a successful jump
        """
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0: # Facing left wall and we attempted moving to the left
                # Jump away from the wall, to the right
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0: # Facing right wall and we tried moving further right
                # Jump to the left and away from the wall
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
