try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from imagesANDbuttons import draw_button, draw_image

# Constants
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
PLAYER_SIZE = 100
GRAVITY = Vector(0, 0.25)
FLOOR_Y = CANVAS_HEIGHT - PLAYER_SIZE / 2  # Y-coordinate of the floor


game_over_sound = simplegui.load_sound('https://audio.jukehost.co.uk/4rXY9bKqh9LnxFndLGst7Xs9U9YpKr9b')
#troll_laugh = simplegui.load_sound('https://audio.jukehost.co.uk/AbmCCtjkcbKmoolGFCixHvlik4zfDVES')
game_over_sound.set_volume(0.2)
coin_sound = simplegui.load_sound('https://audio.jukehost.co.uk/UeryrWle3hDSLEgIqrA2zyNG0mNqX15F')
jump_sound = simplegui.load_sound('https://audio.jukehost.co.uk/849X7g5DQKqnC6dGOuU1asWeUx4D1GUy')

sprite = simplegui.load_image('https://i.ibb.co/BVLTF72/sprite.png')
sprite_inverted = simplegui.load_image('https://i.ibb.co/jfXGNJp/sprite-inverted.png')

up_down_monster = simplegui.load_image('https://i.ibb.co/1rgJtz9/spike-ball-by-lwiis64-df30ssj.png')
side_monster = simplegui.load_image('https://i.ibb.co/QPFrDkF/spiky-monster.png')

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
                            3, 'black', 'black')

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
            canvas.draw_polygon(spike, 1, "red", "red")

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

class Monster:
    def __init__(self, pos,  width, original_x, speed):
        self.x, self.y = pos
        self.radius = 25
        self.right = 20
        self.left = 25
        self.moving_left = True
        self.moving_right = False
        self.width = width
        self.original_x = original_x
        self.speed = speed
    
    def reset(self, pos,  width, original_x, speed):
        self.__init__(pos,  width, original_x, speed)


    def draw(self, canvas):
        canvas.draw_image(side_monster, (side_monster.get_width()/2, side_monster.get_height()/2), (side_monster.get_width(), side_monster.get_height()), (self.x, self.y), (self.radius*2, self.radius*2))




 
    def update(self):
        for monster in monsters:
            if monster.moving_left:
                monster.x -= monster.speed
                if monster.x <= monster.original_x - monster.width/2:
                    monster.moving_left = False
                    monster.moving_right = True
            if monster.moving_right:
                monster.x += monster.speed
                if monster.x >= monster.original_x + monster.width/2:
                    monster.moving_right = False
                    monster.moving_left = True
            
            

class Up_down_monster:
    def __init__(self, pos, radius, width, original_y, speed):
        self.x, self.y = pos
        self.radius = radius
        self.moving_down = True
        self.moving_up = False
        self.width = width
        self.original_y = original_y
        self.speed = speed
    
    def reset(self, pos, radius, width, original_y, speed):
        self.__init__(pos, radius, width, original_y, speed)

    def draw(self, canvas):
        canvas.draw_image(up_down_monster, (up_down_monster.get_width()/2, up_down_monster.get_height()/2), (up_down_monster.get_width(), up_down_monster.get_height()), (self.x, self.y), (self.radius*2, self.radius*2) )

    def update(self):
        for monster in up_and_down_monsters:
            if monster.moving_down:
                monster.y += monster.speed
                if monster.y >= monster.original_y + monster.width/2:
                    monster.moving_down = False
                    monster.moving_up = True
            if monster.moving_up:
                monster.y -= monster.speed
                if monster.y <= monster.original_y - monster.width/2:
                    monster.moving_up = False
                    monster.moving_down = True
                 
    
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
        self.jumping = False
        self.jump_strength = 15
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
        

    def update(self, platforms, traps, coins, finish_line, monsters, up_down_monsters, clock):
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
        if self.pos.y >= CANVAS_HEIGHT - PLAYER_SIZE/2:
            self.pos.y = CANVAS_HEIGHT - PLAYER_SIZE/2
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
            
        # Ensure player stays within canvas bounds
        # Check if player hits the right edge of the screen
        if self.pos.x > CANVAS_WIDTH - self.sprite_number_r_and_l:
            self.pos.x = CANVAS_WIDTH  - self.sprite_number_r_and_l
        # Check if player hits the left edge of the screen
        if self.pos.x < self.sprite_number_r_and_l:
            self.pos.x = self.sprite_number_r_and_l

        
        # Check for collisions with platforms
        for platform in platforms:
            # Collision with left side of the platform
            if self.vel.x > 0 and self.pos.x + self.sprite_number_r_and_l  >= platform.edge_l and \
                self.pos.x - self.sprite_number_r_and_l  < platform.edge_l and \
                self.pos.y + self.sprite_bottom > platform.y and \
                self.pos.y - self.sprite_top < platform.y + platform.height:
                self.pos.x = platform.edge_l - self.sprite_number_r_and_l
            # Collision with right side of the platform
            elif self.vel.x < 0 and self.pos.x - self.sprite_number_r_and_l <= platform.edge_r and \
                    self.pos.x + self.sprite_number_r_and_l > platform.edge_r and \
                    self.pos.y + self.sprite_bottom > platform.y and \
                    self.pos.y - self.sprite_top  < platform.y + platform.height:
                self.pos.x = platform.edge_r + self.sprite_number_r_and_l 
            # Collision with bottom of the platform
            if self.pos.y - self.sprite_top  < platform.edge_b and \
                self.pos.y + self.vel.y - self.sprite_bottom > platform.y and \
                self.pos.x + self.sprite_number_r_and_l > platform.edge_l and \
                self.pos.x - self.sprite_number_r_and_l  < platform.edge_r:
                    # Collision with bottom of the platform
                    self.pos.y = platform.edge_b + self.sprite_top # Move player to just above the platform's bottom edge
                    self.vel.y = 0  # Stop vertical movement
                    self.on_ground = True  # Set player on ground after collision
            # Collision with top of the platform
            elif self.vel.y > 0 and self.pos.y - self.sprite_top  <= platform.edge_t and \
                    self.pos.y + self.sprite_bottom > platform.edge_t and \
                    self.pos.x + self.sprite_number_r_and_l  > platform.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < platform.edge_r:
                self.pos.y = platform.edge_t - self.sprite_bottom 
                self.vel.y = 0
                self.on_ground = True
                # Additional condition to prevent interference with left/right edge collision
                if (self.pos.x + self.sprite_number_r_and_l > platform.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < platform.edge_r):
                    self.on_ground = True
     
        # Check for collisions with traps
        for trap in traps:
            # Collision with top of the trap
            if self.pos.y - self.sprite_top <= trap.edge_t and \
                    self.pos.y + self.sprite_bottom  > trap.edge_t and \
                    self.pos.x + self.sprite_number_r_and_l > trap.edge_l and \
                    self.pos.x - self.sprite_number_r_and_l < trap.edge_r:
                self.pos.y = trap.edge_t - self.sprite_bottom
                self.vel.y = 0
                self.on_ground = False
                self.can_move = False
                self.moving_left = False  # Stop horizontal movement
                self.moving_right = False
                self.death()
                break
        else:  # No collision with trap's top edge
            self.can_move = True

        # Check for collisions with coins
        for coin in coins:
            distance = (self.pos.x - coin.x) ** 2 + (self.pos.y - coin.y) ** 2
            if distance <= (coin.radius + self.sprite_number_r_and_l) ** 2:
                coins.remove(coin)
                coin_sound.play()
                break

        # Check for collisions with Monsters
        for monster in monsters:
            # Check for collisions between the Player and the top of the Monster
            if (monster.x - monster.radius <= self.pos.x <= monster.x + monster.right and
                monster.y - monster.radius <= self.pos.y + self.sprite_bottom <= monster.y + monster.radius):
                monster.x = -300
                monster.y = 800
            # Check for collisions between the Player and the sides of the Monster
            if (monster.x - monster.radius <= self.pos.x + self.sprite_number_r_and_l and self.pos.x - self.sprite_number_r_and_l <= monster.x + monster.right and
                monster.y - monster.radius <= self.pos.y + self.sprite_bottom and self.pos.y - self.sprite_top <= monster.y + monster.radius ):
                self.vel.y = 0
                self.can_move = False
                self.moving_left = False
                self.moving_right = False
                self.death()

        for monster in up_down_monsters:
            if ( monster.x - monster.radius <= self.pos.x + self.sprite_number_r_and_l and self.pos.x - self.sprite_number_r_and_l <= monster.x + monster.radius and
                monster.y - monster.radius <= self.pos.y + self.sprite_bottom and self.pos.y - self.sprite_top <= monster.y + monster.radius):
                self.pos = Vector(20,600)
                self.death()
        
        # Check for collisions with finish line
        finish_line_left = 63
        finish_line_right = 63 + finish_line.get_width() / 3
        finish_line_top = 150
        finish_line_bottom = 150 + finish_line.get_height() / 3

        # Collision with left edge of finish line
        if self.pos.x - self.sprite_number_r_and_l <= finish_line_right and \
                self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.y - self.sprite_top <= finish_line_bottom:
            # Handle collision with left edge
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  # Stop horizontal movement
            self.moving_right = False  # Stop horizontal movement
            return

        # Collision with right edge of finish line
        if self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.x - self.sprite_number_r_and_l <= finish_line_right and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.y - self.sprite_top <= finish_line_bottom:
            # Handle collision with right edge
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  # Stop horizontal movement
            self.moving_right = False  # Stop horizontal movement
            return

        # Collision with top edge of finish line
        if self.pos.y - self.sprite_top <= finish_line_bottom and \
                self.pos.y + self.sprite_bottom >= finish_line_top and \
                self.pos.x + self.sprite_number_r_and_l >= finish_line_left and \
                self.pos.x - self.sprite_number_r_and_l <= finish_line_right:
            # Handle collision with top edge
            self.level_complete = True
            self.on_ground = False
            self.can_move = False
            self.moving_left = False  # Stop horizontal movement
            self.moving_right = False  # Stop horizontal movement
            return
            
               
    def set(self, new_frame_index, new_modulo):
        self.frame_index = new_frame_index
        self.modulo = new_modulo

    def jump(self):
        if self.on_ground:
            jump_sound.play()
            self.vel.y = -8
            self.image = sprite
            self.set([0,2], 3)  # Adjust jump strength as needed

    def start_move_left(self):
        if self.can_move:  # Check if the player is allowed to move
            self.moving_left = True
            self.image = sprite_inverted
            self.set([0,1], 8)

    def stop_move_left(self):
        self.moving_left = False
        self.image = sprite
        self.set([0,0], 5)

    def start_move_right(self):
        if self.can_move:  # Check if the player is allowed to move
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
        
       

class Interaction:
    def __init__(self, platforms, player, clock, traps, coins, monsters, up_down_monsters, block_pos):
        self.player = player
        self.clock = clock
        self.platforms = platforms
        self.traps = traps
        self.coins = coins
        self.game_over = False  # Flag to track if game over
        self.coin_count = 0  # Counter for collected coins
        self.initial_coins_len = len(self.coins)
        self.monsters = monsters
        self.up_down_monsters = up_down_monsters
        self.block_pos = Vector(30, 540)
        self.sprite = player.image

        # Buttons
        self.pause_btn_img = 'https://i.ibb.co/LkHqxxz/pause-btn.jpg'
        self.paused_screen_img = 'https://i.ibb.co/ZdXM7LN/paused-screen.png'
        self.play_btn_img = 'https://i.ibb.co/KFG5ms3/play-btn.jpg' 
        self.exit_btn_img = 'https://i.ibb.co/r29NXsx/exit-btn.jpg'
        self.reset_btn_img = 'https://i.ibb.co/p08zvqP/reset-btn.jpg'

        self.pause_btn = None
        self.paused_screen = None
        self.play_btn = None 
        self.exit_btn = None
        self.reset_btn = None

        # Images
        self.lvl4_bg = 'https://i.ibb.co/ZNxkbF2/lvl4-bg.jpg'
        self.finish_line = simplegui.load_image('https://i.ibb.co/7vHknZT/finish-line.png')
        self.level_complete_img = simplegui.load_image('https://i.ibb.co/X37pXc9/level-complete.png')
        self.game_over_img = simplegui.load_image('https://i.ibb.co/tK8VgNP/game-over.png')

    def reset(self, platforms, player, clock, traps, coins, monsters, up_down_monsters, block_pos):
        self.__init__(platforms, player, clock, traps, coins, monsters, up_down_monsters, block_pos)


    def update(self):
        self.player.update(self.platforms, self.traps, self.coins, self.finish_line, self.monsters, self.up_down_monsters, self.clock)
        
        # Check for game over condition
        if not self.player.can_move and player.level_complete == False:
            self.game_over = True
     
        # Update coin count
        self.coin_count = self.initial_coins_len - len(self.coins) 

        
    def draw(self, canvas):
        draw_image(canvas, self.lvl4_bg, 450, 300, 900, 600)
        self.update()
        
        self.clock.tick()
        if self.clock.transition(10):
            self.player.next_frame()

        self.player.draw(canvas)

        if not self.game_over:
            self.pause_btn = draw_button(canvas, self.pause_btn_img, 30, 20, 50, 50)
            if self.coin_count == self.initial_coins_len:
                canvas.draw_image(self.finish_line, (self.finish_line.get_width()/2, self.finish_line.get_height()/2), 
                                  (self.finish_line.get_width(), self.finish_line.get_height()), (63, 150), 
                                  (self.finish_line.get_width()/5, self.finish_line.get_height()/5)) 

        for platform in self.platforms:
            platform.draw(canvas)
        for trap in self.traps:
            trap.draw(canvas)
        for coin in self.coins:
            coin.draw(canvas)
        for monster in self.monsters:
            monster.draw(canvas)
            monster.update()
        for monster in self.up_down_monsters:
            monster.draw(canvas)
            monster.update()        
   
        
        # Draw coin count
        canvas.draw_text("Coins collected: " + str(self.coin_count) + "/" + str(self.initial_coins_len), (350, 40), 20, "White", "monospace") 
        if self.coin_count != self.initial_coins_len:
            canvas.draw_text("Collect all coins to finish level", (270, 20), 20, "White", "monospace")
        else:
            canvas.draw_text("All coins collected, reach finish line", (255, 20), 20, "White", "monospace")
    
    
        # Draw "Game Over" text if game over
        if self.game_over:
            self.exit_btn = draw_button(canvas, self.exit_btn_img, 255, 420, 500/2, 200/2)
            self.reset_btn = draw_button(canvas, self.reset_btn_img, 555, 420, 500/5, 500/5)
            canvas.draw_image(self.game_over_img, (self.game_over_img.get_width()/2, self.game_over_img.get_height()/2), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()), (450, 200), 
                              (self.game_over_img.get_width(), self.game_over_img.get_height()))
            canvas.draw_text("LOL!!!", (50, 50), 50, "Red", "monospace")
            #game_over_sound.play()
        
        # Draw "Level Complete" text if level complete
        if player.level_complete:
            self.exit_btn = draw_button(canvas, self.exit_btn_img, 255, 420, 500/2, 200/2)
            self.reset_btn = draw_button(canvas, self.reset_btn_img, 555, 420, 500/5, 500/5)
            canvas.draw_image(self.level_complete_img, (self.level_complete_img.get_width()/2, self.level_complete_img.get_height()/2), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()), (450, 260), 
                              (self.level_complete_img.get_width(), self.level_complete_img.get_height()))
            #canvas.draw_text("Level Complete", (260, 230), 80, "Red", "monospace")
    
    def drawTWO(self, canvas):
        self.paused_screen = draw_image(canvas, self.paused_screen_img, 450, 300, 900, 600)
        self.play_btn = draw_button(canvas, self.play_btn_img, 500, 450, 250, 100)
        self.exit_btn = draw_button(canvas, self.exit_btn_img, 150, 450, 250, 100)

    def reset_game(self):
        # Reset player attributes
        self.player.reset(self.block_pos)
        # Reset other objects
        self.coins = [
            Coin((400, 480), 20, 3),
            Coin((670,530), 20, 3),
            Coin((860,430), 20, 3),
            Coin((788, 325), 20, 3),
            Coin((850, 220), 20, 3),
        ]
        #self.monsters.reset(self.pos, self.radius, self.width, self.original_x, self.speed)
        #self.up_down_monsters.reset(self, pos, radius, width, original_y, speed)
        # Reset the Interaction object itself
        self.reset(self.platforms, self.player, self.clock, self.traps, self.coins, self.monsters, self.up_down_monsters, self.block_pos)

    def handle_mouse_click(self, pos, frame, draw, drawTWO):
        if self.pause_btn.is_clicked(pos):
            frame.set_draw_handler(drawTWO)     
        if self.exit_btn is not None and self.exit_btn.is_clicked(pos):
            self.reset_game()  # Reset the game
            import levels
            frame.set_draw_handler(levels.draw)
            frame.set_mouseclick_handler(lambda pos: levels.click(pos, frame))      
        if self.reset_btn is not None and self.reset_btn.is_clicked(pos):
            self.reset_game()
        if self.play_btn is not None and self.play_btn.is_clicked(pos):
            frame.set_draw_handler(draw)

            

platforms = [
    Platform((235,563), 130, 30),
    Platform((330, 506), 140, 30),
    Platform((520, 555), 300, 30),
    Platform((835, 455), 50, 30),
    Platform((763, 350), 50, 30),
    Platform((0, 280), 650, 30),
    Platform((38, 175), 50, 30),
    Platform((830,250), 50, 30)  
]


block_pos = Vector(30, 540)

player = Player(block_pos, sprite)

traps = [
    Trap(8, (385,600), 39, 40),
    Trap(4, (840,600), 39, 40)  
]

coins = [
    Coin((400, 480), 20, 3),
    Coin((670,530), 20, 3),
    Coin((860,430), 20, 3),
    Coin((788, 325), 20, 3),
    Coin((850, 220), 20, 3),
]

monsters = [
    Monster((150,566),  100, 150, 2),
    Monster((450, 480),  100, 430, 2),
    Monster((540,519),  100, 540, 2)
]

up_and_down_monsters = [
    Up_down_monster((660, 450), 25, 140, 450, 1),
    Up_down_monster((735, 370), 25, 180, 450, 1),
    Up_down_monster((576,170), 25, 180, 170, 1),
    Up_down_monster((453, 170), 25, 180, 170, 1),
    Up_down_monster((330,170), 25, 140, 170, 1),
    Up_down_monster((255, 90), 25, 180, 170, 1) 
]

clock = Clock()

i = Interaction(platforms, player, clock, traps, coins, monsters, up_and_down_monsters, block_pos)

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
