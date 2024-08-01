import pygame 
import math
import random
from pygame import mixer

#initialize the pygame 
pygame.init()

#create the screen with its size 
screen = pygame.display.set_mode((800,600))

#background Image 
background = pygame.image.load('space.jpg')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


#title and icon of the terminal 
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('ufo.png')
playerX = 370
playerY = 500
playerX_change = 0

#Enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,768))
    enemyY.append(random.randint(32,300))
    enemyX_change.append(0.3)
    enemyY_change.append(80)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'


#score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over text 

gfont = pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    gfont=font.render('Game Over',True,(255,255,255))
    screen.blit(gfont,(300,250))




def show_score(x, y):
    score = font.render('Score: ' + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

#player
def player(x,y):
    screen.blit(playerImg,(x,y))

#enemy
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y)) 

#fire bullet
def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(x,y+10))

#collision 
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27 :
        return True 
    else:
        return False



#hold the screen 
running = True 
while running:

    #Red Green Blue
    screen.fill((0,0,0)) 
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    #If keystroke is pressed check weather its right or left is pressed 
        if event.type == pygame.KEYDOWN:   #key on hold
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1  
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('gunshot.wav')
                    bullet_sound.play()
                    bulletX =playerX
                    fire_bullet(bulletX,bulletY)  
        if event.type == pygame.KEYUP:  #key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0 

    #player x axis movemets             
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768   

    #enemy x axis movements movements:
    for i in range(num_of_enemies):
        # game over 
        if enemyY[i] > 500:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text()   
            break 
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -0.5 
            enemyY[i]+=enemyY_change[i] 

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 500 
            bullet_state ='ready'
            score_val+=1
            enemyX[i] = random.randint(0,768)
            enemyY[i] = random.randint(32,300)    
        enemy(enemyX[i],enemyY[i],i)     
    #bullet movement
    if bulletY <=0:
        bulletY =500
        bullet_state='ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY) 
        bulletY -= bulletY_change  
    #collison 
    

    player(playerX,playerY)
    show_score(textX,textY)       
    pygame.display.update()   
    
