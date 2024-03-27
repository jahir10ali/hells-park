''' 
This is the main.py file. This was created to only instantiate a frame. 
It allows other files to set the frame draw handler to its own draw(canvas) method.
This file sets the draw handlaer to the draw() method in the menu.py file as this is the first screen.
'''

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# These are the canvas dimensions
canvas_width = 900
canvas_height = 600

# This is to create a global frame
frame = simplegui.create_frame('Hells Park', canvas_width, canvas_height, 0)

# This is to make use of the menu draw() function
import menu

# This set the initial draw and mouse click handlers to the ones in the menu.py file
frame.set_draw_handler(menu.draw)
frame.set_mouseclick_handler(lambda pos: menu.click(pos, frame))  

# Start the frame
frame.start()
