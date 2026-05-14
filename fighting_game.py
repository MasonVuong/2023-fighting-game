"""
Fighting_Game

Description:
"""

#Imports
import pygame as pg, pygame.freetype, sys
pg.init()
from random import *

#Set Up
clock = pg.time.Clock()
window = pg.display.set_mode((2000, 1250))
font = pg.freetype.Font("Acme-Regular.ttf", 50)
sound = pg.mixer.Sound("Whoop.mp3")
happy = pg.mixer.Sound("TahDah.mp3")
hits = pg.mixer.Sound("Squelch.mp3")
dead = pg.mixer.Sound("Splash.mp3")
pg.mouse.set_visible(False)

#Character Selection Variables
char_1 = 3
char_2 = 3

colors = [(0, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255)]

color_1_temp = 6
color_2_temp = 0

#Main Game Loop
play = True
while play:
    
    #Character Base Stats
    lives_1 = 3
    lives_2 = 3
    
    select_1 = True
    select_2 = True
    
    hp_1 = 100
    dmg_1 = 10
    speed_1 = 10
    range_1 = 100
    max_jump_1 = 2
    grav_1 = 5
    
    hp_2 = 100
    dmg_2 = 10
    speed_2 = 10
    range_2 = 100
    max_jump_2 = 2
    grav_2 = 5
    
    x_1 = 500
    y_1 = 750
    x_2 = 1500
    y_2 = 750
    
    jump_1 = False
    jump_2 = False
    
    jump_start_1 = 650
    jump_start_2 = 650
    
    jumps_1 = 0
    jumps_2 = 0
    
    start_1 = False
    start_2 = False
    
    #Character Selection Loop
    select = True
    run = True
    while select:
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                select = False
                run = False
                play = False
            if e.type == pg.KEYDOWN:
                #Player 1
                if select_1:
                    if e.key == pg.K_a:
                        char_1 -= 1
                        if char_1 < 1:
                            char_1 = 1
                    if e.key == pg.K_d:
                        char_1 += 1
                        if char_1 > 7:
                            char_1 = 7
                    if e.key == pg.K_w:
                        color_1_temp += 1
                        if color_1_temp > 6:
                            color_1_temp = 6
                    if e.key == pg.K_s:
                        color_1_temp -= 1
                        if color_1_temp < 0:
                            color_1_temp = 0
                    #Confirm Selection
                    if e.key == pg.K_SPACE and color_1_temp != color_2_temp:
                        select_1 = not select_1
                        sound.play()
                #Player 2
                if select_2:
                    if e.key == pg.K_LEFT:
                        char_2 -= 1
                        if char_2 < 1:
                            char_2 = 1
                    if e.key == pg.K_RIGHT:
                        char_2 += 1
                        if char_2 > 7:
                            char_2 = 7
                    if e.key == pg.K_UP:
                        color_2_temp += 1
                        if color_2_temp > 6:
                            color_2_temp = 6
                    if e.key == pg.K_DOWN:
                        color_2_temp -= 1
                        if color_2_temp < 0:
                            color_2_temp = 0
                    #Confirm Selection
                    if e.key == pg.K_RETURN and color_2_temp != color_1_temp:
                        select_2 = not select_2
                        sound.play()
        
        #Show Not Finalized Character Choice
        window.fill((0, 255, 255))

        color_1 = colors[color_1_temp]
        color_2 = colors[color_2_temp]
        
        if select_1:
            pg.draw.circle(window, color_1, (500, 750), 100)
            font.fgcolor = (color_1)
            if char_1 <= 6:
                font.render_to(window, (500, 1000), str(char_1))
            else:
                font.render_to(window, (500, 1000), "?")            
                
        if select_2:
            pg.draw.circle(window, color_2, (1500, 750), 100)
            font.fgcolor = (color_2)
            if char_2 <= 6:
                font.render_to(window, (1500, 1000), str(char_2))
            else:
                font.render_to(window, (1500, 1000), "?")
        
        #Give Stat Boosts for Character Selection
        if not select_1 and not select_2:
            char_1_temp = char_1
            if char_1 == 7:
                char_1_temp = randint(1, 6)
            if char_1_temp == 1:
                hp_1 = 150
            if char_1_temp == 2:
                dmg_1 = 15
            if char_1_temp == 3:
                speed_1 = 15
            if char_1_temp == 4:
                range_1 = 150
            if char_1_temp == 5:
                max_jump_1 = 3
            if char_1_temp == 6:
                grav_1 = 3
                
            char_2_temp = char_2
            if char_2 == 7:
                char_2_temp = randint(1, 6)
            if char_2_temp == 1:
                hp_2 = 150
            if char_2_temp == 2:
                dmg_2 = 15
            if char_2_temp == 3:
                speed_2 = 15
            if char_2_temp == 4:
                range_2 = 150
            if char_2_temp == 5:
                max_jump_2 = 3
            if char_2_temp == 6:
                grav_2 = 3
            
            #End Character Selection Loop
            select = False
        pg.display.flip()
    
    #Create Attack Box
    attack_1 = pg.Rect(x_1 + 100, y_1 - 100, range_1, 200)
    attack_2 = pg.Rect(x_2 - (100 + range_2), y_2 - 100, range_2, 200)	

    # Initialize hitboxes
    rect_1 = pg.Rect(x_1 - 100, y_1 - 100, 200, 200)
    rect_2 = pg.Rect(x_2 - 100, y_2 - 100, 200, 200)
    
    #Define Gameplay Variables (Attack State, Damage, Direction)
    atk_1 = False
    atk_2 = False
    
    launch_1 = 0
    launch_2 = 0
    
    direct_1 = "Right"
    direct_2 = "Left"

    win = False
    
    #Fighting Loop
    while run:
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
                play = False
            if e.type == pg.KEYDOWN:
                #Attack
                if e.key == pg.K_SPACE:
                    atk_1 = True
                    sound.play()
                if e.key == pg.K_RETURN:
                    atk_2 = True
                    sound.play()
                #Jump
                if e.key == pg.K_w:
                    jumps_1 += 1
                    if not jump_1 and jumps_1 <= max_jump_1:
                        jump_1 = True
                        jump_start_1 = y_1
                        
                if e.key == pg.K_UP:
                    jumps_2 += 1
                    if not jump_2 and jumps_2 <= max_jump_2:
                        jump_2 = True
                        jump_start_2 = y_2
        #Attack and Knockback
        if atk_1 and pg.Rect.colliderect(rect_2, attack_1):
            launch_2 += dmg_1 
            if direct_1 == "Up":
                y_2 -= (launch_2 * 10) - hp_2
            if direct_1 == "Left":
                x_2 -= (launch_2 * 10) - hp_2
            if direct_1 == "Down":
                if not y_2 in range(840, 860) or not x_2 in range(350, 1650):
                    y_2 += (launch_2 * 10) - hp_2
                if x_2 in range(350, 1650) and y_2 >= 850:
                    y_2 = 850
            if direct_1 == "Right":
                x_2 += (launch_2 * 10) - hp_2
            hits.play()     
            
        if atk_2 and pg.Rect.colliderect(rect_1, attack_2):
            launch_1 += dmg_2
            if direct_2 == "Up":
                y_1 -= (launch_1 * 10) - hp_1
            if direct_2 == "Left":
                x_1 -= (launch_1 * 10) - hp_1
            if direct_2 == "Down":
                if not y_1 in range(840, 860) or not x_1 in range(350, 1650):
                    y_1 += (launch_1 * 10) - hp_1
                if x_1 in range(350, 1650) and y_1 >= 850:
                    y_1 = 850
            if direct_2 == "Right":
                x_1 += (launch_1 * 10) - hp_1
            hits.play()            
                    
        window.fill((0, 255, 255))
        
        #Move
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            direct_1 = "Up"
        if keys[pg.K_a]:
            x_1 -= speed_1
            direct_1 = "Left"
        if keys[pg.K_s]:
            if not y_1 in range(840, 860):
                y_1 += speed_1
                jump_1 = False
            elif not x_1 in range(350, 1650):
                y_1 += speed_1
                jump_1 = False
            direct_1 = "Down"
        if keys[pg.K_d]:
            x_1 += speed_1
            direct_1 = "Right"

        if keys[pg.K_UP]:
            direct_2 = "Up"
        if keys[pg.K_LEFT]:
            x_2 -= speed_2
            direct_2 = "Left"
        if keys[pg.K_DOWN]:
            if not y_2 in range(840, 860):
                y_2 += speed_2
                jump_2 = False
            elif not x_2 in range(350, 1650):
                y_2 += speed_2
                jump_2 = False
            direct_2 = "Down"
        if keys[pg.K_RIGHT]:
            x_2 += speed_2
            direct_2 = "Right"
        
        if jump_1:
            y_1 -= speed_1
            if jump_start_1 - y_1 >= 250:
                jump_1 = False
                
        if jump_2:
            y_2 -= speed_2
            if jump_start_2 - y_2 >= 250:
                jump_2 = False
        
        #Death for Player 1
        if x_1 < 0 or x_1 > 2000 or y_1 < 0 or y_1 > 1250:
            dead.play()
            lives_1 -= 1
            launch_1 = 0
            if lives_1 > 0:
                x_1 = 500
                y_1 = 750
            
        #Game End for Player 1
        if lives_1 == 0:
            pg.draw.line(window, (100, 100, 100), (350, 950), (1650, 950), 50)
            pg.draw.line(window, (100, 100, 100), (500, 700), (1500, 700), 50)
            pg.draw.circle(window, (color_1), (x_1, y_1), 100)
            #pg.draw.rect(window, (color_1), attack_1) 
            pg.draw.circle(window, (color_2), (x_2, y_2), 100) 
            pg.draw.rect(window, (color_2), attack_2)
            rect_1 = pg.Rect(x_1 - 100, y_1 - 100, 200, 200)
            rect_2 = pg.Rect(x_2 - 100, y_2 - 100, 200, 200)
            font.fgcolor = (color_1)
            font.render_to(window, (500, 1000), str(lives_1) + "     x     " + str(launch_1))
            font.fgcolor = (color_2) 
            font.render_to(window, (1500, 1000), str(lives_2) + "     x     " + str(launch_2))
            pg.display.flip()
            pg.time.wait(1500)
            win = True
            window.fill(color_2)
            happy.play()
            
            pg.display.flip()
            while win:
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        run = False
                        win = False
                        play = False
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_e:
                            start_1 = True
                            sound.play()
                        if e.key == pg.K_RSHIFT:
                            start_2 = True
                            sound.play()
                if start_1 and start_2:
                    run = False
                    win = False
                    
        #Death for Player 2
        if x_2 < 0  or x_2 > 2000 or y_2 < 0 or y_2 > 1250:
            dead.play()
            lives_2 -= 1
            launch_2 = 0
            if lives_2 > 0:
                x_2 = 1500
                y_2 = 750
            
        #Game End for Player 2
        if lives_2 == 0:
            pg.draw.line(window, (100, 100, 100), (350, 950), (1650, 950), 50)
            pg.draw.line(window, (100, 100, 100), (500, 700), (1500, 700), 50)
            pg.draw.circle(window, (color_1), (x_1, y_1), 100)
            pg.draw.rect(window, (color_1), attack_1) 
            pg.draw.circle(window, (color_2), (x_2, y_2), 100) 
            #pg.draw.rect(window, (color_2), attack_2)
            rect_1 = pg.Rect(x_1 - 100, y_1 - 100, 200, 200)
            rect_2 = pg.Rect(x_2 - 100, y_2 - 100, 200, 200)
            font.fgcolor = (color_1)
            font.render_to(window, (500, 1000), str(lives_1) + "     x     " + str(launch_1))
            font.fgcolor = (color_2) 
            font.render_to(window, (1500, 1000), str(lives_2) + "     x     " + str(launch_2))
            pg.display.flip()
            pg.time.wait(1500)
            win = True
            window.fill(color_1)
            happy.play()
            pg.display.flip()
            while win:
                for e in pg.event.get():
                    if e.type == pg.QUIT:
                        run = False
                        win = False
                        play = False
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_e:
                            start_1 = True
                            sound.play()
                        if e.key == pg.K_RSHIFT:
                            start_2 = True
                            sound.play()
                if start_1 and start_2: 
                    run = False
                    win = False
                        
        if not y_1 in range(840, 860):
            if y_1 in range(590, 610) and x_1 in range(500, 1500):
                if not jump_1:
                    jumps_1 = 0
            else:
                y_1 += grav_1
        elif not x_1 in range(350, 1650):
            y_1 += grav_1
            
        else:
            if not jump_1:
                jumps_1 = 0
            
        if not y_2 in range(840, 860):
            if y_2 in range(590, 610) and x_2 in range(500, 1500):
                if not jump_2:
                    jumps_2 = 0
            else:
                y_2 += grav_2
        elif not x_2 in range(350, 1650):
            y_2 += grav_2
        else:
            if not jump_2:
                jumps_2 = 0
            
        if direct_1 == "Up":
            attack_1 = pg.Rect(x_1 - 100, y_1 - (100 + range_1), 200, range_1)
        if direct_1 == "Left":
            attack_1 = pg.Rect(x_1 - (100 + range_1), y_1 - 100, range_1, 200)
        if direct_1 == "Down":
            attack_1 = pg.Rect(x_1 - 100, y_1 + 100, 200, range_1)
        if direct_1 == "Right":
            attack_1 = pg.Rect(x_1 + 100, y_1 - 100, range_1, 200)

        if direct_2 == "Up":
            attack_2 = pg.Rect(x_2 - 100, y_2 - (100 + range_2), 200, range_2)
        if direct_2 == "Left":
            attack_2 = pg.Rect(x_2 - (100 + range_2), y_2 - 100, range_2, 200)
        if direct_2 == "Down":
            attack_2 = pg.Rect(x_2 - 100, y_2 + 100, 200, range_2)
        if direct_2 == "Right":
            attack_2 = pg.Rect(x_2 + 100, y_2 - 100, range_2, 200)    
            
        pg.draw.line(window, (100, 100, 100), (350, 950), (1650, 950), 50)
        pg.draw.line(window, (100, 100, 100), (500, 700), (1500, 700), 50)
        pg.draw.circle(window, (color_1), (x_1, y_1), 100)
        pg.draw.rect(window, (color_1), attack_1) 
        pg.draw.circle(window, (color_2), (x_2, y_2), 100) 
        pg.draw.rect(window, (color_2), attack_2)
        rect_1 = pg.Rect(x_1 - 100, y_1 - 100, 200, 200)
        rect_2 = pg.Rect(x_2 - 100, y_2 - 100, 200, 200)
        font.fgcolor = (color_1)
        font.render_to(window, (500, 1000), str(lives_1) + "     x     " + str(launch_1))
        font.fgcolor = (color_2) 
        font.render_to(window, (1500, 1000), str(lives_2) + "     x     " + str(launch_2))
            
        atk_1 = False
        atk_2 = False
        
        pg.display.flip()
        clock.tick(60)




