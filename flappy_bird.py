import pygame
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))
BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 30
    MIN_ROTATION = -85
    ROTATION_VELOCITY = 20
    TERMINAL_VELOCITY = 15
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMAGES[0]

    def jump(self):
        self.velocity = -12
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacment = self.velocity * self.tick_count + (1.5 * self.tick_count ** 2)

        if displacment >= self.TERMINAL_VELOCITY:
            displacment = self.TERMINAL_VELOCITY
        if displacment < 0:
            displacment -= 2

        self.y = self.y + displacment

        if displacment < 0 or self.y < self.height -50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = abs(displacment)
            elif self.tilt >= self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
             if self.tilt > self.MIN_ROTATION:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.image_count +=1
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMAGES[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMAGES[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMAGES[1]
        elif self.image_count == self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMAGES[0]
            self.image_count = 0

        if self.tilt < -80:
            self.image = self.IMAGES[1]
            self.image_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

def draw_window(win, bird):
    win.blit(BACKGROUND_IMAGE, (0,0))
    bird.draw(win)
    pygame.display.update()


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bird = Bird(200, 200)
    clock = pygame.time.Clock()

    game = True
    playing = False
    while game:
        clock.tick(30)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not playing:
                        playing = True
                    bird.jump()

                if event.key == pygame.K_ESCAPE:
                    playing = False

                if event.key == pygame.K_r:
                    playing = False
                    bird = Bird(200, 200)

        if playing:
            bird.move()
        draw_window(win, bird)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()