import pygame

import random
from button import Button, Image

pygame.init()

WIDTH, HEIGHT = 700, 500
WIDTH += 1
HEIGHT += 1
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake")

SCORE_FONT = pygame.font.SysFont("comicsans",30)

retry_image = pygame.image.load('retry.png')
apple_image = pygame.image.load('apple.png')

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (160,32,240)



class Rectangle:
    VEL = 20
    U, D, L, R = False, False, False, True


    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.moved = False


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


    def setudlr(self, u, d, l, r):
        self.U = u
        self.D = d
        self.L = l
        self.R = r


    def snake_moved(self,keys):
        if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] or self.moved == True:
            self.moved = True
            return True

    def move(self, up=False, down=False, left=False, right=False):
        if up:
            self.setudlr(True, False, False, False)
            self.y -= self.VEL
        if down:
            self.setudlr(False, True, False, False)
            self.y += self.VEL
        if left:
            self.setudlr(False, False, True, False)
            self.x -= self.VEL
        if right:
            self.setudlr(False, False, False, True)
            self.x += self.VEL


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

def handle_body(x,y,snake):
    snake_head_x = x
    snake_head_y = y
    for i in range(1, len(snake)):
        temp_x = snake[i].getX()
        temp_y = snake[i].getY()
        snake[i].setX(snake_head_x)
        snake[i].setY(snake_head_y)
        snake_head_x = temp_x
        snake_head_y = temp_y


def handle_movement(keys, snake):

    if keys[pygame.K_UP]:

        x = snake[0].getX()
        y = snake[0].getY()
        snake[0].move(up=True, down=False, left=False, right=False)
        handle_body(x, y,snake)


    if keys[pygame.K_DOWN]:

        x = snake[0].getX()
        y = snake[0].getY()
        snake[0].move(up=False, down=True, left=False, right=False)
        handle_body(x, y,snake)


    if keys[pygame.K_LEFT]:

        x = snake[0].getX()
        y = snake[0].getY()
        snake[0].move(up=False, down=False, left=True, right=False)
        handle_body(x, y,snake)


    if keys[pygame.K_RIGHT]:
        x = snake[0].getX()
        y = snake[0].getY()
        snake[0].move(up=False, down=False, left=False, right=True)
        handle_body(x, y,snake)


def draw(win, apple, snake, score, apple_i):
    win.fill(BLACK)
    apple.draw(win)
    apple_i.draw(win)


    score_text = SCORE_FONT.render(f'score: {score}',1,WHITE)
    win.blit(score_text,(WIDTH//2-40,20))


    for i in range(0, WIDTH, 20):
        pygame.draw.line(win, WHITE, (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT, 20):
        pygame.draw.line(win, WHITE, (0, i), (WIDTH, i))

    for s in snake:
        s.draw(win)





def generateX():
    return random.randrange(0, WIDTH-1, 20)


def generateY():
    return random.randrange(0, HEIGHT-1, 20)


def apple_eaten(snake, apple):
    if snake[0].getX()==apple.getX() and snake[0].getY()==apple.getY():
        return True
    else:
        return False



def new_snake(snake):

    if snake[-1].getY()-snake[-2].getY() == 0 and snake[-1].getX()-snake[-2].getX() == -20:    #if the two last parts of snake headed right
        new_s = Rectangle(snake[-1].getX() - 20, snake[-1].getY(), 20, 20, GREEN)
        return new_s

    elif snake[-1].getY()-snake[-2].getY() == 0 and snake[-1].getX()-snake[-2].getX() == 20:     #if the two last parts of snake headed left
        new_s = Rectangle(snake[-1].getX() + 20, snake[-1].getY(), 20, 20, GREEN)
        return new_s

    elif snake[-1].getY()-snake[-2].getY() == 20 and snake[-1].getX()-snake[-2].getX() == 0:      #if two last parts on to of each other and tail is at the bottom
        new_s = Rectangle(snake[-1].getX(), snake[-1].getY() + 20, 20, 20, GREEN)
        return new_s

    elif snake[-1].getY() - snake[-2].getY() == -20 and snake[-1].getX() - snake[-2].getX() == 0:     #if two last parts on to of each other and tail is on top
        new_s = Rectangle(snake[-1].getX(), snake[-1].getY() - 20, 20, 20, GREEN)
        return new_s



def new_apple(snake):
    x = generateX()
    y = generateY()
    tries = 0

    while True:

        for i in range(len(snake)):
            if snake[i].getX() != x or snake[i].getY() != y:
                tries += 1

        if tries == len(snake):
            break
        else:
            x = generateX()
            y = generateY()
            tries = 0


    apple = Rectangle(x, y, 20, 20, RED)
    return apple

def lost(snake):
    if snake[0].getX()<0 or snake[0].getX()>WIDTH-21 or snake[0].getY()<0 or snake[0].getY()>HEIGHT-1:  #check if snake outise the boards of the screen
        return True
    for i in range(1,len(snake)):
        if snake[0].getX()== snake[i].getX() and snake[0].getY()==snake[i].getY():      #check if snake eaten himself
            return True
    return False

def keep_moving(snake):
    x = snake[0].getX()
    y = snake[0].getY()
    snake[0].move(up=snake[0].U, down=snake[0].D, left=snake[0].L, right=snake[0].R)
    handle_body(x, y, snake)

def main():
    run = True
    clock = pygame.time.Clock()
    snake_head = Rectangle(140, 100, 20, 20, GREEN)
    snake_body = Rectangle(120, 100, 20, 20, GREEN)
    snake_tail = Rectangle(100, 100, 20, 20, GREEN)
    snake = [snake_head, snake_body, snake_tail]
    apple = new_apple(snake)
    apple_im = Image(apple.x,apple.y,apple_image)
    time_delay = 100
    score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, apple, snake,score,apple_im)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()

        two_buttons_pressed = (keys[pygame.K_UP] and keys[pygame.K_DOWN]) or (
                    keys[pygame.K_LEFT] and keys[pygame.K_RIGHT])

        if two_buttons_pressed:
            keep_moving(snake)

        if snake[0].snake_moved(keys):
            if (keys[pygame.K_UP] and snake[0].D == False) or (keys[pygame.K_DOWN]and snake[0].U == False) or (keys[pygame.K_LEFT] and snake[0].R == False) or (keys[pygame.K_RIGHT] and snake[0].L == False):
                if not two_buttons_pressed:
                    handle_movement(keys, snake)

            else:
                keep_moving(snake)



        if apple_eaten(snake, apple):
            score+=1
            snake.append(new_snake(snake))
            apple = new_apple(snake)
            apple_im = Image(apple.x,apple.y,apple_image)
            if time_delay >= 75:
                time_delay -= 1

        if lost(snake):
            lost_screen(score)

        pygame.display.update()

        pygame.time.delay(time_delay)




    pygame.quit()

def lost_screen(score):
    WIN.fill(BLACK)
    retry_button = Button(WIDTH // 2, HEIGHT // 2 , retry_image)
    score_text = SCORE_FONT.render(f'your score: {score}', 1, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - 175, 100))

    while True:

        retry_button.draw(WIN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if retry_button.mouse_on_button():
            main()



if __name__ == '__main__':
    main()
