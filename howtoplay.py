from imagesANDbuttons import draw_button, draw_image

exit_btn_img = 'images\\exit_btn.jpg'
bg_img =  'images\\background.png'
bg_img = 'images\htp_bg.jpg'

def draw(canvas):
    global exit_btn 
    bg = draw_image(canvas, bg_img, 450, 300, 900, 600)  # This line is supposed to draw the background image
    canvas.draw_text("How to play Hell's Park", (130, 150), 50, "Black", 'monospace')
    canvas.draw_text("just play the game innit", (130, 450), 50, "Black", 'monospace')
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)

def click(pos, frame):
    global exit_btn
    if exit_btn.is_clicked(pos):
        import menu
        frame.set_draw_handler(menu.draw)
        frame.set_mouseclick_handler(lambda pos: menu.click(pos, frame))
