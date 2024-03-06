try:
    import Simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

frame = simplegui.create_frame("Level one", 1000,700)
frame.set_canvas_background("Black")
frame.start()

# this is the level 1 screen of the game to be worked on