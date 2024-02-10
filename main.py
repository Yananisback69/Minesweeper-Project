import pygame
import sys
import button

# Animation of title 
class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
      super().__init__()
      self.sprite = []
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-0.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-1.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-2.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-3.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-4.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-5.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-6.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-7.png"))
      self.sprite.append(pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixil-frame-8.png"))
      self.current_sprite = 0
      self.image = self.sprite[self.current_sprite]

      self.rect = self.image.get_rect()
      self.rect.topleft = [pos_x,pos_y]

    def update(self):
        self.current_sprite += 0.2 # slows down the animation 

        if self.current_sprite >= len(self.sprite):
            self.current_sprite = 0

        self.image = self.sprite[int(self.current_sprite)]










# This calls the __init__ functions of every pygame module
pygame.init()

# Loading background image
background_img = pygame.image.load("C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/pixel_night.jpg")




#Button images load
start_image = pygame.image.load('C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/Start.png')
difficulty_image = pygame.image.load('C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/Difficulty.png')
help_image = pygame.image.load('C:/Users/User\Documents/Year 12/Software Design and Development Y12/Group Major- Minesweeper/assets/Help.png')


# Creating button instances
start_button = button.Button(300,200, start_image, 4)
difficulty_button = button.Button(250,300, difficulty_image, 4)
help_button = button.Button(300,400, help_image, 4)






#Creating Sprites
moving_sprites = pygame.sprite.Group()
player = Player(250,50)
moving_sprites.add(player)



# Setting screen size
screen = pygame.display.set_mode((900,600))
pygame.display.set_caption("Minesweeper")
timer = pygame.time.Clock()

i = 0
#Main Loop
running = True
while running:
    timer.tick(60)
    screen.fill("white")
    screen.blit(background_img,(i,0))
    screen.blit(background_img, (900 +i, 0))

    # Conditions for the buttons 
    if start_button.draw(screen):
        print("START!")

    if difficulty_button.draw(screen):
        print("DIFFICULTY")

    if help_button.draw(screen):
        print("CANNOT HELP")


    moving_sprites.draw(screen)
    if i == -900:
        screen.blit(background_img, (900 +i, 0))
        i = 0

    pygame.display.flip()
    i -= 2

    moving_sprites.update()

    
    
    pygame.display.flip()
    
 
# Did the user click the window to close the button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()


