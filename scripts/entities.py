import pygame
import math 
import random
from scripts.particle import Particle
from scripts.spark import Spark

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.last_movement = [0, 0]
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action 
            # grab new animation 
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        
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
        
        
        if movement[0] > 0:
            self.flip = False 
        if movement[0] < 0:
            self.flip = True
        
        self.last_movement = movement
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            
        self.animation.update()
        
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        
        self.walking = 0 
        
    def update(self, tilemap, movement=(0, 0)):
        # calcs for what to do 
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                # run into something right or left flip 
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            # cut down to 0 over time 
            self.walking = max(0, self.walking - 1)
            # get one frame to shoot here
            if not self.walking:
                # diff between enemy and player 
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                # if y axis offset is less than 16 pixels 
                if (abs(dis[1]) < 16):
                    if (self.flip and dis[0] < 0):
                        # spawn bullet to left 
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.sparks.append(Spark(self.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                    
                
        # check
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')   
            
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        if self.flip:
            # also flip gun and offset it with the '- 4' and account for the width of gun img 
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            # center with 4 pixel offset and camera 
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        
        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0 
            self.jumps = 1
        
        # acts as a single frame switch (it will immediatly shut off)
        self.wall_slide = False
        if(self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            # used to prevent animation state to not be over written 
            self.wall_slide = True
            # capping downward velocity at 0.5
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                # handle flip
                self.flip = False 
            else:
                self.flip = True
            # update animation
            self.set_action('wall_slide')
        if not self.wall_slide:    
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
                
                # if at start or end of dash
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                # selecting a random angle within a full circle (full circle = math.pi * 2)
                # getting the radian
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                # cos for x axis sin for y axis 

                # generating a velocity based on the angle (how to move something in a direction 2D)
                # by it not being random you maintain distribution and scaling 
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        # this below runs while in a dash
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
            
    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            # get rendering func of the super class 
            # make player invisible
            super().render(surf, offset=offset)
    
    def jump(self):
        if self.wall_slide:
            # facing left and movement is to the left 
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5 # push you away from the wall 
                self.velocity[1] = -2.5 # force you up 
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            # facing right 
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5 # push you away from the wall 
                self.velocity[1] = -2.5 # force you up 
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
    def dash(self):
        if not self.dashing:
            # facing left 
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60