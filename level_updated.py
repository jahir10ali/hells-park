try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from imagesANDbuttons import draw_button, draw_image
from vector import Vector

# Constants
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 30
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  # Y-coordinate of the floor


class Platform:
    def __init__(self, position, width, height):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.edge_l = self.x  # Left edge of the platform
        self.edge_r = self.x + self.width  # Right edge of the platform
        self.edge_b = self.y + self.height  # Bottom edge of the platform
        self.edge_t = self.y  # Top edge of the platform

    def draw(self, canvas):
        canvas.draw_polygon([(self.x, self.y),
                             (self.x + self.width, self.y),
                             (self.x + self.width, self.y + self.height),
                             (self.x, self.y + self.height)],
                            3, 'White', 'Blue')

    def hit(self, player):
        return player.offset_l() <= self.edge_r and player.offset_r() >= self.edge_l \
            and player.offset_t() <= self.edge_b and player.offset_b() >= self.edge_t


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel = Vector(0, 0)
        self.on_ground = True
        self.moving_left = False
        self.moving_right = False

    def draw(self, canvas):
        canvas.draw_polygon([(self.pos.x - PLAYER_SIZE / 2, self.pos.y - PLAYER_SIZE / 2),
                             (self.pos.x + PLAYER_SIZE / 2, self.pos.y - PLAYER_SIZE / 2),
                             (self.pos.x + PLAYER_SIZE / 2, self.pos.y + PLAYER_SIZE / 2),
                             (self.pos.x - PLAYER_SIZE / 2, self.pos.y + PLAYER_SIZE / 2)],
                            1, "Red", "Red")

    def update(self, platforms):
        self.vel += GRAVITY
        # Adjust velocity based on movement direction
        if self.moving_left:
            self.vel.x = -5
        elif self.moving_right:
            self.vel.x = 5
        else:
            self.vel.x = 0
            
        self.pos += self.vel
        
        # Check if player hits the floor
        if self.pos.y >= FLOOR_Y:
            self.pos.y = FLOOR_Y
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Ensure player stays within canvas bounds
        # n/a
        
        # Check if player hits the right edge of the screen
        if self.pos.x > CANVAS_WIDTH and i.current_screen == 1:
            i.switch_screen()
            self.pos.x = 0  # Reset player position to start of the next screen
        elif self.pos.x > CANVAS_WIDTH and i.current_screen == 2:
            self.pos.x = CANVAS_WIDTH 

        # Check if player hits the left edge of the screen
        if self.pos.x < 0 and i.current_screen == 1:
            self.pos.x = 0
        elif self.pos.x < 0 and i.current_screen == 2:
            i.switch_screen()
            self.pos.x = CANVAS_WIDTH  # Reset player position to end of the previous screen


        # Check for collisions with platforms
        for platform in platforms:
            # Collision with left side of the platform
            if self.vel.x > 0 and self.pos.x + self.width / 2 >= platform.edge_l and \
                self.pos.x - self.width / 2 < platform.edge_l and \
                self.pos.y + self.height / 2 > platform.y and \
                self.pos.y - self.height / 2 < platform.y + platform.height:
                self.pos.x = platform.edge_l - self.width / 2
            # Collision with right side of the platform
            elif self.vel.x < 0 and self.pos.x - self.width / 2 <= platform.edge_r and \
                    self.pos.x + self.width / 2 > platform.edge_r and \
                    self.pos.y + self.height / 2 > platform.y and \
                    self.pos.y - self.height / 2 < platform.y + platform.height:
                self.pos.x = platform.edge_r + self.width / 2
            # Collision with bottom of the platform
            if self.pos.y - self.height / 2 < platform.edge_b and \
                self.pos.y + self.vel.y - self.height / 2 > platform.y and \
                self.pos.x + self.width / 2 > platform.edge_l and \
                self.pos.x - self.width / 2 < platform.edge_r:
                    # Collision with bottom of the platform
                    self.pos.y = platform.edge_b + self.height / 2  # Move player to just above the platform's bottom edge
                    self.vel.y = 0  # Stop vertical movement
                    self.on_ground = True  # Set player on ground after collision
            # Collision with top of the platform
            elif self.vel.y > 0 and self.pos.y - self.height / 2 <= platform.edge_t and \
                    self.pos.y + self.height / 2 > platform.edge_t and \
                    self.pos.x + self.width / 2 > platform.edge_l and \
                    self.pos.x - self.width / 2 < platform.edge_r:
                self.pos.y = platform.edge_t - self.height / 2
                self.vel.y = 0
                self.on_ground = True
                # Additional condition to prevent interference with left/right edge collision
                if (self.pos.x + self.width / 2 > platform.edge_l and \
                    self.pos.x - self.width / 2 < platform.edge_r):
                    self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel.y = -7  # Adjust jump strength as needed

    def start_move_left(self):
        self.moving_left = True

    def stop_move_left(self):
        self.moving_left = False

    def start_move_right(self):
        self.moving_right = True

    def stop_move_right(self):
        self.moving_right = False

        
        
        
frame = simplegui.create_frame("Block Wall", CANVAS_WIDTH, CANVAS_HEIGHT, 0)           
       

class Interaction:
    def __init__(self, platformsONE, platformsTWO, player):
        self.player = player
        self.platformsONE = platformsONE
        self.platformsTWO = platformsTWO
        self.current_screen = 1  # Initially set to Screen ONE

    def update(self):
        if self.current_screen == 1:
            self.player.update(self.platformsONE)
        elif self.current_screen == 2:
            self.player.update(self.platformsTWO)

    def draw(self, canvas):
        self.update()
        self.player.draw(canvas)
        if self.current_screen == 1:
            for platform in self.platformsONE:
                platform.draw(canvas)
        elif self.current_screen == 2:
            for platform in self.platformsTWO:
                platform.draw(canvas)

    def switch_screen(self):
        if self.current_screen == 1:
            self.current_screen = 2
        elif self.current_screen == 2:
            self.current_screen = 1



platformsONE = [
    Platform((2, 563), 250, 35),
    Platform((350, 470), 50, 50),
    Platform((500, 563), 200, 35),
    Platform((220, 380), 50, 50),
    Platform((0, 295), 170, 35),
    Platform((320, 295), 170, 35),
    Platform((120, 210), 50, 40),
    Platform((200, 130), 170, 35),
    Platform((760, 295), 20, 20),
    Platform((500, 70), 170, 35),
    Platform((675, 1), 35, 104),
    Platform((500, -37), 170, 35),
    Platform((55, 55), 20, 20),
]

platformsTWO = [
    Platform((165, 350), 130, 30),
    Platform((405, 420), 40, 40),
    Platform((790, 548), 20, 50),
    Platform((850, 508), 50, 20),
    Platform((790, 418), 50, 20),
    Platform((380, 260), 130, 30),
    Platform((850, 350), 50, 20),
    Platform((770, 270), 70, 20),
    Platform((270, 168), 130, 30),
    Platform((30, 90), 200, 30),
    Platform((7, 1), 20, 120),
    Platform((30, -32), 200, 30),
    Platform((560, 90), 315, 30),
    Platform((878, 1), 20, 120),
    Platform((560, -32), 315, 30),
]

block_pos = Vector(platformsONE[0].width / 2, 500)

player = Player(block_pos)

i = Interaction(platformsONE, platformsTWO, player)

# Define key handlers
def keydown(key):
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["up"]:
        player.jump()
    elif key == simplegui.KEY_MAP["a"] or key == simplegui.KEY_MAP["left"]:
        player.start_move_left()
    elif key == simplegui.KEY_MAP["d"] or key == simplegui.KEY_MAP["right"]:
        player.start_move_right()


def keyup(key):
    if key == simplegui.KEY_MAP["a"] or key == simplegui.KEY_MAP["left"]:
        player.stop_move_left()
    elif key == simplegui.KEY_MAP["d"] or key == simplegui.KEY_MAP["right"]:
        player.stop_move_right()

# Set the draw handler to i.drawONE initially
frame.set_draw_handler(i.draw)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()
          
