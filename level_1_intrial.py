try:
    import Simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

frame = simplegui.create_frame("Level 1", 1000, 700)
frame.set_canvas_background("White")
frame.start()