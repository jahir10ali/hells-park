try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from imagesANDbuttons import draw_button, draw_image


# Constants
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 30
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  # Y-coordinate of the floor


troll_face = simplegui.load_image('https://i.ibb.co/q0nG6Qd/troll-face.png')
game_over_sound = simplegui.load_sound('https://audio.jukehost.co.uk/4rXY9bKqh9LnxFndLGst7Xs9U9YpKr9b')
troll_laugh = simplegui.load_sound('https://audio.jukehost.co.uk/AbmCCtjkcbKmoolGFCixHvlik4zfDVES')
game_over_sound.set_volume(0.2)
coin_sound = simplegui.load_sound('https://audio.jukehost.co.uk/UeryrWle3hDSLEgIqrA2zyNG0mNqX15F')
jump_sound = simplegui.load_sound('https://audio.jukehost.co.uk/849X7g5DQKqnC6dGOuU1asWeUx4D1GUy')

arrow = simplegui.load_image('https://cdn1.iconfinder.com/data/icons/pixel-game/110/pixel-39-512.png')

finish_line = simplegui.load_image('https://i.ibb.co/0Bwn2vJ/finish-line.png')


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
        
    
      
class Coin:
    def __init__(self, position, radius, border):
        self.x, self.y = position
        self.radius = radius
        self.border = border

    def draw(self, canvas):
        canvas.draw_circle([self.x, self.y], self.radius, self.border, 'Yellow', 'Orange')

        
        
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
        

    def update(self, platforms, traps, coins):
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

        # Check for collisions with coins
        for coin in coins:
            distance = (self.pos.x - coin.x) ** 2 + (self.pos.y - coin.y) ** 2
            if distance <= (coin.radius + self.width / 2) ** 2:
                coins.remove(coin)
                coin_sound.play()
                break



    def jump(self):
        if self.on_ground:
            jump_sound.play()
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

        
        
        
#frame = simplegui.create_frame("Block Wall", CANVAS_WIDTH, CANVAS_HEIGHT, 0)           
       

class Interaction:
    def __init__(self, platformsONE, platformsTWO, player, trapsONE, trapsTWO, coinsONE, coinsTWO):
        self.player = player
        self.platformsONE = platformsONE
        self.platformsTWO = platformsTWO
        self.trapsONE = trapsONE
        self.trapsTWO = trapsTWO
        self.coinsONE = coinsONE
        self.coinsTWO = coinsTWO
        self.current_screen = 1  # Initially set to Screen ONE
        self.game_over = False  # Flag to track if game over
        self.lives_count = 3  # Flag to track if game over
        self.coin_count = 0  # Counter for collected coins
        self.initial_coins_len = len(self.coinsONE) + len(self.coinsTWO)

        # Buttons
        self.pause_btn_img = 'https://i.ibb.co/LkHqxxz/pause-btn.jpg'
        self.paused_screen_img = 'https://i.ibb.co/ZdXM7LN/paused-screen.png'
        self.play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg' 
        self.exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
        self.reset_btn_img = 'https://i.ibb.co/p08zvqP/reset-btn.jpg'


    def update(self):
        if self.current_screen == 1:
            self.player.update(self.platformsONE, self.trapsONE, self.coinsONE)
        elif self.current_screen == 2:
            self.player.update(self.platformsTWO, self.trapsTWO, self.coinsTWO)
        
        # Check for game over condition
        if not self.player.can_move:
            self.game_over = True

        
        # Update coin count
        self.coin_count = self.initial_coins_len - len(self.coinsONE) - len(self.coinsTWO)

        
    def draw(self, canvas):
        self.update()
        self.player.draw(canvas)
        self.pause_btn = draw_button(canvas, self.pause_btn_img, 760, 20, 50, 50)
        if self.current_screen == 1 and not self.game_over:
            canvas.draw_image(arrow, (arrow.get_width()/2, arrow.get_height()/2), 
                                  (arrow.get_width(), arrow.get_height()), (660, 170), 
                                  (arrow.get_width()/5, arrow.get_height()/3), 4.7)
            canvas.draw_text("This way", (760, 180), 20, "White", "monospace")
        if self.current_screen == 2 and not self.game_over:
            canvas.draw_image(finish_line, (finish_line.get_width()/2, finish_line.get_height()/2), 
                                  (finish_line.get_width(), finish_line.get_height()), (500, 500), 
                                  (finish_line.get_width(), finish_line.get_height()))
        if self.current_screen == 1:
            for platform in self.platformsONE:
                platform.draw(canvas)
            for trap in self.trapsONE:
                trap.draw(canvas)
            for coin in self.coinsONE:
                coin.draw(canvas)
        elif self.current_screen == 2:
            canvas.draw_circle([80, 65], 20, 3, 'Yellow', 'Orange')
            canvas.draw_text("^^ Don't forget this coin! ^^", (10, 140), 15, "White", "monospace")
            for trap in self.trapsTWO:
                trap.draw(canvas)
            for platform in self.platformsTWO:
                platform.draw(canvas)
            for coin in self.coinsTWO:
                coin.draw(canvas)


        
        # Draw coin count
        canvas.draw_text("Coins collected: " + str(self.coin_count) + "/" + str(self.initial_coins_len), (350, 40), 20, "White", "monospace") 
        if self.coin_count != self.initial_coins_len:
            canvas.draw_text("Collect all coins to finish level", (270, 20), 20, "White", "monospace")
        else:
            canvas.draw_text("All coins collected, reach finish line", (255, 20), 20, "White", "monospace")
    
    
        # Draw "Game Over" text if game over
        if self.game_over:
            canvas.draw_text("Game Over", (260, 230), 80, "Red", "monospace")
            canvas.draw_text("LOL!!!", (50, 50), 50, "Red", "monospace")
            canvas.draw_image(troll_face, (troll_face.get_width()/2, troll_face.get_height()/2), 
                              (troll_face.get_width(), troll_face.get_height()), (460, 360), 
                              (troll_face.get_width()/3, troll_face.get_height()/3))
            #game_over_sound.play()

    def drawTWO(self, canvas):
        self.paused_screen = draw_image(canvas, self.paused_screen_img, 450, 300, 900, 600)
        self.play_btn = draw_button(canvas, self.play_btn_img, 500, 450, 250, 100)
        self.exit_btn = draw_button(canvas, self.exit_btn_img, 150, 450, 250, 100)


    def handle_mouse_click(self, pos, frame, draw, drawTWO):
        if self.pause_btn.is_clicked(pos):
            frame.set_draw_handler(drawTWO)
        elif self.exit_btn.is_clicked(pos):
            import levels
            frame.set_draw_handler(levels.draw)
            frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))

    def switch_screen(self):
        if self.current_screen == 1:
            self.current_screen = 2
        elif self.current_screen == 2:
            self.current_screen = 1

            

platformsONE = [
    Platform((2, 563), 250, 35),
    Platform((350, 470), 50, 20),
    Platform((495, 563), 200, 35),
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
    Platform((900, 1), 20, CANVAS_HEIGHT),
]

block_pos = Vector(platformsONE[0].width / 2, 500)

player = Player(block_pos)

trapsONE = [
    Trap(12, (276, 600), 39, 40),  # Creates a Trap with 6 spikes in a row
    Trap(10, (723, 600), 39, 40),  # Creates a Trap with 6 spikes in a row
    Trap(2, (550, 68), 30, 15),
]

trapsTWO = [
    Trap(40, (2, 600), 40, 40),  # Creates a Trap with 6 spikes in a row
    Trap(11, (30, 120), 30, 31),  # Creates a Trap with 6 spikes in a row
]

coinsONE = [
    Coin((64,33), 20, 3),
    Coin((364,273), 20, 3),
    Coin((770,273), 20, 3),
    Coin((650,45), 20, 3),
    Coin((660,540), 20, 3),
]

coinsTWO = [
    Coin((265,320), 20, 3),
    Coin((428,395), 20, 3),
    Coin((810,245), 20, 3),
    Coin((850,574), 20, 3),
]

i = Interaction(platformsONE, platformsTWO, player, trapsONE, trapsTWO, coinsONE, coinsTWO)

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


def click(pos, frame):
    i.handle_mouse_click(pos, frame, i.draw, i.drawTWO) 

