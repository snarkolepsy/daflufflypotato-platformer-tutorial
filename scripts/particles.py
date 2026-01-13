class Particle:
    def __init__(self, game, particle_type, position, velocity=[0, 0], frame=0):
        self.game = game
        self.type = particle_type
        self.position = list(position)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + particle_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surface, offset=(0, 0)):
        img = self.animation.img()
        surface.blit(img, (self.position[0] - offset[0] - img.get_width() // 2, self.position[1] - offset[1] - img.get_height() // 2))
