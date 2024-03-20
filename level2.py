try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from imagesANDbuttons import draw_button, draw_image
from vector import Vector

canvas_width = 900
canvas_height = 600
block_size = 50
jump_strength = 15
gravity = 0.8
is_jumping = False
move_speed = 5
is_moving_left = False
is_moving_right = False

platforms = [
    {"pos": (70, 588), "width": 130, "height": 30},
    {"pos": (165, 550), "width": 80, "height": 100},
    {"pos": (320, 440), "width": 150, "height": 30},
    {"pos": (520, 550), "width": 80, "height": 200},
    {"pos": (670, 380), "width": 150, "height": 30},
    {"pos": (840, 550), "width": 80, "height": 450},
    {"pos": (670, 200), "width": 150, "height": 30},
    {"pos": (455, 200), "width": 80, "height": 100},
    {"pos": (140, 150), "width": 260, "height": 30},
]

block_pos = Vector(70, 588 - platforms[0]["height"] / 2 - block_size / 2)

exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg'  
lvl2_bg_img = 'https://i.ibb.co/gjTgc9B/lvl2-bg.jpg'
reset_btn_img = 'https://i.ibb.co/p08zvqP/reset-btn.jpg'
pause_btn_img = 'https://i.ibb.co/LkHqxxz/pause-btn.jpg'
paused_screen_img = 'https://i.ibb.co/ZdXM7LN/paused-screen.png'


def draw(canvas):
    global exit_btn, reset_btn, pause_btn, block_pos
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

def draw_pause(canvas):
    global play_btn, exit_btn, reset_btn, pause_btn, block_pos, paused_screen
    paused_screen = draw_image(canvas, paused_screen_img, 450, 300, 900, 600)
    play_btn = draw_button(canvas, play_btn_img, 500, 450, 250, 100)
    exit_btn = draw_button(canvas, exit_btn_img, 150, 450, 250, 100)



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
    global block_pos, is_jumping, jump_strength, gravity

    if is_moving_left and block_pos.x - block_size / 2 > 0:
        block_pos.x -= move_speed

    if is_moving_right and block_pos.x + block_size / 2 < canvas_width:
        block_pos.x += move_speed

    if is_jumping:
        block_pos.y -= jump_strength
        jump_strength -= gravity  

        if block_pos.y >= canvas_height - block_size / 2:
            is_jumping = False
            jump_strength = 15  

        for platform in platforms:
            x, y = platform["pos"]
            width = platform["width"]
            height = platform["height"]
            if (x - width / 2 <= block_pos.x <= x + width / 2 and
                y - height / 2 <= block_pos.y + block_size / 2 <= y + height / 2):
                is_jumping = False
                jump_strength = 15
                block_pos.y = y - height / 2 - block_size / 2
                break

    if block_pos.y + block_size / 2 > canvas_height:
        block_pos.y = canvas_height - block_size / 2

    if not is_on_platform():
        block_pos.y += gravity


def is_on_platform():
    for platform in platforms:
        x, y = platform["pos"]
        width = platform["width"]
        height = platform["height"]
        if (x - width / 2 <= block_pos.x <= x + width / 2 and
            y - height / 2 <= block_pos.y + block_size / 2 <= y + height / 2):
            return True
    return False


def click(pos, frame):
    global play_btn, exit_btn, reset_btn, pause_btn, timer, block_pos
    if pause_btn.is_clicked(pos):
        frame.set_draw_handler(draw_pause)
    elif reset_btn.is_clicked(pos):
        block_pos = Vector(70, 588 - platforms[0]["height"] / 2 - block_size / 2)
    elif exit_btn.is_clicked(pos):
        timer.stop()
        import levels
        frame.set_draw_handler(levels.draw)
        frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))
    elif play_btn.is_clicked(pos):
        frame.set_draw_handler(draw)


timer = simplegui.create_timer(1000 // 60, update)
timer.start()

           
