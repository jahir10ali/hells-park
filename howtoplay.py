'''
This is the howtoplay.py file. This file outputs an image containing the instructions
and insights of the game and has an exit button to go back to the menu (menu.py)
'''

from imagesANDbuttons import draw_button, draw_image
# This import is for drawing buttons and images

exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
bg_img = 'https://i.ibb.co/VtLj2ZZ/htp-bg.jpg'
# These are the (button) image assets

# This is the draw function of the how to play screen 
# This draws the image of the instructions and the exit button on screen
def draw(canvas):
    global exit_btn 
    bg = draw_image(canvas, bg_img, 450, 300, 900, 600)  
    # This line draws the background image
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)

# This is the click() function that handles mouse clicks on these button images
def click(pos, frame):
    global exit_btn
    if exit_btn.is_clicked(pos):
        import menu
        frame.set_draw_handler(menu.draw) # This switches the frame to the menu.py content
        frame.set_mouseclick_handler(lambda pos: menu.click(pos, frame))
        # This switches the handle of mouse clicks to the menu.py click() function
