import pygame
import time
import random

# Initialize pygame
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600


# Create surface, must insert a tuple or list into set_mode
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

# Flip and Update are essentially the same
# pygame.display.flip()
# Mostly use update
# pygame.display.update()

block_size = 20
FPS = 15

smallFont = pygame.font.SysFont('comicsansms', 25)
medFont = pygame.font.SysFont('comicsansms', 50)
largeFont = pygame.font.SysFont('comicsansms', 80)

def pause():
    paused = True
    message_to_screen('Paused', black, -100, size='large')
    message_to_screen('Press C to continue or Q to quit', black, 20)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)

def score(score):
    text = smallFont.render('Score: ' + str(score), True, black)
    gameDisplay.blit(text, [0, 0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-block_size))#/10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height-block_size))#/10.0) * 10.0
    return randAppleX, randAppleY

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False              
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen('Welcome to Slither',
                            green,
                            -100,
                            'large')
        message_to_screen('The objective of the game is to eat red apples',
                            black,
                            -30)
        message_to_screen('The more apples you eat, the longer you get',
                            black,
                            10)
        message_to_screen('If you run into yourself, or the edges, you will die!',
                            black,
                            50)
        message_to_screen('Press C to play, P to pause, or Q to quit',
                            black,
                            180)
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

# Centers text
def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallFont.render(text, True, color)
    elif size == 'medium':
        textSurface = medFont.render(text, True, color)
    elif size == 'large':
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

clock = pygame.time.Clock()

def gameLoop():
    gameExit = False
    gameOver = False

    # head of snake
    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()
    
    while not gameExit:
        if gameOver == True:
            message_to_screen('Game Over', 
                                red, -50, 
                                size='large')
            message_to_screen('Press C to play again or Q to quit', 
                                black, 
                                50,
                                size='medium')
            pygame.display.update()
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False                   
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True


        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        appleThickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, appleThickness, appleThickness])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)

        score(snakeLength-1)

        pygame.display.update()

        if lead_x < randAppleX + appleThickness and lead_x > randAppleX - block_size and lead_y < randAppleY + appleThickness and lead_y > randAppleY - block_size:
            randAppleX, randAppleY = randAppleGen()
            snakeLength += 1

        # Frames per second
        clock.tick(FPS)

    # Unitialize pygame
    pygame.quit()
    quit()

game_intro()
gameLoop()