# game.py

import pygame

#TODO
# 1. thought about what i wanted to do in my final project


# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "<Game>"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./image/mario copy.png")
        # self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

        # Mario's starting position
        self.vel_x = 0
        self.vel_y = 0

        self.level = None

    def update(self):
        self.calc_grav()

        self.rect.x += self.vel_x

        # See if we hit anything
        platform_hit_group = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in platform_hit_group:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        self.rect.y += self.vel_y

        # Check and see if we hit anything
        platform_hit_group = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in platform_hit_group:

            # Reset our position based on the top/bottom of the object.
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.vel_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.vel_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.vel_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.vel_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.image.load("./image/platformfixed.png")
        self.image = pygame.transform.scale(self.image, ([width, height]))

        self.rect = self.image.get_rect()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [
            [210, 70, 500, 500],
            [210, 70, 200, 400],
            [210, 70, 600, 300],
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # group of all the sprites
    all_sprites = pygame.sprite.Group()

    mario = Player()
    all_sprites.add(mario)

    level_one = Level_01(mario)
    mario.level = level_one

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mario.go_left()
                if event.key == pygame.K_RIGHT:
                    mario.go_right()
                if event.key == pygame.K_UP:
                    mario.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and mario.vel_x < 0:
                    mario.stop()
                if event.key == pygame.K_RIGHT and mario.vel_x > 0:
                    mario.stop()


        # ----- LOGIC
        all_sprites.update()

        # ----- DRAW
        level_one.draw(screen)
        all_sprites.draw(screen)


        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()