import pygame

# button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.original_image = image
        self.image_scale = scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center=(x, y))  # Set the center of the button
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.clicked = False

        # temporarily increase size when hovered
        if self.rect.collidepoint(pos):
            scale_factor = self.image_scale + (self.image_scale * 0.1)
        else:
            scale_factor = self.image_scale

        # update the button size and position based on the scale factor
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale_factor),
                                                                  int(self.original_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(center=self.rect.center)

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Title:
    def __init__(self, x, y, image, scale):
        self.original_image = image
        self.image_scale = scale
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.last_change_time = pygame.time.get_ticks()
        self.scale_up = True

    def toggle_scale(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_change_time >= 1000:  # 1000 milliseconds = 1 second
            self.last_change_time = current_time
            self.scale_up = not self.scale_up

    def draw(self, surface):
        self.toggle_scale()

        if self.scale_up:
            scale_factor = self.image_scale + (self.image_scale * 0.05)
        else:
            scale_factor = self.image_scale - (self.image_scale * 0.05)

        self.image = pygame.transform.scale(self.original_image,
                                            (int(self.original_image.get_width() * scale_factor),
                                             int(self.original_image.get_height() * scale_factor)))
        self.rect = self.image.get_rect(center=self.rect.center)
        surface.blit(self.image, (self.rect.x, self.rect.y))
