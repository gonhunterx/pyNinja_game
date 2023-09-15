import pygame


class PhysicsEntity:
    # taking game as a parameter allows you access anything in the game.
    # e_type = entity type pos = position
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )
        # min takes the lower of two/however many values you give it
        # 5 is the maximum velocity downwards. With 0,0 at the top left
        # positive is down and like -10 would be an up value.

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.collidedict(rect):
                pass

        self.pos[1] += frame_movement[1]
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)
