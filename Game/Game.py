import pygame
import sys
import os

# Initialize Pygame
def init():
    pygame.init()
    pygame.mixer.init()

init()

# Create the game window
screen_width, screen_height = 992, 496
screen = pygame.display.set_mode((screen_width, screen_height))  # Set the display window size
clock = pygame.time.Clock()  # Create a clock object to control frame rate

def start():  # Start menu screen

    class Button:
        def __init__(self, image_path, pos, scale=(2.0, 2.0)):
            # Load and scale the default image
            self.image_default = pygame.image.load(image_path).convert_alpha()
            self.image_default = pygame.transform.scale(
                self.image_default, 
                (int(self.image_default.get_width() * scale[0]), 
                 int(self.image_default.get_height() * scale[1]))
            )
            
            self.image_clicked = self.load_clicked_image(image_path, scale)
            self.image = self.image_default  # Start with the default image
            self.rect = self.image.get_rect(center=pos)
            self.clicked = False

        def load_clicked_image(self, image_path, scale):
            # Change '1' to '2' in the filename to get the clicked image
            base, ext = os.path.splitext(image_path)
            if base.endswith('1'):
                clicked_image_path = base[:-1] + '2' + ext
            else:
                # If filename does not follow expected pattern, return default image
                clicked_image_path = image_path
            
            # Load, scale, and return the clicked image
            clicked_image = pygame.image.load(clicked_image_path).convert_alpha()
            clicked_image = pygame.transform.scale(
                clicked_image, 
                (int(clicked_image.get_width() * scale[0]), 
                 int(clicked_image.get_height() * scale[1]))
            )
            return clicked_image

        def draw(self, surface):
            # Draw the button with the appropriate image
            surface.blit(self.image, self.rect.topleft)

        def is_clicked(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image = self.image_clicked  # Switch to clicked image
                    self.clicked = True
                    return True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.clicked:
                    self.image = self.image_default  # Revert to default image
                    self.clicked = False
            return False

    pygame.display.set_caption('Rusty Ridge Ranch')

    # Load parallax background layers in order from nearest to farthest
    front_bg = pygame.image.load('Images/Menu/Parallax/Front.png').convert_alpha()  # Nearest foreground layer
    mid_bg = pygame.image.load('Images/Menu/Parallax/Mid.png').convert_alpha()  # Middle background layer
    far_bg = pygame.image.load('Images/Menu/Parallax/Far.png').convert_alpha()  # Farthest background layer
    close_clouds = pygame.image.load('Images/Menu/Parallax/Close_clouds.png').convert_alpha()  # Close clouds layer
    far_clouds = pygame.image.load('Images/Menu/Parallax/Far_clouds.png').convert_alpha()  # Far clouds layer

    # Get the dimensions of each image
    bg_width, bg_height = front_bg.get_size()

    # Initialize positions for parallax layers
    front_bg_x = 0
    mid_bg_x = 0
    far_bg_x = 0
    close_clouds_x = 0
    far_clouds_x = 0

    # Set scroll speeds for each layer (slower for layers farther away)
    scroll_speed_front_bg = 1
    scroll_speed_mid_bg = 0.69
    scroll_speed_far_bg = 0.4
    scroll_speed_close_clouds = 0.25
    scroll_speed_far_clouds = 0.1

    # Center positions for the buttons
    button_y_spacing = 120  # Vertical spacing between buttons
    center_x = screen_width // 2  # Horizontal center of the screen
    start_y = screen_height // 2 - button_y_spacing  # Start button position

    # Create Button instances using the file paths and larger scale
    play_button = Button('Images/Menu/Buttons/Start1.png', (center_x, start_y), scale=(2.0, 2.0))
    options_button = Button('Images/Menu/Buttons/Options1.png', (center_x, start_y + button_y_spacing), scale=(2.0, 2.0))
    quit_button = Button('Images/Menu/Buttons/Quit1.png', (center_x, start_y + 2 * button_y_spacing), scale=(2.0, 2.0))

    # Correct the horizontal center of each button individually
    play_button.rect.centerx = center_x
    options_button.rect.centerx = center_x - 14
    quit_button.rect.centerx = center_x - 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check if any button is clicked
            if play_button.is_clicked(event):
                play()  # Start the game
            if options_button.is_clicked(event):
                print("Options button clicked")
            if quit_button.is_clicked(event):
                print("Quit button clicked")
                pygame.quit()
                sys.exit()

        # Update positions for parallax layers
        front_bg_x -= scroll_speed_front_bg
        mid_bg_x -= scroll_speed_mid_bg
        far_bg_x -= scroll_speed_far_bg
        close_clouds_x -= scroll_speed_close_clouds
        far_clouds_x -= scroll_speed_far_clouds

        # Wrap around the background images when they move off-screen
        if front_bg_x <= -bg_width:
            front_bg_x = 0
        if mid_bg_x <= -bg_width:
            mid_bg_x = 0
        if far_bg_x <= -bg_width:
            far_bg_x = 0
        if close_clouds_x <= -bg_width:
            close_clouds_x = 0
        if far_clouds_x <= -bg_width:
            far_clouds_x = 0

        # Draw the background layers with parallax effect
        screen.blit(far_clouds, (far_clouds_x, 0))
        screen.blit(far_clouds, (far_clouds_x + bg_width, 0))

        screen.blit(close_clouds, (close_clouds_x, 0))
        screen.blit(close_clouds, (close_clouds_x + bg_width, 0))

        screen.blit(far_bg, (far_bg_x, 0))
        screen.blit(far_bg, (far_bg_x + bg_width, 0))

        screen.blit(mid_bg, (mid_bg_x, 0))
        screen.blit(mid_bg, (mid_bg_x + bg_width, 0))

        # Apply a semi-transparent overlay to dim the front background
        overlay = pygame.Surface((bg_width, bg_height))
        overlay.set_alpha(150)  # Adjust transparency (0: fully transparent, 255: fully opaque)
        overlay.fill((0, 0, 0))  # Black overlay
        screen.blit(front_bg, (front_bg_x, 0))
        screen.blit(front_bg, (front_bg_x + bg_width, 0))
        screen.blit(overlay, (0, 0))

        # Draw buttons on the screen
        play_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.update()  # Update the display
        clock.tick(165)  # Limit frame rate to 165 FPS

def esc():  # In-game menu screen
    pass

def play():  # Play screen
    # Define a Player class for handling player movement
    class Player(pygame.sprite.Sprite):
        def __init__(self, pos, scale=1.5):  # Added scale parameter
            super().__init__()
            self.scale = scale  # Store the scale factor
            self.images = {
                'standing_right': pygame.transform.scale(
                    pygame.image.load('Images/Sprites/Player/Player_Standing_Right.png').convert_alpha(), 
                    (int(pygame.image.load('Images/Sprites/Player/Player_Standing_Right.png').get_width() * scale), 
                     int(pygame.image.load('Images/Sprites/Player/Player_Standing_Right.png').get_height() * scale))
                ),
                'jogging_right_1': pygame.transform.scale(
                    pygame.image.load('Images/Sprites/Player/Player_Jogging_Right1.png').convert_alpha(), 
                    (int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right1.png').get_width() * scale), 
                     int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right1.png').get_height() * scale))
                ),
                'jogging_right_2': pygame.transform.scale(
                    pygame.image.load('Images/Sprites/Player/Player_Jogging_Right2.png').convert_alpha(), 
                    (int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right2.png').get_width() * scale), 
                     int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right2.png').get_height() * scale))
                ),
                'standing_left': pygame.transform.flip(pygame.transform.scale(
                    pygame.image.load('Images/Sprites/Player/Player_Standing_Right.png').convert_alpha(), 
                    (int(pygame.image.load('Images/Sprites/Player/Player_Standing_Right.png').get_width() * scale), 
                     int(pygame.image.load('Images/Sprites/Player/Player_Standing_Right.png').get_height() * scale))
                ), True, False),
                'jogging_left_1': pygame.transform.flip(pygame.transform.scale(
                    pygame.image.load('Images/Sprites/Player/Player_Jogging_Right1.png').convert_alpha(), 
                    (int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right1.png').get_width() * scale), 
                     int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right1.png').get_height() * scale))
                ), True, False),
                'jogging_left_2': pygame.transform.flip(pygame.transform.scale(
                    pygame.image.load('Images/Sprites/Player/Player_Jogging_Right2.png').convert_alpha(), 
                    (int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right2.png').get_width() * scale), 
                     int(pygame.image.load('Images/Sprites/Player/Player_Jogging_Right2.png').get_height() * scale))
                ), True, False)
            }
            self.image = self.images['standing_right']
            self.rect = self.image.get_rect(center=pos)
            self.speed = 1
            self.animation_frame = 0
            self.jogging = False
            self.facing_left = False

        def update(self):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                self.jogging = True
                self.animation_frame += 1

                # Switch between jogging frames
                if self.animation_frame // 25 % 2 == 0:
                    if self.facing_left:
                        self.image = self.images['jogging_left_1']
                    else:
                        self.image = self.images['jogging_right_1']
                else:
                    if self.facing_left:
                        self.image = self.images['jogging_left_2']
                    else:
                        self.image = self.images['jogging_right_2']

                # Move player
                if keys[pygame.K_a]:
                    self.rect.x -= self.speed  # Move left
                    self.facing_left = True
                if keys[pygame.K_d]:
                    self.rect.x += self.speed  # Move right
                    self.facing_left = False
                if keys[pygame.K_w]:
                    self.rect.y -= self.speed  # Move up
                if keys[pygame.K_s]:
                    self.rect.y += self.speed  # Move down
            else:
                self.jogging = False
                if self.facing_left:
                    self.image = self.images['standing_left']
                else:
                    self.image = self.images['standing_right']

    # Define a CameraGroup to follow the player
    class CameraGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()
            self.display_surface = pygame.display.get_surface()
            self.offset = pygame.math.Vector2(0, 0)
            self.half_w = self.display_surface.get_size()[0] // 2
            self.half_h = self.display_surface.get_size()[1] // 2
            self.ground_surf = pygame.image.load('Images/Map/Ground.png').convert_alpha()
            self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

            # Map dimensions (change these to your actual map size)
            self.map_width = self.ground_rect.width
            self.map_height = self.ground_rect.height

        def custom_draw(self, player):
            # Update the camera offset based on the player's position
            self.offset.x = player.rect.centerx - self.half_w
            self.offset.y = player.rect.centery - self.half_h

            # Clamp the offset to ensure the camera does not go out of the map bounds
            self.offset.x = max(0, min(self.offset.x, self.map_width - self.display_surface.get_width()))
            self.offset.y = max(0, min(self.offset.y, self.map_height - self.display_surface.get_height()))

            # Draw the ground with the current offset
            ground_offset_pos = self.ground_rect.topleft - self.offset
            self.display_surface.blit(self.ground_surf, ground_offset_pos)

            # Draw all sprites in the group with the current offset
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    # Create instances of Player and CameraGroup
    player = Player((screen_width // 2, screen_height // 2))
    camera_group = CameraGroup()
    camera_group.add(player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update player and draw everything
        camera_group.update()
        camera_group.custom_draw(player)

        pygame.display.update()  # Update the display
        clock.tick(165)  # Limit frame rate to 165 FPS

# Start screen
start()