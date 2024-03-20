try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from imagesANDbuttons import draw_button, draw_image
from vector import Vector

# Global variables
canvas_width = 900
canvas_height = 600
block_size = 50
jump_strength = 15
gravity = 0.8
is_jumping = False
move_speed = 5
is_moving_left = False
is_moving_right = False

# Platform variables
platforms = [
    {"pos": (140, 588), "width": 150, "height": 30},  # Platform 1
    {"pos": (255, 550), "width": 80, "height": 100},  # Platform 3
    {"pos": (600, 300), "width": 200, "height": 20},  # Platform 4
    {"pos": (250, 200), "width": 200, "height": 20},  # Platform 5
    {"pos": (740, 200), "width": 200, "height": 20},  # Platform 6
]

block_pos = Vector(140, 588 - platforms[0]["height"] / 2 - block_size / 2)

exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
lvl2_bg_img = 'https://i.ibb.co/gjTgc9B/lvl2-bg.jpg'


def draw(canvas):
    global exit_btn, block_pos
    lvl2_bg = draw_image(canvas, lvl2_bg_img, 450, 300, 900, 600)
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)
    # Draw block
    canvas.draw_polygon([(block_pos.x - block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y + block_size / 2),
                         (block_pos.x - block_size / 2, block_pos.y + block_size / 2)],
                        1, 'Red', 'Red')
    
    # Draw platforms
    for platform in platforms:
        x, y = platform["pos"]
        width = platform["width"]
        height = platform["height"]
        canvas.draw_polygon([(x - width / 2, y - height / 2),
                             (x + width / 2, y - height / 2),
                             (x + width / 2, y + height / 2),
                             (x - width / 2, y + height / 2)],
                            3, '#92620F', '#C49139')


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

    # Move left if allowed
    if is_moving_left and block_pos.x - block_size / 2 > 0:
        block_pos.x -= move_speed

    # Move right if allowed
    if is_moving_right and block_pos.x + block_size / 2 < canvas_width:
        block_pos.x += move_speed

    # Apply jump
    if is_jumping:
        block_pos.y -= jump_strength
        jump_strength -= gravity  # Apply gravity to decrease jump height

        if block_pos.y >= canvas_height - block_size / 2:
            is_jumping = False
            jump_strength = 15  # Reset jump strength when landing

        # Check for collision with platforms
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

    # Ensure the player stays on the canvas floor
    if block_pos.y + block_size / 2 > canvas_height:
        block_pos.y = canvas_height - block_size / 2

    # Apply gravity when not on a platform
    if not is_on_platform():
        block_pos.y += gravity


def is_on_platform():
    # Check if the player is on any platform
    for platform in platforms:
        x, y = platform["pos"]
        width = platform["width"]
        height = platform["height"]
        if (x - width / 2 <= block_pos.x <= x + width / 2 and
            y - height / 2 <= block_pos.y + block_size / 2 <= y + height / 2):
            return True
    return False

def click(pos, frame):
    global exit_btn, timer
    if exit_btn.is_clicked(pos):
        import levels
        frame.set_draw_handler(levels.draw)
        frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))
        try:
            timer.stop()
        except ValueError:
            pass  # Timer may already be stopped


timer = simplegui.create_timer(1000 // 60, update)
timer.start()