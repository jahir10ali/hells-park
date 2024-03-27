'''
This is the menu.py file. This file was created to draw the menu elements
including the title and the buttons. It redirects the player to the level.py or
howtoplay.py screens if its respective buttons are clicked.
'''

from imagesANDbuttons import draw_button, draw_image 
# This import is for drawing buttons and image

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg'  
htp_btn_img = 'https://i.ibb.co/2kCBLmH/htp-btn.jpg'
exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
title_img = 'https://i.ibb.co/PjQb0W9/title.png'
# These are the button image assets


# This is the draw function of the menu, drawing the title and buttons on screen
def draw(canvas):      
    global play_btn, htp_btn, exit_btn
    
    play_btn = draw_button(canvas, play_btn_img, 500, 450, 250, 100)
    htp_btn = draw_button(canvas, htp_btn_img, 150, 450, 250, 100)
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)
    title = draw_button(canvas, title_img, 195, 85, 500, 100)


# This is the click() function that handles mouse clicks on these button images
def click(pos, frame):
    global play_btn, htp_btn
    if play_btn.is_clicked(pos):
        import levels
        frame.set_draw_handler(levels.draw) # This switches the frame to the levels.py content
        frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))
        # This switches the handle of mouse clicks to the levels.py click() function
    elif htp_btn.is_clicked(pos):
        import howtoplay
        frame.set_draw_handler(howtoplay.draw) # This switches the frame to the howtoplay.py content
        frame.set_mouseclick_handler(lambda pos: howtoplay.click(pos, frame))
        # This switches the handle of mouse clicks to the howtoplay.py click() function
    elif exit_btn.is_clicked(pos):
        frame.stop() # This stops the frame, acting as a normal exit button
