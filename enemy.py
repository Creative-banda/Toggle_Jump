import pygame
import random
import os

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, SCREEN_WIDTH, y, scale):
        pygame.sprite.Sprite.__init__(self)
        # define variables
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        # load images from folder
            for i in range(8):  # Assuming 8 images named 1.png through 8.png
                img_path = os.path.join('assets/enemy', f'{i+1}.png')
                try:
                    image = pygame.image.load(img_path).convert_alpha()
                    # Scale the image
                    width = int(image.get_width() * scale)
                    height = int(image.get_height() * scale)
                    image = pygame.transform.scale(image, (width, height))
                    image = pygame.transform.rotate(image, -90)
                    # Flip if needed
                    if self.flip:
                        image = pygame.transform.flip(image, True, False)
                    self.animation_list.append(image)
                except pygame.error as e:
                    print(f"Couldn't load image {img_path}: {e}")
                    continue

        # select starting image and create rectangle from it
        if len(self.animation_list) > 0:
            try:
                self.image = self.animation_list[self.frame_index]
                self.rect = self.image.get_rect()
            except:
                pass
        else:
            print("No images loaded for enemy animation!")
            # Create a default red rectangle if no images are loaded
            self.image = pygame.Surface((32 * scale, 32 * scale))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH
        self.rect.y = y

    def update(self, scroll, SCREEN_WIDTH):
        # update animation
        ANIMATION_COOLDOWN = 50
        # update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        # move enemy
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        # check if gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()