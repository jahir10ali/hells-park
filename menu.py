from imagesANDbuttons import draw_button, draw_image

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


play_btn_img = 'https://i.ibb.co/CscppQV/play-btn.jpg'  
htp_btn_img = 'images/htp_btn.jpg'
exit_btn_img = 'images/exit_btn.jpg'
title_img = 'images/title.jpg'


# Define draw function to load and draw the image
def draw(canvas):      
    global play_btn, htp_btn, exit_btn
    
    play_btn = draw_button(canvas, play_btn_img, 500, 450, 250, 100)
    htp_btn = draw_button(canvas, htp_btn_img, 150, 450, 250, 100)
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)
    title = draw_button(canvas, title_img, 195, 85, 500, 100)
    
    #canvas.draw_text("Welcome to Hell's Park", (140, 150), 50, "White", 'monospace')


def click(pos, frame):  # Add frame as a parameter
    global play_btn, htp_btn
    if play_btn.is_clicked(pos):
        import levels
        # Change the draw and mouse click handlers directly from game_test.py
        frame.set_draw_handler(levels.draw)
        frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))  # Pass frame to click function
    elif htp_btn.is_clicked(pos):
        import howtoplay
        frame.set_draw_handler(howtoplay.draw)
        frame.set_mouseclick_handler(lambda pos: howtoplay.click(pos, frame))
    elif exit_btn.is_clicked(pos):
        frame.stop()
