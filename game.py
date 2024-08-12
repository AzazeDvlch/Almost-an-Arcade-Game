import random
import pygame, sys, os
import math
import time
import ctypes

pygame.font.init()
pygame.init()
screen_info = pygame.display.Info()
win_width = screen_info.current_w
win_height = screen_info.current_h
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("A Game perhaps?")

# Define colors
Black = (0, 0, 0)
White = (255, 255, 255)
Blue = (2,55,55)
green = (0, 255, 0)
bright_green = (0, 200, 0)
red = (255, 0, 0)
bright_red = (200, 0, 0)
grey = (200, 200, 200)
blue = (50, 50, 200)
bright_blue = (50,50,130)

# Load the images
image_path = "enemie.png" 
image = pygame.image.load(image_path)
image_path2 = "player.png"
image2 = pygame.image.load(image_path2)
image_path3 = "enemie2.png"
image3 = pygame.image.load(image_path3)
image_path4 = "projectile.png"
image4 = pygame.image.load(image_path4)
image_path5 = "laser1.png"
image5 = pygame.image.load(image_path5)
image_path6 = "healthbonus.png"
image6 = pygame.image.load(image_path6)
image_path7 = "Fatenemie.png"
image7 = pygame.image.load(image_path7)
image_path8 = "Smollenemy.png"
image8 = pygame.image.load(image_path8)
image_path9 = "background.png"
image9 = pygame.image.load(image_path9)
image_path10 = "NukaCola.png"
image10 = pygame.image.load(image_path10)

# initialization
timer = time.time()
last_collision_time = time.time()
#start_time = pygame.time.get_ticks()
score = 0
left = 1
right = 3
thresh = 50
thresh2 = 500
thresh3 = 1500
size = [700, 500]
endlessMode = False    
    
# Player variables
player_x, player_y = 1000, 500
player_width, player_height = 40, 27
player_vel = 5
player_health = 3

# Enemy variables
enemy_width, enemy_height = 28, 28
enemy_vel = 3
enemies = []
last_spawn_time = 0

# FatEnemy variables
Fatenemy_width, Fatenemy_height = 70, 70
Fatenemy_vel = 6
Fatenemies = []
last_spawn_timeFat = 0

# SmollEnemy variables
SE_width, SE_height = 18, 18
SE_vel = 7.5
SEnemies = []
last_spawn_timeSmoll = 0

# Enemy2 variables
enemy2_width, enemy2_height = 37, 37
enemy2_vel = 5.1
enemies2 = []
last_spawn_time2 = 0

# healtbonus variables
hb_width, hb_height = 15, 15
hb_vel = 1.2
hbs = []
last_spawn_timehb = 0
bonus = random.randint(1, 3)

# nukeCharge variables
nC_width, nC_height = 25, 25
nC_vel = 1.5
nCs = []
last_spawn_timenC = 0

# Initialize pause state
pause = False

def scaling(): 
    global enemy_vel, bulletTime, score, bullet_vel, player_vel
    if score >= thresh:
        enemy_vel += 0.0002
        bulletTime -= 0.00000015
    if score >= thresh2:
        enemy_vel += 0.0003
        bulletTime -= 0.0000002
        player_vel += 0.0001
    if score >= thresh2 and bullet_vel <= 13:
        bullet_vel += 2    
    if score >= thresh3 and endlessMode == False:
        ctypes.windll.user32.MessageBoxW(0, "This is the intended end, congrats and try finger but Marika...", 0)
        reset()

def button(msg, x, y, w, h, inactive_color, active_color, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(win, active_color, (x, y, w, h))
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(win, inactive_color, (x, y, w, h))

    font = pygame.font.SysFont("comicsansms", 20)
    text_surf, text_rect = text_objects(msg, font)
    text_rect.center = (x + w / 2, y + h / 2)
    win.blit(text_surf, text_rect)

def text_objects(text, font):
    text_surface = font.render(text, True, Black)
    return text_surface, text_surface.get_rect()

def paused():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill(Black)
        large_text = pygame.font.SysFont("comicsansms", 115)
        text_surf, text_rect = text_objects("Paused", large_text)
        text_rect.center = (size[0] / 2, size[1] / 2)
        win.blit(text_surf, text_rect)
        win.blit(image9, (0, 0, 3000, 300))

        button1 = button("Continue", 700, 450, 100, 50, green, bright_green, unpause)
        button2 = button("Quit", 1100, 450, 100, 50, red, bright_red, quit_game)
        button3 = button("Info", 900, 450, 100, 50, White, grey, info)
        button4 = button("Reset", 875, 575, 150, 75, blue, bright_blue, reset)
        button5 = button("Endless Mode", 875, 300, 150, 75, White, grey, endless)

        pygame.display.update()

def endless():
    global endlessMode
    if endlessMode == False:
        endlessMode = True
    else:
        endlessMode = False

def showEndless():
    if endlessMode == True:
        return "On"      
    if endlessMode == False:
        return "Off"  
# Function to unpause the game
def unpause():
    global pause
    pause = False
def quit_game():
    pygame.quit()
    quit()
def info():
    ctypes.windll.user32.MessageBoxW(0, "W = up,     A = left,   S = down,   D = right, E = Nuke,   Mouse1/SPACE = shoot,   Mouse2 = big shot", "Why u readin dis?", 0)
    print("this loser needs tips xD")
def reset():
    global player_x, player_y, player_health, player_vel
    global enemies, enemies2, Fatenemies, hbs, SEnemies, Fatenemy_vel, enemy_vel    
    global score, bullets, lasers, pause, nCs, nukeCharge, endlessMode 
    global last_bullet_time, last_collision_time, last_spawn_time, last_spawn_time2, last_spawn_timeFat, last_spawn_timehb, last_spawn_timeSmoll, last_nuke_time, last_spawn_timenC 

    player_x, player_y = 1000, 500
    player_health = 3
    player_vel = 5
    Fatenemy_vel = 6
    enemy_vel = 3
    hbs = []
    SEnemies = []
    enemies = []
    enemies2 = []
    Fatenemies = []
    bullets = []
    lasers = []
    nCs = []
    score = 0
    last_bullet_time = 0
    last_collision_time = 0
    last_spawn_time = 0
    last_spawn_time2 = 0
    last_spawn_timeFat = 0
    last_spawn_timehb = 0
    last_spawn_timeSmoll = 0
    last_nuke_time = 0
    last_spawn_timenC = 0
    #nukeCharge = 0 #pshhhht
    pause = False
    endlessMode = False
    
# Create a HealthBar class
class HealthBar:
    def __init__(self, max_health, color):
        self.max_health = max_health
        self.current_health = max_health
        self.color = color

    def draw(self, win, x, y, width, height):
        # Calculate the width of the health bar based on current health
        health_width = (self.current_health / self.max_health) * width
        pygame.draw.rect(win, self.color, (x, y, health_width, height))  
    
def spawn_enemy():
    global last_spawn_time
    current_time = time.time()
    if current_time - last_spawn_time >= 0.55:  # Spawn every 0.55 seconds
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, win.get_height() - enemy_height)
        elif side == "right":
            x, y = win.get_width() - enemy_width, random.randint(0, win.get_height() - enemy_height)
        elif side == "top":
            x, y = random.randint(0, win.get_width() - enemy_width), 0
        else:
            x, y = random.randint(0, win.get_width() - enemy_width), win.get_height() - enemy_height
        enemies.append((x, y))
        last_spawn_time = current_time

def move_enemies():
    global enemies
    new_enemies = []
    for x, y in enemies:
        dx, dy = player_x - x, player_y - y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance, dy / distance
        x += dx * enemy_vel
        y += dy * enemy_vel
        new_enemies.append((x, y))
    enemies = new_enemies

# same as spawn_enemy just added a 2 to every 'enemy' and adjustet time between spawns    
def spawn_enemy2():
    global last_spawn_time2
    current_time = time.time()
    if current_time - last_spawn_time2 >= random.randint(1, 2):
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, win.get_height() - enemy2_height)
        elif side == "right":
            x, y = win.get_width() - enemy2_width, random.randint(0, win.get_height() - enemy2_height)
        elif side == "top":
            x, y = random.randint(0, win.get_width() - enemy2_width), 0
        else:
            x, y = random.randint(0, win.get_width() - enemy2_width), win.get_height() - enemy2_height
        enemies2.append((x, y))
        last_spawn_time2 = current_time

# same as move_enemies just adapted the variables
def move_enemies2():
    global enemies2
    new_enemies2 = []
    for x, y in enemies2:
        dx, dy = player_x - x, player_y - y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance, dy / distance
        x += dx * enemy2_vel
        y += dy * enemy2_vel
        new_enemies2.append((x, y))
    enemies2 = new_enemies2

def spawn_Fatenemy():
    global last_spawn_timeFat
    current_time = time.time()
    if current_time - last_spawn_timeFat >= 50:  # Spawn every 50 seconds
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, win.get_height() - Fatenemy_height)
        elif side == "right":
            x, y = win.get_width() - Fatenemy_width, random.randint(0, win.get_height() - Fatenemy_height)
        elif side == "top":
            x, y = random.randint(0, win.get_width() - Fatenemy_width), 0
        else:
            x, y = random.randint(0, win.get_width() - Fatenemy_width), win.get_height() - Fatenemy_height
        Fatenemies.append((x, y))
        last_spawn_timeFat = current_time    

def move_Fatenemies():
    global Fatenemies
    new_Fatenemies = []
    for x, y in Fatenemies:
        dx, dy = player_x - x, player_y - y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance, dy / distance
        x += dx * Fatenemy_vel
        y += dy * Fatenemy_vel
        new_Fatenemies.append((x, y))
    Fatenemies = new_Fatenemies

# spawn health bonus
def spawn_hb():
    global last_spawn_timehb
    current_time = time.time()
    if current_time - last_spawn_timehb >= random.randint(40, 55):  # Spawn between every 40 to 55 seconds
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, win.get_height() - hb_height)
        elif side == "right":
            x, y = win.get_width() - hb_width, random.randint(0, win.get_height() - hb_height)
        elif side == "top":
            x, y = random.randint(0, win.get_width() - hb_width), 0
        else:
            x, y = random.randint(0, win.get_width() - hb_width), win.get_height() - hb_height
        hbs.append((x, y))
        last_spawn_timehb = current_time

def move_hbs():
    global hbs
    new_hbs = []
    for x, y in hbs:
        dx, dy = player_x - x, player_y - y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance, dy / distance
        x += dx * hb_vel
        y += dy * hb_vel
        new_hbs.append((x, y))
    hbs = new_hbs

# spawn nukeCharge
def spawn_nC():
    global last_spawn_timenC
    current_time = time.time()
    if current_time - last_spawn_timenC >= random.randint(45, 75):  # Spawn between every 45 to 75 seconds
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, win.get_height() - nC_height)
        elif side == "right":
            x, y = win.get_width() - nC_width, random.randint(0, win.get_height() - nC_height)
        elif side == "top":
            x, y = random.randint(0, win.get_width() - nC_width), 0
        else:
            x, y = random.randint(0, win.get_width() - nC_width), win.get_height() - nC_height
        nCs.append((x, y))
        last_spawn_timenC = current_time

def move_nCs():
    global nCs
    new_nCs = []
    for x, y in nCs:
        dx, dy = player_x - x, player_y - y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance, dy / distance
        x += dx * nC_vel
        y += dy * nC_vel
        new_nCs.append((x, y))
    nCs = new_nCs
    
def spawn_Senemy():
    global last_spawn_timeSmoll
    current_time = time.time()
    if current_time - last_spawn_timeSmoll >= 10:  # Spawn every 10 seconds
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 0, random.randint(0, win.get_height() - SE_height)
        elif side == "right":
            x, y = win.get_width() - SE_width, random.randint(0, win.get_height() - SE_height)
        elif side == "top":
            x, y = random.randint(0, win.get_width() - SE_width), 0
        else:
            x, y = random.randint(0, win.get_width() - SE_width), win.get_height() - SE_height
        SEnemies.append((x, y))
        last_spawn_timeSmoll = current_time

def move_Senemies():
    global SEnemies
    new_SEnemies = []
    for x, y in SEnemies:
        dx, dy = player_x - x, player_y - y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance, dy / distance
        x += dx * SE_vel
        y += dy * SE_vel
        new_SEnemies.append((x, y))
    SEnemies = new_SEnemies

# Laser variables
laser_width, laser_height = 150, 150
laser_vel = 5.1
lasers = []  # List to store active bullets
last_laser_time = 0  # Time when the last bullet was fired
laserTime = 10
            
# Bullet variables
bullet_width, bullet_height = 10, 10
bullet_vel = 12
bullets = []  # List to store active bullets
last_bullet_time = 0  # Time when the last bullet was fired
bulletTime = 0.14

# Nuke variables
nuke_width, nuke_height = 10000, 10000
nuke_vel = 100
nukes = []
last_nuke_time = 0
nukeTime = 60
nukeCharge = 0

def nuked():
    global enemies, enemies2, SEnemies, Fatenemies, bullets, lasers, score
    
    SEnemies = []
    enemies = []
    enemies2 = []
    Fatenemies = []
    bullets = []
    lasers = []
    score += 15

def spawn_nuke():
    global last_nuke_time
    global nukeCharge
    nx, ny = 0, 0
    nuke_nx, nuke_ny = nuke_vel * nx, nuke_vel * ny 
    nukes.append((0, 0, nuke_nx, nuke_ny))
    nuked()        

def shoot_laser():
    global last_laser_time
    current_time = time.time()
    if current_time - last_laser_time >= laserTime:  # Check if 10 of a seconds have passed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cx, cy = mouse_x - player_x, mouse_y - player_y
        distance = math.sqrt(cx**2 + cy**2)
        laser_cx, laser_cy = laser_vel * cx / distance, laser_vel * cy / distance
        lasers.append((player_x, player_y, laser_cx, laser_cy))
        last_laser_time = current_time

def shoot_bullet():
    global last_bullet_time
    current_time = time.time()
    if current_time - last_bullet_time >= bulletTime:  # Check if 0.14 of a second has passed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - player_x, mouse_y - player_y
        distance = math.sqrt(dx**2 + dy**2)
        bullet_dx, bullet_dy = bullet_vel * dx / distance, bullet_vel * dy / distance
        bullets.append((player_x, player_y, bullet_dx, bullet_dy))
        last_bullet_time = current_time
    
def check_collision():
    global player_health, last_collision_time, enemies, enemies2, hbs, Fatenemies, SEnemies, nCs

    def is_colliding(x, y):
        return abs(player_x - x) < player_width and abs(player_y - y) < player_height

    for x, y in enemies + enemies2:
        if is_colliding(x, y):
            current_time = time.time()
            if current_time - last_collision_time >= 1.2:  # Limit health loss to 1 per 1.2 seconds (basically immunityframes)
                player_health -= 1
                last_collision_time = current_time
                if player_health <= 0:
                    print("Game Over! Your health reached 0.")
                    ctypes.windll.user32.MessageBoxW(0, "Game Over! Your health reached 0 and you dont get ObamaCare.", "Dead as hell", 0)    
                    reset()                
                    #pygame.quit()
    for x, y in Fatenemies + SEnemies:
        if is_colliding(x, y):
            current_time = time.time()
            if current_time - last_collision_time >= 1.2:  # Limit health loss to 1 per 1.2 seconds (basically immunityframes)
                player_health -= 1
                last_collision_time = current_time
                if player_health <= 0:
                    print("Game Over! Your health reached 0.")
                    ctypes.windll.user32.MessageBoxW(0, "Game Over! Your health reached 0 and the medical bill is 5mil.", "Dead as hell", 0)    
                    reset()                
                    #pygame.quit() 
                                                           
# Check laser-enemy collisions
    new_enemies = []
    for x, y in enemies:
        enemy_rect = pygame.Rect(x, y, 30, 30)
        enemy_hit = False  # Flag to track if the enemy is hit
        for cx, cy, _, _ in lasers:
            laser_rect = pygame.Rect(cx, cy, 150, 150 )
            if enemy_rect.colliderect(laser_rect):
                global score
                score += 1
                # Enemy hit by a bullet
                enemy_hit = True
                break  # No need to check other bullets for this enemy
        if not enemy_hit:
            new_enemies.append((x, y))
        
    enemies = new_enemies
            
# Check laser-enemy2 collisions (same as laser-enemy collisions)
    new_enemies2 = []
    for x, y in enemies2:
        enemy2_rect = pygame.Rect(x, y, 37, 37)
        enemy2_hit = False  # Flag to track if the enemy2 is hit
        for cx, cy, _, _ in lasers:
            laser_rect = pygame.Rect(cx, cy, 150, 150)
            if enemy2_rect.colliderect(laser_rect):
                score += 2
                # Enemy2 hit by a bullet
                enemy2_hit = True
                break  # No need to check other bullets for this enemy2
        if not enemy2_hit:
            new_enemies2.append((x, y))
            
    enemies2 = new_enemies2  # Update the enemies2 list

#Fatenemies collision laser
    new_Fatenemies = []
    for x, y in Fatenemies:
        Fatenemy_rect = pygame.Rect(x, y, 70, 70)
        Fatenemy_hit = False  # Flag to track if the enemy is hit
        for cx, cy, _, _ in lasers:
            laser_rect = pygame.Rect(cx, cy, 150, 150 )
            if Fatenemy_rect.colliderect(laser_rect):
                score += 5
                # Enemy hit by a bullet
                Fatenemy_hit = True
                break  # No need to check other bullets for this enemy
        if not Fatenemy_hit:
            new_Fatenemies.append((x, y))
            
    Fatenemies = new_Fatenemies 

#Smollenemy collision laser
    new_SEnemies = []
    for x, y in SEnemies:
        SEnemy_rect = pygame.Rect(x, y, 18, 18)
        SEnemy_hit = False  # Flag to track if the SEnemy is hit
        for cx, cy, _, _ in lasers:
            laser_rect = pygame.Rect(cx, cy, 150, 150 )
            if SEnemy_rect.colliderect(laser_rect):
                score += 8
                # SEnemy hit by a bullet
                SEnemy_hit = True
                break  # No need to check other bullets for this SEnemy
        if not SEnemy_hit:
            new_SEnemies.append((x, y))
            
    SEnemies = new_SEnemies 

# Check laser-healthbonus collisions
    new_hbs = []
    for x, y in hbs:
        hb_rect = pygame.Rect(x, y, hb_width, hb_height)
        hb_hit = False  # Flag to track if the enemy is hit
        for cx, cy, _, _ in lasers:
            laser_rect = pygame.Rect(cx, cy, 150, 150 )
            if hb_rect.colliderect(laser_rect):
                global bonus
                player_health += random.randint(1, 3)
                # hb hit by laser
                hb_hit = True
                break  # No need to check other lasers for this enemy
        if not hb_hit:
            new_hbs.append((x, y))
        
    hbs = new_hbs
    
    # Check laser-nukeCharge collisions
    new_nCs = []
    for x, y in nCs:
        nC_rect = pygame.Rect(x, y, nC_width, nC_height)
        nC_hit = False  
        for cx, cy, _, _ in lasers:
            laser_rect = pygame.Rect(cx, cy, 150, 150 )
            if nC_rect.colliderect(laser_rect):
                global nukeCharge
                nukeCharge += 1
                nC_hit = True
                break  # No need to check other lasers for this enemy
        if not nC_hit:
            new_nCs.append((x, y))
        
    nCs = new_nCs
    
    # Check bullet-enemy collisions
    new_enemies = []
    for x, y in enemies:
        enemy_rect = pygame.Rect(x, y, 30, 30)
        enemy_hit = False  # Flag to track if the enemy is hit
        for bx, by, _, _ in bullets:
            bullet_rect = pygame.Rect(bx, by, 10, 10 )
            if enemy_rect.colliderect(bullet_rect):
                score += 1
                # Enemy hit by a bullet
                enemy_hit = True
                break  # No need to check other bullets for this enemy
        if not enemy_hit:
            new_enemies.append((x, y))

    enemies = new_enemies  # Update the enemies list
    
    # Check bullet-enemy2 collisions (same as bullet-enemy collisions)
    new_enemies2 = []
    for x, y in enemies2:
        enemy2_rect = pygame.Rect(x, y, 37, 37)
        enemy2_hit = False  # Flag to track if the enemy2 is hit
        for bx, by, _, _ in bullets:
            bullet_rect = pygame.Rect(bx, by, 10, 10 )
            if enemy2_rect.colliderect(bullet_rect):
                score += 3
                # Enemy2 hit by a bullet
                enemy2_hit = True
                break  # No need to check other bullets for this enemy
        if not enemy2_hit:
            new_enemies2.append((x, y))

    enemies2 = new_enemies2  # Update the enemies list

    # Check bullet-Smollenemy collisions
    new_SEnemies = []
    for x, y in SEnemies:
        SEnemy_rect = pygame.Rect(x, y, 18, 18)
        SEnemy_hit = False  # Flag to track if the SEnemy is hit
        for bx, by, _, _ in bullets:
            bullet_rect = pygame.Rect(bx, by, 10, 10 )
            if SEnemy_rect.colliderect(bullet_rect):
                score += 8
                #player_health += 1
                # SEnemy hit by a bullet
                SEnemy_hit = True
                break  # No need to check other bullets for this SEnemy
        if not SEnemy_hit:
            new_SEnemies.append((x, y))

    SEnemies = new_SEnemies  # Update the SEnemies list
    
# Check bullet-Fatenemy collisions
    new_Fatenemies = []
    for x, y in Fatenemies:
        Fatenemy_rect = pygame.Rect(x, y, 70, 70)
        Fatenemy_hit = False  # Flag to track if the enemy is hit
        for bx, by, _, _ in bullets:
            bullet_rect = pygame.Rect(bx, by, 10, 10 )
            if Fatenemy_rect.colliderect(bullet_rect):
                score +=7
                # Enemy hit by a bullet
                Fatenemy_hit = True
                break  # No need to check other bullets for this enemy
        if not Fatenemy_hit:
            new_Fatenemies.append((x, y))
            
    Fatenemies = new_Fatenemies  # Update the enemies list

# Check bullet-healthbonus collisions
    new_hbs = []
    for x, y in hbs:
        hb_rect = pygame.Rect(x, y, hb_width, hb_height)
        hb_hit = False  # Flag to track if the hb is hit
        for bx, by, _, _ in bullets:
            bullet_rect = pygame.Rect(bx, by, 10, 10 )
            if hb_rect.colliderect(bullet_rect): 
                player_health += random.randint(1, 3)
                # hb hit by a bullet
                hb_hit = True
                break  # No need to check other bullets for this enemy
        if not hb_hit:
            new_hbs.append((x, y))

    hbs = new_hbs  

# Check bullet-nukeCharge collisions
    new_nCs = []
    for x, y in nCs:
        nC_rect = pygame.Rect(x, y, nC_width, nC_height)
        nC_hit = False  # Flag to track if the hb is hit
        for bx, by, _, _ in bullets:
            bullet_rect = pygame.Rect(bx, by, 10, 10 )
            if nC_rect.colliderect(bullet_rect): 
                nukeCharge += 1
                nC_hit = True
                break  
        if not nC_hit:
            new_nCs.append((x, y))

    nCs = new_nCs 

    # Update 'last_collision_time' when a collision occurs
last_collision_time = pygame.time.get_ticks()

class Player:
    def __init__(self, initial_health=3):
        self.health = initial_health

    def reduce_health(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.game_over()

    def game_over(self):
        print("Game Over! Your health reached 0 and you dont get Obamacare.")
        pygame.quit()
        exit()
            
run = True
last_collision_time = time.time()  # Initialize last collision time
while run:
    pygame.time.delay(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        player_x = max(player_x - player_vel, 0)
    if keys_pressed[pygame.K_d]:
        player_x = min(player_x + player_vel, win.get_width() - player_width)
    if keys_pressed[pygame.K_w]:
        player_y = max(player_y - player_vel, 0)
    if keys_pressed[pygame.K_s]:
        player_y = min(player_y + player_vel, win.get_height() - player_height)
    if keys_pressed[pygame.K_SPACE] or event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
        shoot_bullet()
    # if keys_pressed[pygame.K_ESCAPE]:
    #     break
    if event.type == pygame.MOUSEBUTTONUP and event.button == right:
      #pos = pygame.mouse.get_pos()
      shoot_laser()
    if keys_pressed[pygame.K_ESCAPE] and not pause:
        pause = True
        paused()
    if keys_pressed[pygame.K_ESCAPE] and pause == True: #for whatever reason not working
        pause = False
        unpause()
    if keys_pressed[pygame.K_e] and nukeCharge >= 1:
        current_time = time.time()
        if current_time - timer >= 1:  # Check if at least 1 second has passed
            spawn_nuke()
            nukeCharge -= 1
            timer = current_time  # Update the last spawn time
            
    scaling()
    spawn_enemy()
    move_enemies()
    spawn_enemy2()
    move_enemies2()
    spawn_Fatenemy()
    move_Fatenemies()
    spawn_hb()
    move_hbs()
    spawn_nC()
    move_nCs()
    spawn_Senemy()
    move_Senemies()
    check_collision()
    
    # Update bullet positions
    for i, (bx, by, bdx, bdy) in enumerate(bullets):
        bullets[i] = (bx + bdx, by + bdy, bdx, bdy)
        
    # Update laser positions
    for j, (cx, cy, cdx, cdy) in enumerate(lasers):
        lasers[j] = (cx + cdx, cy + cdy, cdx, cdy)
    
    #for q, (nx, ny, ndx, ndy) in enumerate(nukes):
    #   nukes[q] = (nx + ndx, ny + ndy, ndx, ndy)

    # Draw everything
    win.fill((0, 0, 0)) 
    pygame.draw.rect(win, (255, 0, 0), (player_x, player_y, player_width, player_height))
    win.blit(image2, (player_x, player_y, player_width, player_height))
    for bx, by, _, _ in bullets:
        #pygame.draw.rect(win, (250, 250, 255), (bx, by, bullet_width, bullet_height))
        win.blit(image4, (bx, by, bullet_width, bullet_height))
    for x, y in enemies:
        #pygame.draw.rect(win, (0, 0, 0), (x, y, enemy_width, enemy_height))
        win.blit(image, (x, y, enemy_width, enemy_height))
    for cx, cy, _, _ in lasers:
        #pygame.draw.rect(win, (250, 250, 0), (cx, cy, laser_width, laser_height))
        win.blit(image5, (cx, cy, laser_width, laser_height))
    for x, y in enemies2:
        #pygame.draw.rect(win, (0, 255, 0), (x, y, enemy2_width, enemy2_height))
        win.blit(image3, (x, y, enemy2_width, enemy2_height))
    for x, y in hbs:
        #pygame.draw.rect(win, (255, 0, 0), (x, y, hb_width, hb_height))
        win.blit(image6, (x, y, hb_width, hb_height))
    for x, y in Fatenemies:
        #pygame.draw.rect(win, (255, 255, 255), (x, y, Fatenemy_width, Fatenemy_height))
        win.blit(image7, (x, y, Fatenemy_width, Fatenemy_height))
    for x, y in SEnemies:
        #pygame.draw.rect(win, (255,0,0), (x, y,SE_width, SE_height))
        win.blit(image8, (x, y, SE_width, SE_height))
    for x, y in nCs:
        win.blit(image10, (x, y, nC_width, nC_height))
    #for x, y in bosses:
    #    pygame.draw.rect(win, (255, 255, 255), (x, y, boss_width, boss_height))

    font = pygame.font.Font(None, 50)  # Load the default font, size 50
    font2 = pygame.font.Font(None, 25)
    
    # Display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    win.blit(score_text, (10, 10))  
    # Display Health
    Health_text = font.render(f"Health: {player_health}", True, (255, 30, 30))
    win.blit(Health_text, (205, 10))
    
    INFOtxt = font.render(f"Press Escape to Pause", True, (50, 50, 50))
    win.blit(INFOtxt, (1530, 10))
    
    Nukestxt = font2.render(f"(E)Nukes: {nukeCharge}", True, (200, 200, 200))
    win.blit(Nukestxt, (10, 1050))
    
    #Lasertxt = font2.render(f"Laser: {last_laser_time}", True, (255, 30, 30))
    #win.blit(Lasertxt, (250, 1050))
    
    if endlessMode == False:
        endlstxt = font2.render(f"Endless Mode: Off", True, (200, 200, 200))
        win.blit(endlstxt, (120, 1050))
    if endlessMode == True:
        endlstxt = font2.render(f"Endless Mode: On", True, (200, 200, 200))
        win.blit(endlstxt, (120, 1050))
    
    # endlstxt = font2.render(f"Endless Mode: {endlessMode}", True, (200, 200, 200))
    # win.blit(endlstxt, (120, 1050))
    
    #win.blit(counting_text, counting_rect)
    
    pygame.display.update()
    
pygame.quit()

# Collision bullets with border, bullets get deleted (kinda unnecessary now due to nuke deleting everything, could still be usefull for when the nuke isnt used for a long while)
# Game-Timer displayed on screen
# make an effect for the nuke