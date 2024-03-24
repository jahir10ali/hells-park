import simplegui
from user305_o32FtUyCKk_0 import Vector

# Constants
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 30
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  # Y-coordinate of the floor


class Trap:
    def __init__(self, spikes_quantity, position, width, height):
        self.spikes = []
        self.width = width
        self.height = height
        self.edge_l = position[0] - width / 2  # Left edge of the trap
        self.edge_r = position[0] + (width / 2 * spikes_quantity)  # Right edge of the trap
        self.edge_b = position[1]  # Bottom edge of the trap
        self.edge_t = position[1] - height  # Top edge of the trap
        
        # Calculate spike positions
        for i in range(spikes_quantity):
            spike_x = position[0] - width / 2 + i * width / 2
            spike_y = position[1]
            spike = [(spike_x, spike_y), (spike_x + width / 2, spike_y), (spike_x + width / 4, spike_y - height)]
            self.spikes.append(spike)

    def draw(self, canvas):
        for spike in self.spikes:
            canvas.draw_polygon(spike, 1, "#326F28", "#326F28")

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
        self.can_move = True

    def draw(self, canvas):
        canvas.draw_polygon([(self.pos.x - PLAYER_SIZE / 2, self.pos.y - PLAYER_SIZE / 2),
                             (self.pos.x + PLAYER_SIZE / 2, self.pos.y - PLAYER_SIZE / 2),
                             (self.pos.x + PLAYER_SIZE / 2, self.pos.y + PLAYER_SIZE / 2),
                             (self.pos.x - PLAYER_SIZE / 2, self.pos.y + PLAYER_SIZE / 2)],
                            1, "Red", "Red")

    def update(self, traps):
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

        # Check for collisions with traps
        for trap in traps:
            # Collision with top of the trap
            if self.pos.y - self.height / 2 <= trap.edge_t and \
                    self.pos.y + self.height / 2 > trap.edge_t and \
                    self.pos.x + self.width / 2 > trap.edge_l and \
                    self.pos.x - self.width / 2 < trap.edge_r:
                self.pos.y = trap.edge_t - self.height / 2
                self.vel.y = 0
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  # Stop horizontal movement
                self.moving_right = False  # Stop horizontal movement
                break
        else:  # No collision with trap's top edge
            self.can_move = True


       

    def jump(self):
        if self.on_ground:
            self.vel.y = -7  # Adjust jump strength as needed

    def start_move_left(self):
        if self.can_move:  # Check if the player is allowed to move
            self.moving_left = True

    def stop_move_left(self):
        self.moving_left = False

    def start_move_right(self):
        if self.can_move:  # Check if the player is allowed to move
            self.moving_right = True

    def stop_move_right(self):
        self.moving_right = False

frame = simplegui.create_frame("Block Wall", CANVAS_WIDTH, CANVAS_HEIGHT, 0)           
       
class Interaction:
    def __init__(self, player, trapsONE):
        self.player = player
        self.trapsONE = trapsONE
        self.current_screen = 1  # Initially set to Screen ONE

    def update(self):
        if self.current_screen == 1:
            self.player.update(self.trapsONE)
        elif self.current_screen == 2:
            self.player.update(self.trapsONE)

    def draw(self, canvas):
        self.update()
        self.player.draw(canvas)
        if self.current_screen == 1:
            for trap in self.trapsONE:
                trap.draw(canvas)
        elif self.current_screen == 2:
            for trap in self.trapsONE:
                trap.draw(canvas)

    def switch_screen(self):
        if self.current_screen == 1:
            self.current_screen = 2
        elif self.current_screen == 2:
            self.current_screen = 1

block_pos = Vector(50, 500)

player = Player(block_pos)

trapsONE = [
    Trap(6, (500, 600), 40, 40),  # Creates a Trap with 6 spikes in a row
    Trap(3, (300, 600), 40, 40)   # Creates a Trap with 3 spikes in a row
]

i = Interaction(player, trapsONE)

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
