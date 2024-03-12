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
block_pos = Vector(canvas_width / 2, canvas_height - block_size / 2)  # Starting position at the bottom center
jump_strength = 15
gravity = 0.8
is_jumping = False
move_speed = 5
is_moving_left = False
is_moving_right = False

exit_btn_img = 'images\\exit_btn.jpg'

def draw(canvas):
    global exit_btn, block_pos
    canvas.draw_text("THIS IS LEVEL 1", (130, 150), 50, "White", 'monospace')
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)
    canvas.draw_polygon([(block_pos.x - block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y + block_size / 2),
                         (block_pos.x - block_size / 2, block_pos.y + block_size / 2)],
                        1, 'Red', 'Red')

def keydown(key):
    global is_jumping, is_moving_left, is_moving_right
    if key == simplegui.KEY_MAP['left']:
        is_moving_left = True
    elif key == simplegui.KEY_MAP['right']:
        is_moving_right = True
    elif key == simplegui.KEY_MAP['up'] and not is_jumping:
        jump()

def keyup(key):
    global is_moving_left, is_moving_right
    if key == simplegui.KEY_MAP['left']:
        is_moving_left = False
    elif key == simplegui.KEY_MAP['right']:
        is_moving_right = False

def jump():
    global is_jumping, jump_strength
    is_jumping = True
    jump_strength = 15  # Reset jump strength when jumping

def update():
    global block_pos, is_jumping, is_moving_left, is_moving_right, jump_strength

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

def click(pos, frame):
    global exit_btn
    if exit_btn.is_clicked(pos):
        import levels
        frame.set_draw_handler(levels.draw)
        frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))
        timer.stop()

timer = simplegui.create_timer(1000 // 60, update)
timer.start()
