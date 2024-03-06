try:
    import Simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class levelOne():

    def draw(self, canvas):
        canvas.draw_text("play", (100,100), 50, 'blue' 'sans-serif')

    def click(self, pos):
        self.click_pos = pos



# this is the level 1 screen of the game to be worked on