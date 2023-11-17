import pygame.mouse


class Button:
    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



    def draw(self,win):
        win.blit(self.image,(self.rect.x,self.rect.y))

    def mouse_on_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return True

