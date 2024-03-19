try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Define canvas dimensions
canvas_width = 900
canvas_height = 600

# Create a global frame
frame = simplegui.create_frame('Hells Park', canvas_width, canvas_height, 0)

# Import other modules
import menu

# Set the initial draw and mouse click handlers
frame.set_draw_handler(menu.draw)
frame.set_mouseclick_handler(lambda pos: menu.click(pos, frame))  # Pass frame to click function

# Start the frame
frame.start()
