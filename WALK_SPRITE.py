from vector import Vector

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



URL = r'C:\Users\mokta\OneDrive\Desktop\cs\spitesheet\Girl-Sheet.png'
WIDTH = 1056
HEIGHT = 24
Column = 44
Rows = 1


class Spritesheet_walking():
    
    def __init__(self, imgurl, width, height, column, rows):
        self.imgurl = imgurl
        self.width = width
        self.height = height
        self.column = column 
        self.rows = rows
        
        
        
        self._intit_dimension()
        
        self.frame_index = [43, 0]
        
    #dimensions of the frame
    def _intit_dimension(self):
        self.frame_width = self.width / self.column
        self.frame_height = self.height / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        
    


        
    
    def draw(self, canvas):
        
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )
        
        source_size = (self.frame_width, self.frame_height)
        
        dest_centre = (300, 150)
        dest_size = (200, 200)
        
        img = simplegui.load_image(self.imgurl)
        
        canvas.draw_image(img, source_centre, source_size, dest_centre,
                         dest_size)
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.column
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows
        
   
        
        
class Clock():
    
    def __init__(self):
        self.time = 0
        
    
    def tick(self):
        self.time += 1
        
    def transition(self, frame_duration):
        return self.time % frame_duration == 0
    
    
    
def draw(canvas):
    sheet.draw(canvas)
    
    clock.tick()
    if clock.transition(1):
        sheet.next_frame()
        
        
        
        
clock = Clock()        
sheet = Spritesheet_walking(URL, WIDTH, HEIGHT, Column, Rows)        

        
frame = simplegui.create_frame('Spritesheet', 600, 300)
frame.set_draw_handler(draw)

frame.start()
        