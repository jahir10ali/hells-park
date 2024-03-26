try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from imagesANDbuttons import draw_button, draw_image
from vector import Vector

canvas_width = 900
canvas_height = 600
block_size = 50
jump_strength = 26
gravity = 9.81
is_jumping = False
move_speed = 5
monster_move_speed = 5
is_moving_left = False
is_moving_right = False



platforms = [
    {"pos": (300, 578), "width": 130, "height": 30},
    {"pos": (400, 520), "width": 140, "height": 30},
    {"pos": (670, 570), "width": 300, "height": 30},
    {"pos": (860, 470), "width": 50, "height": 30},
    {"pos": (788,365), "width": 50, "height": 30},
    {"pos": (347,295), "width": 650, "height": 30},
    {"pos": (63,190), "width": 50, "height": 30}
 
]

monsters = [
    {"pos": (150, 566), "radius": 25, "moving_left": True, "moving_right" : False, "width": 100, "original_x": 150},
    {"pos": (450, 480), "radius": 25, "moving_left": True, "moving_right": False, "width": 100, "original_x": 430},
    {"pos": (540, 519), "radius": 25, "moving_left": True, "moving_right": False, "width": 100, "original_x": 540}
    


]

up_down_monsters = [
    {"pos": (660,450), "radius": 25, "moving_down": True, "moving_up": False, "width": 100, "original_y": 450, "speed": 5},
    {"pos": (735,370), "radius": 25, "moving_down": True, "moving_up": False, "width": 180, "original_y": 450, "speed": 3},
    {"pos": (576, 170), "radius": 25, "moving_down": True, "moving_up": False, "width": 180, "original_y": 170, "speed": 3},
    {"pos": (453, 170), "radius": 25, "moving_down": True, "moving_up": False, "width": 180, "original_y": 170, "speed": 5},
    {"pos": (330, 170), "radius": 25, "moving_down": True, "moving_up": False, "width": 180, "original_y": 170, "speed": 7},
    {"pos": (255, 90), "radius": 25, "moving_down": True, "moving_up": False, "width": 100, "original_y": 170, "speed": 3}
    

]

block_pos = Vector(30, 588 - platforms[0]["height"] / 2 - block_size / 2)

exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg'  
lvl2_bg_img = 'https://i.ibb.co/gjTgc9B/lvl2-bg.jpg'
reset_btn_img = 'https://i.ibb.co/p08zvqP/reset-btn.jpg'
pause_btn_img = 'https://i.ibb.co/LkHqxxz/pause-btn.jpg'
paused_screen_img = 'https://i.ibb.co/ZdXM7LN/paused-screen.png'


def draw(canvas):
    global reset_btn, pause_btn, block_pos
    lvl2_bg = draw_image(canvas, lvl2_bg_img, 450, 300, 900, 600)
    reset_btn = draw_button(canvas, reset_btn_img, 830, 20, 50, 50)
    pause_btn = draw_button(canvas, pause_btn_img, 760, 20, 50, 50)
    canvas.draw_polygon([(block_pos.x - block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y + block_size / 2),
                         (block_pos.x - block_size / 2, block_pos.y + block_size / 2)],
                        1, 'Red', 'Red')
    
    for platform in platforms:
        x, y = platform["pos"]
        width = platform["width"]
        height = platform["height"]
        canvas.draw_polygon([(x - width / 2, y - height / 2),
                             (x + width / 2, y - height / 2),
                             (x + width / 2, y + height / 2),
                             (x - width / 2, y + height / 2)],
                            3, '#92620F', '#C49139')
    
    for monster in monsters:
        x,y = monster["pos"]
        radius = monster["radius"]
        canvas.draw_circle((x,y), radius, 1, 'white' )

    for monster in up_down_monsters:
        x,y = monster["pos"]
        radius = monster["radius"]
        canvas.draw_circle((x,y), radius, 1, 'white')

    



def draw_pause(canvas):
    global play_btn, reset_btn, pause_btn, block_pos, paused_screen
    paused_screen = draw_image(canvas, paused_screen_img, 450, 300, 900, 600)
    play_btn = draw_button(canvas, play_btn_img, 500, 450, 250, 100)
    



def keydown(key):
    global is_jumping, is_moving_left, is_moving_right
    if key == simplegui.KEY_MAP['left']:
        is_moving_left = True
    elif key == simplegui.KEY_MAP['a']:
        is_moving_left = True
    elif key == simplegui.KEY_MAP['right']:
        is_moving_right = True
    elif key == simplegui.KEY_MAP['d']:
        is_moving_right = True
    elif key == simplegui.KEY_MAP['up'] and not is_jumping:
        is_jumping = True
    elif key == simplegui.KEY_MAP['w'] and not is_jumping:
        is_jumping = True


def keyup(key):
    global is_moving_left, is_moving_right
    if key == simplegui.KEY_MAP['left']:
        is_moving_left = False
    if key == simplegui.KEY_MAP['a']:
        is_moving_left = False
    elif key == simplegui.KEY_MAP['right']:
        is_moving_right = False
    elif key == simplegui.KEY_MAP['d']:
        is_moving_right = False



def update():
    global block_pos, is_jumping, jump_strength, gravity, monster_move_speed

    if is_moving_left and block_pos.x - block_size / 2 > 0:
        block_pos.x -= move_speed

    if is_moving_right and block_pos.x + block_size / 2 < canvas_width:
        block_pos.x += move_speed

    for monster in monsters:
        x,y = monster["pos"]
        
        moving_left = monster["moving_left"]
        moving_right = monster["moving_right"]
        width = monster["width"]

        

        if moving_left:
            x -= move_speed
            if x <= monster["original_x"] - width/2:
                monster["moving_left"] = False
                monster["moving_right"] = True

        if moving_right:
            x += monster_move_speed
            if x >= monster["original_x"] + width/2:
                monster["moving_right"] = False
                monster["moving_left"] = True
        
        monster["pos"] = (x, y)

        if is_on_monster():
            monster["pos"] = (-300, 800)

        if should_die():
            block_pos = Vector(30, 588 - platforms[0]["height"] / 2 - block_size / 2)

    for monster in up_down_monsters:
        x,y = monster["pos"]
        moving_down = monster["moving_down"]
        moving_up = monster["moving_up"]
        width = monster["width"]


        if moving_down:
            y += monster["speed"]
            if y >= monster["original_y"] + width/2:
                monster["moving_down"] = False
                monster["moving_up"] = True

        if moving_up:
            y -= monster["speed"]
            if y <= monster["original_y"] - width/2:
                monster["moving_up"] = False
                monster["moving_down"] = True
    
        monster["pos"] = (x, y)
        
        

        if should_die_up_down():
            block_pos = Vector(30, 588 - platforms[0]["height"] / 2 - block_size / 2) 
                         

    if is_jumping:
        block_pos.y -= jump_strength
        jump_strength -= 0.8  

        if block_pos.y >= canvas_height - block_size / 2:
            is_jumping = False
            jump_strength = 24

        for platform in platforms:
            x, y = platform["pos"]
            width = platform["width"]
            height = platform["height"]


            if (x - width / 2 <= block_pos.x  <= x + width / 2 and
                y - height / 2 <= block_pos.y  + block_size / 2 <= y + height / 2):
                is_jumping = False
                jump_strength = 18
                block_pos.y = y - height / 2 - block_size / 2
                break
            
                

    if block_pos.y + block_size / 2 > canvas_height:
        block_pos.y = canvas_height-1 - block_size / 2

    if not is_on_platform():
        block_pos.y += gravity
        
    else:
        jump_strength = 24

    

    
    
    
    
    




def is_on_platform():
    for platform in platforms:
        x, y = platform["pos"]
        width = platform["width"]
        height = platform["height"]
        if (x - width / 2 <= block_pos.x <= x + width / 2 and
            y - height / 2 <= block_pos.y + block_size / 2 <= y + height / 2):
            return True
    return False


def is_on_monster():
    for monster in monsters:
        x,y = monster["pos"]
        radius = monster["radius"]
        if (x - radius <= block_pos.x <= x + radius and 
             y - radius <= block_pos.y <= y + radius):
            return True            
    return False


def is_on_up_down_monster():
    for monster in up_down_monsters:
        x,y = monster["pos"]
        radius = monster["radius"]
        if (x - radius <= block_pos.x <= x + radius and 
             y - radius <= block_pos.y <= y + radius):
            return True            
    return False

def should_die():
    for monster in monsters:
        x,y = monster["pos"]
        radius = monster["radius"]
        if ( x - radius <= block_pos.x + block_size/2 and block_pos.x - block_size/2 <= x + radius and
            y - radius <= block_pos.y - block_size/2):
            return True
    return False


def should_die_up_down():
    for monster in up_down_monsters:
        x,y = monster["pos"]
        radius = monster["radius"]
        if ( x - radius <= block_pos.x + block_size/2 and block_pos.x - block_size/2 <= x + radius and
            y - radius <= block_pos.y + block_size/2 and block_pos.y - block_size/2 <= y + radius):
            return True
    return False


def click(pos):
    if reset_btn.is_clicked(pos):
        block_pos = Vector(70, 588 - platforms[0]["height"] / 2 - block_size / 2)
    


timer = simplegui.create_timer(1000 // 60, update)
timer.start()

           
frame = simplegui.create_frame('Hells Park', canvas_width, canvas_height, 0)

# Set the initial draw and mouse click handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)  # Pass frame to click function

# Start the frame
frame.start()