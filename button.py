try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import *
import random


class Button:
    def __init__(self, position, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = simplegui.load_image(image)
        self.image_width = int(width * scale)
        self.image_height = int(height * scale)
        self.position = position
        self.clicked = False

    def draw(self, canvas):
        action = False
        # Get mouse position
        mouse_pos = canvas.mouse_pos

        # Check mouseover and clicked conditions
        if (self.position[0] - self.image_width / 2) <= mouse_pos[0] <= (self.position[0] + self.image_width / 2) and \
           (self.position[1] - self.image_height / 2) <= mouse_pos[1] <= (self.position[1] + self.image_height / 2):
            if canvas.mouse_down:
                self.clicked = True
                action = True

        if not canvas.mouse_down:
            self.clicked = False

        # Draw button on screen
        canvas.draw_image(self.image, (self.image.get_width() / 2, self.image.get_height() / 2),
                          (self.image.get_width(), self.image.get_height()),
                          self.position, (self.image_width, self.image_height))

        return action



'''
# Example usage:
def play_game():
    print("Play Game button clicked!")

def how_to_play():
    print("How to Play button clicked!")

frame = simplegui.create_frame("Buttons Example", 400, 300)

play_button = Button((100, 100), "https://image-url.com/play_button.png", 0.5)
how_to_play_button = Button((300, 100), "https://image-url.com/how_to_play_button.png", 0.5)

def draw(canvas):
    play_button.draw(canvas)
    how_to_play_button.draw(canvas)

def mouse_handler(pos):
    if play_button.draw(pos):
        play_game()
    elif how_to_play_button.draw(pos):
        how_to_play()

frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)

frame.start()
'''
