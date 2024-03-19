# Imports go at the top
from microbit import *
import random
import audio
import music

def handle_move_ship ():
    global ship_loc
    if button_a.was_pressed():
        if ship_loc >0 :
            display.set_pixel(ship_loc, 4, 0)
            ship_loc -= 1
            display.set_pixel(ship_loc,4,9)
            music.pitch(1200)
            sleep(5)
            music.stop()
        else:
            ship_loc=0
    elif button_b.was_pressed():
        if ship_loc <4 :
            display.set_pixel(ship_loc, 4, 0)
            ship_loc += 1
            display.set_pixel(ship_loc,4,9)
            music.pitch(1200)
            sleep(5)
            music.stop()
        else:
            ship_loc=4
    
def update_game(enemies):
    global score
    for enemy in enemies:
        if enemy['y'] == 4:
            # game over! 
            display.set_pixel(enemy['x'],enemy['y'],0)

            display.clear()
            music.play(music.POWER_DOWN)
            display.show("GAME OVER" + str(score))
            return True
        else:  
            if enemy['y'] > -1:
                display.set_pixel(enemy['x'],enemy['y'],0)
            enemy['y'] +=1
            display.set_pixel(enemy['x'],enemy['y'],6)
    return False

def create_enemy ():
    global enemies
    loc_x = random.randrange(0, 4)
    enemies.append({
        'x' : loc_x,
        'y' : -1
    })

def init_game():
    global enemy_max_time_repeater
    display.clear()
    audio.play(Sound.TWINKLE)
    ship_loc = 2
    enemy_max_time_repeater = 18000
    enemies.clear()
    rockets.clear()
    display.set_pixel(ship_loc,4,9)
    

def create_rocket():
    global rockets
    # can't launch rocket if you just launched one
    for rocket in rockets:
        if rocket['y'] == 3:
            return None

    rockets.append({
        'x' : ship_loc,
        'y' : 3
    })
    display.set_pixel(ship_loc,3,4)
    


def handle_launch_rocket():
    if accelerometer.was_gesture('shake'):
        music.pitch(900)
        sleep(5)
        music.pitch(600)
        sleep(5)

        music.stop()
        create_rocket()

        
        
def detect_collision(x, y):
    global enemies, rockets, score
    remove = None
    for enemy in enemies:
        if enemy['x'] == x and enemy['y'] == y:
            display.set_pixel(x,y,5)
            display.set_pixel(x,y,6)
            display.set_pixel(x,y,7)
            display.set_pixel(x,y,8)
            display.set_pixel(x,y,9)
            display.set_pixel(x,y,0)
            display.set_pixel(x,y,9)
            display.set_pixel(x,y,0)
            display.set_pixel(x,y,9)
            music.play(music.POWER_UP)
            display.set_pixel(x,y,0)
            remove = enemy
    if remove:
        score +=1
        enemies.remove(remove)
        rockets.remove(remove)

            

    
def move_rocket():
    global rockets
    remove_last = False
    for rocket in rockets:
        display.set_pixel(rocket['x'],rocket['y'],0)
        rocket['y'] -=1
        if rocket['y'] < 0:
            remove_last = True
        else:
            display.set_pixel(rocket['x'],rocket['y'],4)
            detect_collision(rocket['x'],rocket['y'])

    
    if remove_last:
        rockets.pop(0)


# game variables
ship_loc = 2
enemy_time_counter = 0
enemy_max_time_repeater = 18000
enemies = []
enemy_skip = True

rocket_time_counter = 0
rocket_time_repeater = 4000

rockets = []
score = 0
init_game()

# Code in a 'while True:' loop repeats forever
while True:

    handle_move_ship()
    handle_launch_rocket()
    if rocket_time_counter == rocket_time_repeater:
        move_rocket()
        rocket_time_counter = 0
    rocket_time_counter +=1
    
    if enemy_time_counter == enemy_max_time_repeater:
        if enemy_skip:
            music.play(['a:1'])
            enemy_skip = False
        else:
            create_enemy()
            music.play(['ab:1'])
            enemy_skip = True
        enemy_time_counter = 0
        enemy_max_time_repeater -=500

        game_over = update_game(enemies)
        if game_over:
            while True:
                if accelerometer.was_gesture('shake'):
                    game_over = False
                    init_game()
                    break

    enemy_time_counter+=1
    

    

    
