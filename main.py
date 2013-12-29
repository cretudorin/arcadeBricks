import pygame
import Tkinter
import sys
from pygame.locals import *
from random import choice, randrange

### init ###
pygame.font.init()
root_tk = Tkinter.Tk()
pygame.init()

    #mouse
pygame.mouse.set_visible(False)

    #on screen display
font = pygame.font.Font(None, 40)
font_big = pygame.font.Font(None, 250)

    #game paused
game_paused = False
temp_acc = [0, 0]

#get screen info
screen_size = (root_tk.winfo_screenwidth(), root_tk.winfo_screenheight())

#intial consts
lives = 1
bgcolor = (0, 0, 0)
gameLoop = True
paddle_coord = [screen_size[0] / 2 - 300, screen_size[1] - 20]
arrow_move = 0


class OSD():
    def __init__(self, lives):
        self.live = font.render("Lives: %s" % str(lives), 1, (255, 255, 255))
        #scoretext = font.render("Score:", 1, (255, 255, 255))
        self.gameOver = font.render("", 5, (255, 0, 0))
        self.pause = font_big.render("", 15, (255, 255, 255))
        
    def update_lives(self):
        global lives
        lives -= 1
        self.live = font.render("Lives: %s" % lives, 1, (255, 255, 255))
    def paused(self):
        if game_paused == True:
            self.pause = font_big.render("Pause", 15, (255, 255, 255))
        else : 
            self.pause = font_big.render("", 15, (255, 255, 255))
    def game_over(self):
        if lives == 0:
            self.gameOver = font_big.render("Game Over!", 15, (255, 255, 255))
        else:
            self.gameOver = font_big.render("", 15, (255, 255, 255))
osd = OSD(lives)


class Screen():

    def __init__(self):
        self.root = pygame.display.set_mode(screen_size, FULLSCREEN|DOUBLEBUF)
        self.root.fill(bgcolor)
        pygame.display.flip()
            
screen = Screen()


class Ball():

    def __init__(self):
        self.acc = [choice([-5, -4, -3, -2, -1, 1, 2, 3,  4, 5]), choice([4, 5]), 0, 0]
        self.coord = [(screen_size[0] - 300) / 2 - 30, screen_size[1] - 82]
        self.root = pygame.image.load("scaled2.png").convert_alpha()
        screen.root.blit((self.root), (self.coord[0], self.coord[1]))
        pygame.display.update()
        
    def reset(self):
        global paddle_coord, lives, game_paused, temp_acc
        game_paused = False
        temp_acc = [0, 0]
        osd.update_lives()
        osd.game_over()
        paddle_coord = [screen_size[0] / 2 - 300, screen_size[1] - 20]
        self.coord = [(screen_size[0] - 300) / 2 - 30, screen_size[1] - 82]
        if lives > 0:
            self.acc = [choice([-5, -4, -3, -2, -1, 1, 2, 3,  4, 5]), choice([4, 5]), 0, 0]
        else:
            self.acc = [0, 0]     
            
ball = Ball()

class Blocks():
    
    def __init__(self,blocks_x, blocks_y):
        self.coord = [blocks_x, blocks_y]
        self.root = pygame.Rect(self.coord[0], self.coord[1], 95, 35)
        self.color = randrange(255), randrange(255), randrange(255)
    def update(self):
        ball_width = (ball.coord[0] - 6, ball.coord[0] + 6)
        for x in ball_width:
            if x in xrange(self.coord[0],
                                       self.coord[0] + 91) and ball.coord[1] in xrange(self.coord [1],
                                                                                       self.coord[1] + 31):
                self.coord = (0,0,0)
                self.color = 0, 0, 0
                ball.acc[1] = -ball.acc[1]
            
#create blocks
blocks = []
def create_blocks():
    
    global blocks
    if len(blocks) > 1: 
        blocks = []
    blocks_x = [30]
    blocks_y = [38]
    i = 1
    while i < 10:
        blocks_y.append(blocks_y[i-1] + 100)
        if  i < 8:
            blocks_x.append(blocks_x[i-1] + 40)
        i += 1 
                
    for x in blocks_x:
        for y in blocks_y:
            blocks.append(Blocks(y, x))
    return blocks

create_blocks()

#create background lines
temp_coords = [[0, 0, screen_size[0], 5],
              [0, 0, 5, screen_size[1]],
              [screen_size[0] - 5, 0, 5 , screen_size[1]], 
              [screen_size[0] - 300, 0, 5, screen_size[1]],
              [screen_size[0] - 300, screen_size[1] - 5, 300, screen_size[1]]]
background_lines = []
for i in xrange(0, len(temp_coords)):
    background_lines.append(pygame.Rect(temp_coords[i]))
    
### main loop ###
while gameLoop == True:

### get events ###
    for event in pygame.event.get():   
 
        # quit     
        if event.type == pygame.QUIT:
            gameLoop = False
            pygame.quit()
            sys.exit()
        
        #key down    
        elif event.type == pygame.KEYDOWN:   
            
            #quit
            if event.key == pygame.K_q:
                gameLoop = False
                root_tk.quit()
                pygame.quit()
                sys.exit()
            
            #reset 
            if event.key == pygame.K_r:
                lives = 3
                ball.reset()
                game_paused = False
                osd.paused()
                create_blocks()
                osd.game_over()
            
            #pause
            if event.key == pygame.K_p:
                if game_paused == False:
                    temp_acc = ball.acc
                    ball.acc = [0, 0]
                    game_paused = True
                    osd.paused()
                elif game_paused == True:
                    ball.acc = temp_acc
                    game_paused = False
                    osd.paused()
                    
            #arrows    
            elif event.key == K_LEFT:
                arrow_move = -7
            elif event.key == K_RIGHT:
                arrow_move = 7
            
        #keys up        
        if event.type == pygame.KEYUP:
            
            #arrows
            if event.key == K_LEFT:
                arrow_move = 0
            elif event.key == K_RIGHT:
                arrow_move = 0
    
### paddle ###
    if game_paused == False:
        paddle = pygame.Rect(paddle_coord[0], paddle_coord[1], 300, 20)
        paddle_coord[0] += arrow_move
    else :
        paddle = pygame.Rect(paddle_coord[0], paddle_coord[1], 300, 20)
        paddle_coord[0] += 0
    #move paddle
    
    
    #collision for paddle
    if paddle_coord[0] > screen_size[0] - paddle.width - 300:
        paddle_coord[0] = screen_size[0] - paddle.width - 300
        
    if paddle_coord[0] < 0:
        paddle_coord[0] = 0

### ball ###

    #ball acceleration
    ball.coord[0] += ball.acc[0]
    ball.coord[1] -= ball.acc[1]
    
    #collision with paddle
    paddle_collision_range = xrange(paddle_coord[0], 
                            paddle_coord[0] + paddle.width + 1)
    if ball.coord[1] > screen_size[1] - ball.root.get_height() and ball.coord[0] in paddle_collision_range:
        ball.acc[1] = -ball.acc[1] 
       
    if ball.coord[1] > screen_size[1] - ball.root.get_height() and ball.coord[0] not in paddle_collision_range:
        ball.reset()
 
    #collision top wall
    if ball.coord[1] < 0:
        ball.acc[1] = -ball.acc[1]
    
    #collision left wall
    elif ball.coord[0] < 0:
        ball.acc[0] = -ball.acc[0]
        
    #collision right wall    
    elif ball.coord[0] > screen_size[0] - 300 - ball.root.get_width(): 
        ball.acc[0] = -ball.acc[0]
 
### draw ### 
    
    #background color
    screen.root.fill(bgcolor)
    
    #create background lines
    for item in background_lines:
        pygame.draw.rect(screen.root,(255, 0, 0), item)
    
    #blocks
    for item in blocks:
        pygame.draw.rect(screen.root,(item.color),item.root)
        item.update()
    
    #on screen display
    screen.root.blit(osd.gameOver, (screen_size[0] / 2 - font_big.size("Game Over!")[0] / 2,
                                    screen_size[1] / 2 - font_big.size("Game Over!")[1] / 2))
    screen.root.blit(osd.pause, (screen_size[0] / 2 - font_big.size("Pause")[0] / 2,
                                    screen_size[1] / 2 - font_big.size("Pause")[1] / 2))
    screen.root.blit(osd.live, (screen_size[0] - 200, 50))
        
    #ball
    screen.root.blit((ball.root), (ball.coord[0], ball.coord[1]))
    
    #create paddle
    pygame.draw.rect(screen.root, (255, 0, 0), paddle)
    
    #display update
    pygame.display.flip()
    
