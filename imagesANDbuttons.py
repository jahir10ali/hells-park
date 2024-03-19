try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Button:
    def __init__(self, image_path, pos_x, pos_y, width, height):
        self.image = simplegui.load_image(image_path)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def draw(self, canvas):
        canvas.draw_image(self.image, (self.image.get_width()/2, self.image.get_height()/2), 
                          (self.image.get_width(), self.image.get_height()), 
                          (self.pos_x + self.width/2, self.pos_y + self.height/2), 
                          (self.width, self.height))
        
    def is_clicked(self, pos):
        return (self.pos_x < pos[0] < self.pos_x + self.width) and (self.pos_y < pos[1] < self.pos_y + self.height)

def draw_button(canvas, imagePath, pos_x, pos_y, width, height):
    button = Button(imagePath, pos_x, pos_y, width, height)
    button.draw(canvas)
    return button


def draw_image(canvas, imagePath, pos_x, pos_y, width, height):
    image = simplegui.load_image(imagePath)

    canvas.draw_image(image, (image.get_width()/2, image.get_height()/2), 
                      (image.get_width(), image.get_height()), (pos_x, pos_y), 
                      (width, height))
