from imagesANDbuttons import draw_button

exit_btn_img = 'images\\exit_btn.jpg'
lvl1_btn_img = 'images\\lvl1_btn.jpg'
lvl2_btn_img = 'images\\lvl2_btn.jpg'
lvl3_btn_img = 'images\\lvl3_btn.jpg'
lvl4_btn_img = 'images\\lvl4_btn.jpg'



def draw(canvas):
    global exit_btn, lvl1_btn, lvl2_btn, lvl3_btn, lvl4_btn
    canvas.draw_text("Choose a level", (240, 130), 50, "White", 'monospace')
    exit_btn = draw_button(canvas, exit_btn_img, 750, 20, 125, 50)
    lvl1_btn = draw_button(canvas, lvl1_btn_img, 150, 250, 250, 100)
    lvl2_btn = draw_button(canvas, lvl2_btn_img, 500, 250, 250, 100)
    lvl3_btn = draw_button(canvas, lvl3_btn_img, 150, 450, 250, 100)
    lvl4_btn = draw_button(canvas, lvl4_btn_img, 500, 450, 250, 100)


def click(pos, frame):
    global exit_btn
    if exit_btn.is_clicked(pos):
        import menu
        # Change the draw and mouse click handlers directly from game_test.py
        frame.set_draw_handler(menu.draw)
        frame.set_mouseclick_handler(lambda pos: menu.click(pos, frame))  # Pass frame to click function
    elif lvl1_btn.is_clicked(pos):
        import level1
        frame.set_draw_handler(level1.draw)
        frame.set_keydown_handler(level1.keydown)
        frame.set_keyup_handler(level1.keyup)
        frame.set_mouseclick_handler(lambda pos: level1.click(pos, frame))
    elif lvl2_btn.is_clicked(pos):
        import level2
        frame.set_draw_handler(level2.draw)
        frame.set_keydown_handler(level2.keydown)
        frame.set_keyup_handler(level2.keyup)
        frame.set_mouseclick_handler(lambda pos: level2.click(pos, frame))
    elif lvl3_btn.is_clicked(pos):
        import level3
        frame.set_draw_handler(level3.draw)
        frame.set_keydown_handler(level3.keydown)
        frame.set_keyup_handler(level3.keyup)
        frame.set_mouseclick_handler(lambda pos: level3.click(pos, frame))
    elif lvl4_btn.is_clicked(pos):
        import level4
        frame.set_draw_handler(level4.draw)
        frame.set_keydown_handler(level4.keydown)
        frame.set_keyup_handler(level4.keyup)
        frame.set_mouseclick_handler(lambda pos: level4.click(pos, frame))

