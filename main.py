class TileFunction:
            def __init__(self, x, y, image, w, h):
                self.image = pygame.transform.scale(image, (w, h))
                self.rect = self.image.get_rect()
                self.rect.topleft = (x, y)
                self.state = "normal"
                self.is_mine = False
                self.adjacent_mines = 0
                # self.tile_blank = False

            def draw(self, surface):

                global clicked
                global clicks

                action = False

                # get mouse position
                
                pos = pygame.mouse.get_pos()
                
                # flag mouse over button

                if self.rect.collidepoint(pos):
                    
                    # Left Click!
                    if pygame.mouse.get_pressed()[0] == 1 and self.state == "normal":
                        clicks += 1
                        print(clicks)

                        tile_row = int(pos[1]//100) + 1
                        tile_col = int(pos[0]//100) + 1
                    
                        clicked = (tile_row, tile_col)

                        dug.add(clicked)

                        if clicks == 0 or clicks == 1:  # Check if it's the first or second click
                            if self.is_mine or self.adjacent_mines > 0:
                                reset_grid()
                            else:
                                clear_grid(tile, dug)
                        else:
                            if self.is_mine:
                                self.image = bomb_tile  # Change to bomb_tile if it's a mine
                            elif self.adjacent_mines > 0:
                                self.image = number_tiles[self.adjacent_mines - 1]  # Change to number_tile based on adjacent mines.-1 is there to match the image from the list 'number_tiles'
                                dug.add(clicked)
                            elif self.adjacent_mines == 0:
                                clear_grid(tile, dug)

                        self.image = pygame.transform.scale(self.image, (100, 100))  # resizing the image
                        self.state = "clicked"  # now can't click it again
                        action = True
