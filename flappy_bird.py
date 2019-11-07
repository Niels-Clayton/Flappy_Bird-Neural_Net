import pygame
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))


class Bird:
    MAX_ROTATION = 30
    MIN_ROTATION = -85
    ROTATION_VELOCITY = 20
    TERMINAL_VELOCITY = 17
    ANIMATION_TIME = 5
    IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
              pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
              pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]

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
        self.velocity = -11
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacment = self.velocity * self.tick_count + (1.5 * self.tick_count ** 2)

        if displacment >= self.TERMINAL_VELOCITY:
            displacment = self.TERMINAL_VELOCITY
        if displacment < 0:
            displacment -= 2

        if self.y > 0:
            self.y = self.y + displacment
        elif self.y <= 0:
            self.y = 1
            self.velocity = 2
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


class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.bottom_pipe = PIPE_IMAGE
        self.top_pipe = pygame.transform.flip(PIPE_IMAGE, False, True)

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.top_pipe.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.top_pipe, (self.x, self.top))
        window.blit(self.bottom_pipe, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_overlap = bird_mask.overlap(bottom_mask, bottom_offset)
        top_overlap = bird_mask.overlap(top_mask, top_offset)

        if bottom_overlap or top_overlap:
            return True
        else:
            return False


class Base:
    VELOCITY = 5

    def __init__(self):
        self.base_image = BASE_IMAGE
        self.width = self.base_image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = WIN_HEIGHT - self.base_image.get_height() + 100

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 < -self.width:
            self.x1 = self.x2 + self.width
        if self.x2 < -self.width:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.base_image, (self.x1, self.y))
        window.blit(self.base_image, (self.x2, self.y))

def draw_window(win, bird, pipes, base):
    win.blit(BACKGROUND_IMAGE, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bird = Bird(200, 350)
    pipes = [Pipe(500)]
    base = Base()
    clock = pygame.time.Clock()

    game = True
    playing = False
    while game:
        base.move()
        clock.tick(30)
        to_remove = []

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
                    pipes = [Pipe(500)]

        if playing:
            add_pipe = False

            for pipe in pipes:
                if pipe.collide(bird):
                    pass
                if pipe.x + pipe.bottom_pipe.get_width() < 0:
                    to_remove.append(pipe)
                if not pipe.passed and pipe.x + (pipe.bottom_pipe.get_width() / 2) < bird.x:
                    pipe.passed = True
                    add_pipe = True
                pipe.move()

            if add_pipe:
                pipes.append(Pipe(550))
            for rem in to_remove:
                pipes.remove(rem)

            bird.move()
        draw_window(win, bird, pipes, base)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()