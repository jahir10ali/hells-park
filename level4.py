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

# Platform variables
platform_height = 20
platform_gap = 150
platform_width = 200
platform_positions = [(100, 500), (350, 400), (600, 300), (250, 200)]

exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'

def draw(canvas):
    global exit_btn, block_pos
    canvas.draw_text("THIS IS LEVEL 4", (130, 150), 50, "White", 'monospace')
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)
    # Draw block
    canvas.draw_polygon([(block_pos.x - block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y - block_size / 2),
                         (block_pos.x + block_size / 2, block_pos.y + block_size / 2),
                         (block_pos.x - block_size / 2, block_pos.y + block_size / 2)],
                        1, 'Red', 'Red')
    
    # Draw platforms
    for pos in platform_positions:
        canvas.draw_polygon([(pos[0] - platform_width / 2, pos[1] - platform_height / 2),
                             (pos[0] + platform_width / 2, pos[1] - platform_height / 2),
                             (pos[0] + platform_width / 2, pos[1] + platform_height / 2),
                             (pos[0] - platform_width / 2, pos[1] + platform_height / 2)],
                            1, 'Green', 'Green')

def keydown(key):
    global is_jumping, is_moving_left, is_moving_right
    if key == simplegui.KEY_MAP['left']:
        is_moving_left = True
    elif key == simplegui.KEY_MAP['right']:
        is_moving_right = True
    elif key == simplegui.KEY_MAP['up'] and not is_jumping:
        is_jumping = True

def keyup(key):
    global is_moving_left, is_moving_right
    if key == simplegui.KEY_MAP['left']:
        is_moving_left = False
    elif key == simplegui.KEY_MAP['right']:
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
        for pos in platform_positions:
            if (pos[0] - platform_width / 2 <= block_pos.x <= pos[0] + platform_width / 2 and
                pos[1] - platform_height / 2 <= block_pos.y + block_size / 2 <= pos[1] + platform_height / 2):
                is_jumping = False
                jump_strength = 15
                block_pos.y = pos[1] - platform_height / 2 - block_size / 2
                break

def click(pos, frame):
    global exit_btn
    if exit_btn.is_clicked(pos):
        import levels
        frame.set_draw_handler(levels.draw)
        frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))
        timer.stop()


