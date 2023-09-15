import pygame


class PhysicsEntity:
    # taking game as a parameter allows you access anything in the game.
    # e_type = entity type pos = position
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        # we create the pos list because we have to keep track of it since we need to abstract the process to a rectable for collision and movement.
        # this is because rectangles do not work with float values only int. So if a value is added like .5 then it will stay in the same spot.
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
            if entity_rect.colliderect(rect):
                # moving right
                if frame_movement[0] > 0:
                    # make the right edge of the entitiy snap to the left edge of the tile
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                # moving right
                if frame_movement[1] > 1:
                    # make the right edge of the entitiy snap to the left edge of the tile
                    entity_rect.bottom = rect.top
                    # these just return an int representing their place on the x or y axis
                if frame_movement[1] < 1:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)
