try:
    import Simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

name = "Water Boy"

class screen():

    def __init__(self, title, start):
        self.title = title
        self.start = start 
    
    def draw(self, canvas):
        
        canvas.draw_text(self.title, (300, 200), 100, 'Blue', 'serif' )
        canvas.draw_text(self.start, (450,400), 50, 'Blue', 'serif')

def click_start():
    frame.set_canvas_background("blue")
    



def click_menu():
    frame.set_canvas_background("black")
    

    




opening_screen = screen(name, "Start")

frame = simplegui.create_frame("Welcome Screen", 1000, 700)
frame.set_canvas_background("white")





frame.add_button("Start", click_start)
frame.add_button("Menu", click_menu)


frame.set_draw_handler(opening_screen.draw)
frame.start()

# this is the menu screen of the game to be worked on