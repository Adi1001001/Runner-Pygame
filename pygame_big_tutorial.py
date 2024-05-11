import pygame
from random import randint, choice

from pygame.sprite import Group

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Runner/graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Runner/graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Runner/graphics/player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Runner/audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('Runner/graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Runner/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('Runner/graphics/Snail/Snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Runner/graphics/Snail/Snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}',False,('Purple'))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return current_time

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    # play a walking animation when player is on the floor
    # play the jump surface when player is not on the floor
    global player_surf, player_index
    if player_rectangle.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

start_time = 0

# set up
pygame.init()
# size of the window
screen = pygame.display.set_mode((800,400))

# naming the window
pygame.display.set_caption('Runner')

# setting up the frame rate
clock = pygame.time.Clock()

# creating a text preset
test_font = pygame.font.Font('Runner/font/Pixeltype.ttf',50)

# creating the different game states
game_active = False

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# creating background music
bg_music = bg_sound = pygame.mixer.Sound('Runner/audio/music.wav')
bg_sound.set_volume(0.1)
bg_sound.play(loops = -1)
    

# setting up the different aspects of the object
sky_surface = pygame.image.load('Runner/graphics/Sky.png').convert()
ground_surface = pygame.image.load('Runner/graphics/Ground.png').convert() 
# setting up a text surface
#score_surface = test_font.render('My game', False, (64,64,64))
#score_rectangle = score_surface.get_rect(center = (400,50))
# setting up an animation
snail_frame_1 = pygame.image.load('Runner/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Runner/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('Runner/graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Runner/graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

snail_rectangle = snail_surface.get_rect(bottomright = (750,300))
# setting up an animation
player_walk_1 = pygame.image.load('Runner/graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Runner/graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('Runner/graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]

player_rectangle = player_walk_1.get_rect(midbottom = (80,300))

# setting up the gravity variables
player_gravity = 0

# creating menu surfaces
player_menu = pygame.image.load('Runner/graphics/player/player_stand.png').convert_alpha()
# transforming a surface
player_menu = pygame.transform.rotozoom(player_menu,0,2).convert_alpha()
player_menu_rect = player_menu.get_rect(center = (400,200))

menu_toptext = test_font.render('Pixel Runner', False, 'Purple')
menu_toptext_rect = menu_toptext.get_rect(center = (400,80))

menu_bottomtext = test_font.render('Click space to start', False, 'Purple')
menu_bottomtext_rect = menu_toptext.get_rect(center = (400,350))

score = 0

# creating enemy spawn logic
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
obstacle_rect_list = []

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

#game loop
while True:
    # setting up the exit of the window and game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos):
                        player_gravity = -20

            # getting keyboard inputs in the most optimal way
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
            #    if randint(0,2):
            #        obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100),300)))
            #    else:
            #        obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1000), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rectangle.left = 800
                    start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # position of the object
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        score = display_score()

        #pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        #pygame.draw.line(screen, 'Pink', (0,0), (800,400))
        #screen.blit(score_surface, (score_rectangle))

        # making the jumping and falling mechanics
        #player_gravity += 1
        #player_rectangle.y += player_gravity
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # creating an animation
        #snail_rectangle.right -= 4
        #if snail_rectangle.right < -100:
        #    snail_rectangle.right = 850
        #screen.blit(snail_surface, (snail_rectangle))

        # creating a floor
        #if player_rectangle.bottom >= 300:
        #    player_rectangle.bottom = 300
        #player_animation()
        #screen.blit(player_surf, (player_rectangle))

        #if player_rectangle.colliderect(snail_rectangle):
        #    game_active = False

        #game_active = collisions(player_rectangle,obstacle_rect_list)
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_menu,player_menu_rect)
        screen.blit(menu_toptext,menu_toptext_rect)

        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your Score: {int(score)}', False, 'Purple')
        score_message_rect = score_message.get_rect(center = (350,350))

        if score == 0:
            screen.blit(menu_bottomtext,menu_bottomtext_rect)
        else:
            screen.blit(score_message,score_message_rect)

    # updating the display
    pygame.display.update()

    # 60 frame rate maximum
    clock.tick(60)