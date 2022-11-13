from cgitb import text
from turtle import Screen, speed
import pygame, sys

import pygame
import os
import random


from button import Button
from player import Player
from enemy import Enemy, Boss
from utils import collide
from consts import WIDTH, HEIGHT, BLACK
         
#item
from item import Item
from item import PowerUp
from item import LiveUp

#sound
from pygame import mixer
pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()

#Load sounds
Gameover_fx = pygame.mixer.Sound("SoundEffect/GameoverSound.wav")
Gameover_fx.set_volume(0.50)

GetItem_fx = pygame.mixer.Sound("SoundEffect/Get_Item.wav")
GetItem_fx.set_volume(0.20)

MouseClick_fx = pygame.mixer.Sound("SoundEffect/ClickMouse.mp3")
MouseClick_fx.set_volume(0.50)
#end

#.json            
import json
from operator import itemgetter
#end

pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE REVENGER")

#Background
BG =pygame.transform.scale(pygame.image.load("Map/map.jpg"),(WIDTH,HEIGHT))

#Cutscene
CUTSCENE_1 = pygame.transform.scale(pygame.image.load("Cutscene/Cover.png"),(WIDTH,HEIGHT))
CUTSCENE_2 = pygame.transform.scale(pygame.image.load("Cutscene/ENEMY.png"),(WIDTH,HEIGHT))
CUTSCENE_3 = pygame.transform.scale(pygame.image.load("Cutscene/BOSS.png"),(WIDTH,HEIGHT))
CUTSCENE_4 = pygame.transform.scale(pygame.image.load("Cutscene/Item.png"),(WIDTH,HEIGHT))
CUTSCENE_5 = pygame.transform.scale(pygame.image.load("Cutscene/Cover.png"),(WIDTH,HEIGHT))

#Endscene
ENDSCENE_BG = pygame.transform.scale(pygame.image.load("Map/EndsceneBG.png"),(WIDTH,HEIGHT))

#Playerscore        
playername = ''
startDel = 0
isCooldown = 0

#Main font
main_font = pygame.font.SysFont("comicsans", 30)



def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.SysFont("comicsans", size)

def game():
    running = True
    FPS = 60
    level = 0
    lives = 15

    enemies = []
    items = []                       
    powerUp = []
    liveUp = []

    player_score = 0
    wave_length = 5
    laser_vel = 8

    player = Player(round(WIDTH/2)-40, HEIGHT - 100)

    clock = pygame.time.Clock()
   
    boss_spawned = True
    
    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, BLACK)
        level_label = main_font.render(f"Level: {level}", 1, BLACK)
        score_label = main_font.render(f"Score: {player_score}", 1, BLACK)
        
        WIN.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 50))
        WIN.blit(score_label, (10, 10))

        # draw enemies ship
        for en in enemies:
            en.draw(WIN)
        #heal item         
        for item in items:
            item.draw(WIN)
        #power item                                    
        for power_item in powerUp:
            power_item.draw(WIN)
        #live up item
        for live_item in liveUp:
            live_item.draw(WIN)

        # draw player ship
        player.draw(WIN)

    while running:
        clock.tick(FPS)
        redraw_window()

        #Playerscore
        player_score +=  player.Playerscore
        player.Playerscore = 0
       
        if lives <= 0 or player.health <= 0 or level == 8:
            scoreName(player_score)
            updatescore()
    
        #spawned enemies
        if len(enemies) == 0 and level <=7 :

            if boss_spawned is True :
                level += 1

                if level == 8 :
                    scoreName(player_score)
                    endScene()
                    
                #heal item
                item = Item(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50))
                items.append(item)
                #power item
                power_item = PowerUp(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50))
                powerUp.append(power_item)
                player.damage = 5                      #reset player damage after get pow when level + 1
                #live item
                live_item = LiveUp(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50))
                liveUp.append(live_item)
                
                wave_length += 3            
                boss_spawned = False 
                for i in range(wave_length):
                    if level == 1:
                        enemy = Enemy(random.randrange(0, WIDTH - 50 ), random.randrange(-800 + level * 100, -50),random.choice(["red"]))
                    elif level == 2:
                        enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),random.choice(["green"]))
                    elif level == 3:
                        enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),random.choice(["blue"]))
                    elif level == 4:
                        enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),random.choice(["blue","green"]))
                    elif level == 5 :
                        enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),random.choice(["red","green"]))
                    elif level == 6 :
                        enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),random.choice(["red","blue"]))
                    elif level == 7 :
                        enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-800 + level * 100, -50),random.choice(["red","green","blue"]))                                                            

                    enemies.append(enemy)
            else:
                if level <= 7:
                    boss = Boss(round(300), -100, level)
                    enemies.append(boss)
                boss_spawned = True
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:                             #press esc to exit
                    print("escape pressed")
                    pygame.quit()
                    running = False

        # player control
        keys = pygame.key.get_pressed()
        player.move(keys)                              

        for enemy in enemies[:]:
            enemy.move()
            enemy.move_lasers(laser_vel, player)
           
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):                 #overlap player กับ enemy
                player.health -= 5
                if player_score != 0:
                    player_score  -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:             #enemy out of screen
                lives -= 1
                
                if player_score != 0:
                    player_score -= 10
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        #heal item
        for item in items[:]:
            if collide(item,player):
                GetItem_fx.play()
                if player.health !=100 :
                    player.health += 10
                items.remove(item) 
        #power item
        for power_item in powerUp[:]:
            if collide(power_item,player):
                GetItem_fx.play()
                player.damage += 5
                powerUp.remove(power_item) 
        # live item 
        for live_item in liveUp[:]:
            if collide(live_item,player):
                GetItem_fx.play()
                lives +=1
                liveUp.remove(live_item)     

        pygame.display.update()

#Score 
def scoreName(player_score):
    global playername
    global startDel
    global isCooldown
    
    Gameover_fx.play()
    while True:
        WIN.blit(BG, (0, 0))
        
        GameOver = get_font(60).render("Game Over", True, "White")
        WIN.blit(GameOver, (130,100))

        EnterName = get_font(40).render("Please Enter your name", True, "White")
        WIN.blit(EnterName, (80,200))

        PLAYERSCORE = main_font.render(f"PlayerScore: {playername,player_score}", 1, BLACK)
        WIN.blit(PLAYERSCORE, (130, 300))

        NAME_TEXT = get_font(25).render("Teeruth Ieowsakulrat 65010495", True, "Orange")
        NAME_RECT = NAME_TEXT.get_rect(center=(400, 670))
        WIN.blit(NAME_TEXT, NAME_RECT)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if playername.replace(" ","") == "":
                        playername = "Unknown"
                    
                    with open('score.json', 'r') as file:            #read
                        playerScore = json.load(file)

                    playerScore.append([playername,int(player_score)])
                    playerScore = sorted(playerScore,reverse= True, key=itemgetter(1))
                    if len(playerScore) > 5:
                        playerScore.pop()                     #take out

                    with open('score.json', 'w+') as file:
                        json.dump(playerScore,file)            
                    return
                elif not event.key == pygame.K_BACKSPACE:
                    playername += event.unicode
                    
        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and not isCooldown:
            isCooldown = True
            startDel = pygame.time.get_ticks()         #start time counter
            if len(playername) <= 1:
                playername = ""
            else:
                playername = playername[:-1]        #Remove last character

        if len(playername) > 15:        #playername length
            playername = playername[:15]

        if (pygame.time.get_ticks() - startDel)/1000 >= 0.3 and isCooldown:
            isCooldown = False

        pygame.display.update()

#UpdateScore    
def updatescore():
    while True:
        UPDATESCORE_MOUSE_POS = pygame.mouse.get_pos()

        WIN.blit(BG, (0, 0))

        UPDATESCORE_TEXT = get_font(70).render("Leaderboard", True, "#FFD700")
        UPDATESCORE_RECT = UPDATESCORE_TEXT.get_rect(center=(300, 100))
        WIN.blit(UPDATESCORE_TEXT, UPDATESCORE_RECT)

        #read file
        with open('score.json', 'r') as file:            
            playerScore = json.load(file)

        for i,score in enumerate(playerScore):
        
        #Name
            NAME_TEXT = get_font(45).render(score[0], True, "White")
           # NAME_RECT = NAME_TEXT.get_rect(200, 200+(i*50))
            WIN.blit(NAME_TEXT, (100,150+ i*50))

        #Score
            SCORE_TEXT = get_font(45).render(str(score[1]), True, "White")
           # SCORE_RECT = SCORE_TEXT.get_rect(center=(400, 200+(i*50)))
            WIN.blit(SCORE_TEXT, (400,150+ i*50))

        UPDATESCORE_BACK = Button(image=None, pos=(300, 600), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="#FFD700")

        UPDATESCORE_BACK.changeColor(UPDATESCORE_MOUSE_POS)
        UPDATESCORE_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if UPDATESCORE_BACK.checkForInput(UPDATESCORE_MOUSE_POS):
                    MouseClick_fx.play()
                    main_menu()

        pygame.display.update()

#start cutscene
def cutScene():

    cutscene_font = pygame.font.SysFont("comicsans", 30)
    clock = pygame.time.Clock()

    messages = ['Welcome to space revenger.',                                    #Cutscene 1
                'You have to Survival from enemies.',                            #Cutscene 2
                'And eliminate all enemies.',                                    #Cutscene 3
                'Use items for strengthen',                                      #Cutscene 4
                'Click Anyway to Start the game']                                #Cutscene 5

    Cutscene_text = cutscene_font.render('',True,'white')
    counter = 0
    textspeed = 3
    active_message = 0
    message = messages[active_message]

    page = 0
    done = False
    run = True
    
    while run:
        WIN.blit(CUTSCENE_1, (0, 0))
        clock.tick(60)
        pygame.draw.rect(WIN,(255,255,255),(0,520,800,300)) 
        pygame.draw.rect(WIN,'black',[0,530,800,160])

        if counter < textspeed *  len(message):
            counter += 1  
        elif counter >= textspeed * len(message):
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN :
                    active_message += 1                 #next sentence
                    done = False
                    message = messages[active_message]
                    counter = 0
                    page +=1 
                    MouseClick_fx.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                MouseClick_fx.play()
                game()
        
        if page == 1:
            WIN.blit(CUTSCENE_2, (0, 0))
            pygame.draw.rect(WIN,(255,255,255),(0,520,800,300)) 
            pygame.draw.rect(WIN,'black',[0,530,800,160])
        if page == 2:
            WIN.blit(CUTSCENE_3, (0,0))
            pygame.draw.rect(WIN,(255,255,255),(0,520,800,300)) 
            pygame.draw.rect(WIN,'black',[0,530,800,160])   
        if page == 3:
            WIN.blit(CUTSCENE_4, (0,0))
            pygame.draw.rect(WIN,(255,255,255),(0,520,800,300)) 
            pygame.draw.rect(WIN,'black',[0,530,800,160])   
        if page == 4:
            WIN.blit(CUTSCENE_5, (0,0))
            pygame.draw.rect(WIN,(255,255,255),(0,520,800,300)) 
            pygame.draw.rect(WIN,'black',[0,530,800,160])   

        Cutscene_text = cutscene_font.render(message[0:counter],True,'white')
        WIN.blit(Cutscene_text,(10,560))

        pygame.display.flip()

#end cutscene
def endScene():

    endscene_font = pygame.font.SysFont("comicsans", 30)
    clock = pygame.time.Clock()

    messages = ['You save the world.',
                'Click anyway to Leaderboard' ]

    Endscene_text = endscene_font.render('',True,'white')
    counter2 = 0
    textspeed2 = 2
    active_message = 0
    message = messages[active_message]
    done = False
    run = True
    
    while run:
        WIN.blit(ENDSCENE_BG, (0, 0))
        clock.tick(60)
        pygame.draw.rect(WIN,(255,255,255),(0,520,800,300)) 
        pygame.draw.rect(WIN,'black',[0,530,800,160])

        if counter2 < textspeed2 *  len(message):
            counter2 += 1
        elif counter2 >= textspeed2 * len(message):
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN :
                    active_message += 1                 #next sentence
                    done = False
                    message = messages[active_message]
                    counter2 = 0
                    MouseClick_fx.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                MouseClick_fx.play()
                updatescore()
        Endscene_text = endscene_font.render(message[0:counter2],True,'white')
        WIN.blit(Endscene_text,(10,560))     

        pygame.display.flip()

def main_menu():
    while True:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(65).render("SPACE REVENGER", True, "#FFD700")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Menu/Play_Rect.png"), pos=(300, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCORE_BUTTON = Button(image=pygame.image.load("Menu/Play_Rect.png"), pos=(300, 400), 
                            text_input="SCORE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Menu/Play_Rect.png"), pos=(300, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        #Teeruth 650104953
        NAME_TEXT = get_font(25).render("Teeruth Ieowsakulrat 65010495", True, "Orange")
        NAME_RECT = NAME_TEXT.get_rect(center=(400, 670))

        WIN.blit(NAME_TEXT, NAME_RECT)
        
        for button in [PLAY_BUTTON, SCORE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS): 
                    MouseClick_fx.play() 
                    cutScene()
                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MouseClick_fx.play()
                    updatescore()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MouseClick_fx.play()
                    pygame.quit()
                    sys.exit()
                
        pygame.display.update()
main_menu()