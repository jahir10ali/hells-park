'''
This is the level1.py file that includes everything for level 1.
'''

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
# This import is for making use of the Vector class
from imagesANDbuttons import draw_button, draw_image
# This import is for drawing buttons and images

# These are the constants to be used in game
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 20
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  # This is the Y-coordinate of the floor

# These are all the sounds, and the player sprite being loaded in
game_over_sound = simplegui.load_sound('https://audio.jukehost.co.uk/4rXY9bKqh9LnxFndLGst7Xs9U9YpKr9b')
coin_sound = simplegui.load_sound('https://audio.jukehost.co.uk/UeryrWle3hDSLEgIqrA2zyNG0mNqX15F')
jump_sound = simplegui.load_sound('https://audio.jukehost.co.uk/849X7g5DQKqnC6dGOuU1asWeUx4D1GUy')
sprite = simplegui.load_image('https://i.ibb.co/BVLTF72/sprite.png')
sprite_inverted = simplegui.load_image('https://i.ibb.co/jfXGNJp/sprite-inverted.png')


# This is the Platform class that represents each platform in the game
class Platform:
    def __init__(self, position, width, height):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.edge_l = self.x  
        self.edge_r = self.x + self.width  
        self.edge_b = self.y + self.height 
        self.edge_t = self.y 

    def draw(self, canvas):
        # This draws the platforms
        canvas.draw_polygon([(self.x, self.y),
                             (self.x + self.width, self.y),
                             (self.x + self.width, self.y + self.height),
                             (self.x, self.y + self.height)],
                            4, '#1FB016', '#915518')

# This is the Trap class that represents each trap in the game
class Trap:
    def __init__(self, spikes_quantity, position, width, height):
        self.spikes = []
        self.width = width
        self.height = height
        self.edge_l = position[0] - width / 2  
        self.edge_r = position[0] + (width / 2 * spikes_quantity)  
        self.edge_b = position[1]  
        self.edge_t = position[1] - height  
        
        # This calculates spike positions
        for i in range(spikes_quantity):
            spike_x = position[0] - width / 2 + i * width / 2
            spike_y = position[1]
            spike = [(spike_x, spike_y), (spike_x + width / 2, spike_y), (spike_x + width / 4, spike_y - height)]
            self.spikes.append(spike)

    def draw(self, canvas):
        for spike in self.spikes:
            canvas.draw_polygon(spike, 3, "#5F5F5F", "#A5A2A2")
        
    
 # This is the Coin class that represents each coin in the game     
class Coin:
    def __init__(self, position, radius, border):
        self.x, self.y = position
        self.radius = radius
        self.border = border

    def draw(self, canvas):
        canvas.draw_circle([self.x, self.y], self.radius, self.border, 'Yellow', 'Orange')

        
# This is the Player class that represents the player (sprite) in the game        
class Player:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel = Vector(0, 0)
        self.on_ground = True
        self.moving_left = False
        self.moving_right = False
        self.can_move = True
        self.level_complete = False
        self.spritesheet_width = 512
        self.spritesheet_height = 576
        self.column = 8
        self.rows = 9
        self.vel = Vector()
        self.frame_index = [0,0]
        self.modulo = 5
        self.sprite_number_r_and_l = 22
        self.sprite_top = 20
        self.sprite_bottom = 35

        self._init_dimension()

    def _init_dimension(self):
        self.frame_width = self.spritesheet_width / self.column
        self.frame_height = self.spritesheet_height / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2

    def reset(self, pos):
        self.__init__(pos, sprite)

    def draw(self, canvas):
        
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x,
            self.frame_height * self.frame_index[1] + self.frame_centre_y
        )
       
        source_size = (self.frame_width, self.frame_height)
        dest_centre = self.pos.get_p()
        dest_size = (150, 150)

        canvas.draw_image(self.image, source_centre, source_size, dest_centre, dest_size)
        
    def next_frame(self):
        self.frame_index[0] = (self.frame_index[0] + 1) % self.modulo

    def update(self, platforms, traps, coins, finish_line, clock):
        self.vel += GRAVITY
        # This adjusts the velocity based on movement direction
        if self.moving_left:
            self.vel.x = -5
        elif self.moving_right:
            self.vel.x = 5
        else:
            self.vel.x = 0
            
        self.pos += self.vel
        
        # This checks if player hits the floor
        if self.pos.y >= CANVAS_HEIGHT - self.sprite_top:
            self.pos.y = CANVAS_HEIGHT - self.sprite_top
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
          
        
        # This ensures the player stays within canvas bounds
        # This checks if the player hits the right edge of the screen
        if self.pos.x > CANVAS_WIDTH - self.sprite_number_r_and_l:
            self.pos.x = CANVAS_WIDTH  - self.sprite_number_r_and_l
        # This checks if the player hits the left edge of the screen
        if self.pos.x < self.sprite_number_r_and_l:
            self.pos.x = self.sprite_number_r_and_l

        # This checks for collisions with platforms
        for platform in platforms:
            # This checks for collisions with the left side of the platform
            if self.vel.x > 0 and self.pos.x + self.sprite_number_r_and_l  >= platform.edge_l and \
                self.pos.x - self.sprite_number_r_and_l  < platform.edge_l and \
                self.pos.y + self.sprite_bottom > platform.y and \
                self.pos.y - self.sprite_top < platform.y + platform.height:
                self.pos.x = platform.edge_l - self.sprite_number_r_and_l
            # This checks for collisions with the right side of the platform
            elif self.vel.x < 0 and self.pos.x - self.sprite_number_r_and_l <= platform.edge_r and \
                    self.pos.x + self.sprite_number_r_and_l > platform.edge_r and \
                    self.pos.y + self.sprite_bottom > platform.y and \
                    self.pos.y - self.sprite_top  < platform.y + platform.height:
                self.pos.x = platform.edge_r + self.sprite_number_r_and_l 
            # This checks for collisions with the bottom side of the platform
            if self.pos.y - self.sprite_top  < platform.edge_b and \
                self.pos.y + self.vel.y - self.sprite_bottom > platform.y and \
                self.pos.x + self.sprite_number_r_and_l > platform.edge_l and \
                self.pos.x - self.sprite_number_r_and_l  < platform.edge_r:
                    # Collision with bottom of the platform
                    self.pos.y = platform.edge_b + self.sprite_top # Move player to just above the platform's bottom edge
                    self.vel.y = 0  # Stop vertical movement
                    self.on_ground = True  # Set player on ground after collision
            # This checks for collisions with the top side of the platform
            elif self.vel.y > 0 and self.pos.y - self.sprite_top  <= platform.edge_t and \
                    self.pos.y + self.sprite_bottom > platform.edge_t and \
                    self.pos.x + self.sprite_number_r_and_l  > platform.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < platform.edge_r:
                self.pos.y = platform.edge_t - self.sprite_bottom 
                self.vel.y = 0
                self.on_ground = True
                if (self.pos.x + self.sprite_number_r_and_l > platform.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < platform.edge_r):
                    self.on_ground = True

        
        for trap in traps:
            # This checks for collisions with the traps
            if self.pos.y - self.sprite_top <= trap.edge_t and \
                    self.pos.y + self.sprite_bottom  > trap.edge_t and \
                    self.pos.x + self.sprite_number_r_and_l > trap.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < trap.edge_r:
                self.pos.y = trap.edge_t - self.sprite_bottom
                self.vel.y = 0
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  
                self.moving_right = False
                self.death()
                break
        else:  
            self.can_move = True

        # This checks for collisions with each coin
        for coin in coins:
            distance = (self.pos.x - coin.x) ** 2 + (self.pos.y - coin.y) ** 2
            if distance <= (coin.radius + self.sprite_number_r_and_l) ** 2:
                coins.remove(coin)
                coin_sound.play()
                break


        # This checks for collisions with the finish line
        finish_line_left = 85
        finish_line_right = 85 + finish_line.get_width() / 3
        finish_line_top = 107
        finish_line_bottom = 107 + finish_line.get_height() / 3

        # This checks for collisions with the left side of the finish line
        if self.pos.x - self.sprite_number_r_and_l <= finish_line_right and \
                self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.y - self.sprite_top <= finish_line_bottom:
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  
            self.moving_right = False  
            return

        # This checks for collisions with the right side of the finish line
        if self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.x - self.sprite_number_r_and_l <= finish_line_right and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.y - self.sprite_top <= finish_line_bottom:
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  
            self.moving_right = False  
            return

        # This checks for collisions with the top side of the finish line
        if self.pos.y - self.sprite_top <= finish_line_bottom and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.x - self.sprite_number_r_and_l <= finish_line_right:
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False 
            self.moving_right = False 
            return

    def set(self, new_frame_index, new_modulo):
        self.frame_index = new_frame_index
        self.modulo = new_modulo

    def jump(self):
        if self.on_ground:
            jump_sound.play()
            self.vel.y = -8 
            self.image = sprite
            self.set([0,2], 3)

    def start_move_left(self):
        if self.can_move: 
            self.moving_left = True
            self.image = sprite_inverted
            self.set([0,1], 8)

    def stop_move_left(self):
        self.moving_left = False
        self.image = sprite
        self.set([0,0], 5)

    def start_move_right(self):
        if self.can_move:  
            self.moving_right = True
            self.image = sprite
            self.set([0,1], 8)

    def stop_move_right(self):
        self.moving_right = False
        self.image = sprite
        self.set([0,0], 5)
    
    def death(self):
        self.die = True
        self.image = sprite
        self.set([0, 7], 6)

class Clock():
        def __init__(self):
            self.time = 0

        def tick(self):
            self.time += 1

        def transition(self, frame_duration):
            return self.time % frame_duration == 0
        
               
# This is the Interaction class that brings all the other classes together
# It also has its own functionality such as resetting the game, mouse clicks, and more
class Interaction:
    def __init__(self, platforms, player, clock, traps, coins, block_pos):
        self.player = player
        self.clock = clock
        self.platforms = platforms
        self.traps = traps
        self.coins = coins
        self.game_over = False  
        self.coin_count = 0 
        self.initial_coins_len = len(self.coins)
        self.block_pos = Vector(platforms[0].width / 2, 500)

        # Buttons
        self.pause_btn_img = 'https://i.ibb.co/LkHqxxz/pause-btn.jpg'
        self.paused_screen_img = 'https://i.ibb.co/ZdXM7LN/paused-screen.png'
        self.play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg' 
        self.exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
        self.reset_btn_img = 'https://i.ibb.co/p08zvqP/reset-btn.jpg'
        self.next_lvl_btn_img = 'https://i.ibb.co/5cyXJTm/next-lvl-btn.jpg'

        self.pause_btn = None
        self.paused_screen = None
        self.play_btn = None 
        self.exit_btn = None
        self.reset_btn = None
        self.next_lvl_btn = None

        # Images
        self.lvl1_bg = 'https://i.ibb.co/M1PzWg8/lvl1-bg.jpg'
        self.finish_line = simplegui.load_image('https://i.ibb.co/7vHknZT/finish-line.png')
        self.level_complete_img = simplegui.load_image('https://i.ibb.co/X37pXc9/level-complete.png')
        self.game_over_img = simplegui.load_image('https://i.ibb.co/tK8VgNP/game-over.png')


    def reset(self, platforms, player, clock, traps, coins, block_pos):
        self.__init__(platforms, player, clock, traps, coins, block_pos)
    
    
    def update(self):
        self.player.update(self.platforms, self.traps, self.coins, self.finish_line, self.clock)
        
        # This checks for the game over condition
        if not self.player.can_move and player.level_complete == False:
            self.game_over = True

        
        # This updates the coin count
        self.coin_count = self.initial_coins_len - len(self.coins)

        
    def draw(self, canvas):
        draw_image(canvas, self.lvl1_bg, 450, 300, 900, 600)
        self.update()

        self.clock.tick()
        if self.clock.transition(10):
            self.player.next_frame()

        self.player.draw(canvas)

        if not player.level_complete:
            canvas.draw_text('Jump from platform to platform!', (50,310), 20, 'Black', 'monospace')
            canvas.draw_text('Avoid the spikes or it is Game Over!', (262,520), 20, 'Black', 'monospace')
            canvas.draw_text('Collect all the coins!', (490,170), 20, 'Black', 'monospace')
        if not self.game_over:
            self.pause_btn = draw_button(canvas, self.pause_btn_img, 30, 20, 50, 50)
            if self.coin_count == self.initial_coins_len:
                canvas.draw_image(self.finish_line, (self.finish_line.get_width()/2, self.finish_line.get_height()/2), 
                                  (self.finish_line.get_width(), self.finish_line.get_height()), (85, 107), 
                                  (self.finish_line.get_width()/3, self.finish_line.get_height()/3))
        
        
 
        for platform in self.platforms:
            platform.draw(canvas)
        for trap in self.traps:
            trap.draw(canvas)
        for coin in self.coins:
            coin.draw(canvas)
        
        # Draw coin count
        canvas.draw_text("Coins collected: " + str(self.coin_count) + "/" + str(self.initial_coins_len), (350, 40), 20, "Black", "monospace") 
        if self.coin_count != self.initial_coins_len:
            canvas.draw_text("Collect all coins to finish level", (270, 20), 20, "Black", "monospace")
        else:
            canvas.draw_text("All coins collected, reach finish line", (255, 20), 20, "Black", "monospace")
    
    
        # Draw "Game Over" text if game over
        if self.game_over:
            self.exit_btn = draw_button(canvas, self.exit_btn_img, 255, 420, 500/2, 200/2)
            self.reset_btn = draw_button(canvas, self.reset_btn_img, 555, 420, 500/5, 500/5)
            canvas.draw_image(self.game_over_img, (self.game_over_img.get_width()/2, self.game_over_img.get_height()/2), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()), (450, 200), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()))
            canvas.draw_text("LOL!!!", (50, 50), 50, "Red", "monospace")
            game_over_sound.play()

        # Draw "Level Complete" text if level complete
        if player.level_complete:
            self.next_lvl_btn = draw_button(canvas, self.next_lvl_btn_img, 255, 420, 500/2, 200/2)
            self.reset_btn = draw_button(canvas, self.reset_btn_img, 555, 420, 500/5, 500/5)
            canvas.draw_image(self.level_complete_img, (self.level_complete_img.get_width()/2, self.level_complete_img.get_height()/2), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()), (450, 260), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()))
            

    def drawTWO(self, canvas):
        self.paused_screen = draw_image(canvas, self.paused_screen_img, 450, 300, 900, 600)
        self.play_btn = draw_button(canvas, self.play_btn_img, 500, 450, 250, 100)
        self.exit_btn = draw_button(canvas, self.exit_btn_img, 150, 450, 250, 100)

    def reset_game(self):
        # This resets everything
        self.player.reset(self.block_pos)
        self.coins = [
            Coin((200,459), 20, 3),
            Coin((480,400), 20, 3),
            Coin((825,259), 20, 3),
            Coin((265,137), 20, 3),
        ]
        # This resets the Interaction object itself
        self.reset(self.platforms, self.player, self.clock, self.traps, self.coins, self.block_pos)

    def handle_mouse_click(self, pos, frame, draw, drawTWO):
        if self.pause_btn.is_clicked(pos):
            frame.set_draw_handler(drawTWO)
        if self.next_lvl_btn is not None and self.next_lvl_btn.is_clicked(pos):
            import level2
            frame.set_draw_handler(level2.i.draw)
            frame.set_keydown_handler(level2.keydown)
            frame.set_keyup_handler(level2.keyup)
            frame.set_mouseclick_handler(lambda pos: level2.click(pos, frame))     
        if self.exit_btn is not None and self.exit_btn.is_clicked(pos):
            self.reset_game() 
            import levels
            frame.set_draw_handler(levels.draw)
            frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))      
        if self.reset_btn is not None and self.reset_btn.is_clicked(pos):
            self.reset_game()
        if self.play_btn is not None and self.play_btn.is_clicked(pos):
            frame.set_draw_handler(draw)
                

platforms = [
    Platform((10, 558), 100, 40),
    Platform((155, 483), 100, 40),
    Platform((455, 423), 50, 50),
    Platform((700, 375), 50, 220),
    Platform((800, 285), 50, 50),
    Platform((455, 230), 170, 30),
    Platform((45, 160), 250, 40)
]


block_pos = Vector(platforms[0].width / 2, 500)

player = Player(block_pos, sprite)

traps = [
    Trap(29, (138, 600), 40, 40),
    Trap(7, (777, 600), 40, 40),
    Trap(1, (198, 160), 40, 40)
]


coins = [
    Coin((200,459), 20, 3),
    Coin((480,400), 20, 3),
    Coin((825,259), 20, 3),
    Coin((265,137), 20, 3),
]

clock = Clock()


i = Interaction(platforms, player, clock, traps, coins, block_pos)


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

