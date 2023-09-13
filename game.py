import pygame
import sys
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images


# rendering is based entirely on the order you render on surface


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("2D ninja game")
        # create window ... setmode creates the window
        # setting screen as the window surface
        self.screen = pygame.display.set_mode((640, 480))
        # display is what we are rendering on to.
        # pygame.Surface generates an empty surface. Used for creating stuff in memory that you may need for some purpose.
        # we will use it in this instance for rendering
        self.display = pygame.Surface((320, 240))

        # clock forces games fps.. create clock object
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            # if this was larger it could be efficient to do a for loop
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
        }
        # print(self.assets)

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))

    def run(self):
        # SDL?
        while True:
            # clear screen after each frame to prevent trails
            self.display.fill((14, 219, 248))

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                # clicked the x on window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            # create display for screen
            pygame.display.update()
            # set fps
            self.clock.tick(60)


Game().run()


# creates a rectangle every frame based on image
# and size of it is being determined by the image
# img_r = pygame.Rect(
#     self.img_pos[0],
#     self.img_pos[1],
#     self.img.get_width(),
#     self.img.get_height(),
# )
# # drawing the rectangle
# if img_r.colliderect(self.collision_area):
#     pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
# else:
#     pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

# # make it so a true gets equated to 1 and false = 0
# self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
# # the top left of the screen is (0, 0)
# self.screen.blit(self.img, self.img_pos)
# DEMONSTRATION FOR IMAGE LOADING BELOW
# self.img = pygame.image.load("data/images/clouds/cloud_1.png")
# # set_colorkey allows you to choose a color to be transparent
# self.img.set_colorkey((0, 0, 0))

# self.img_pos = [160, 260]
# # updaing movement values based on whether the key is being held down
# # if the first is true we are holding up key second true = downkey
# self.movement = [False, False]

# self.collision_area = pygame.Rect(50, 50, 300, 50)
