import pygame, random

pygame.init()
pygame.mixer.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rock, Paper, Scissors")

WHITE = (255, 255, 255)
RED = (255, 128, 128)
YELLOW = (255, 200, 15)
GREEN_WIN = (0, 255, 0)
RED_LOOSE = (255, 0, 250)

rock_button_img = pygame.image.load('rock_button.png').convert_alpha()
paper_button_img = pygame.image.load('paper_button.png').convert_alpha()
scissors_button_img = pygame.image.load('scissors_button.png').convert_alpha()

bg_image = pygame.image.load("bg.png")
rock_img = pygame.image.load("rock.png")
paper_img = pygame.image.load("paper.png")
scissors_img = pygame.image.load("scissors.png")

rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))


choices = ["rock", "paper", "scissors"]
player_score = 0
computer_score = 0

def display_choice(choice, x, y, angle=0, flip=False):
    rotated_img = pygame.transform.rotate(choice_img[choice], angle)
    if flip:
        rotated_img = pygame.transform.flip(rotated_img, True, False)
    screen.blit(rotated_img, (x, y))

def find_winner(player, computer):
    if player == computer:
        return "Draw"
    
    beats = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }
    
    if beats[player] == computer:
        return "Player wins!"
    else:
        return "Computer wins!"

class Button:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (150, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                button_click_sound.play() 
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

rock_button = Button(100, 500, rock_button_img)
paper_button = Button(350, 500, paper_button_img)
scissors_button = Button(600, 500, scissors_button_img)

choice_img = {
    "rock": rock_img,
    "paper": paper_img,
    "scissors": scissors_img
}

running = True
player_choice = None
computer_choice = None
result = None

animation_phase = 0
player_animation_angle = 0
computer_animation_angle = 0
player_animation_clockwise = True
computer_animation_clockwise = True
animation_timer = pygame.time.get_ticks()

def update_animation_phase(angle, clockwise, phase):
    if clockwise:
        angle -= 30
        if angle <= -30:
            clockwise = False
    else:
        angle += 30
        if angle >= 0:
            clockwise = True
            phase += 1
    return angle, clockwise, phase

pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  
pygame.mixer.music.set_volume(0.5)  

button_click_sound = pygame.mixer.Sound('button_click.mp3')

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rock_button.draw(screen):
                player_choice = "rock"
            elif paper_button.draw(screen):
                player_choice = "paper"
            elif scissors_button.draw(screen):
                player_choice = "scissors"
            
            if player_choice:
                player_animation_angle = 0
                computer_animation_angle = 0
                player_animation_clockwise = True
                computer_animation_clockwise = True
                animation_phase = 0

                computer_choice = random.choice(choices)
                
                result = find_winner(player_choice, computer_choice)
                if result == "Player wins!":
                    player_score += 1
                    
                elif result == "Computer wins!":
                    computer_score += 1
                    

    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(bg_image, (0, 0))
    rock_button.draw(screen)
    paper_button.draw(screen)
    scissors_button.draw(screen)

    font = pygame.font.Font(None, 36)
    player_label = font.render("Player", True, WHITE)
    computer_label = font.render("Computer", True, WHITE)
    
    screen.blit(player_label, (150, 50))
    screen.blit(font.render(str(player_score), True, WHITE), (185, 90))
    screen.blit(computer_label, (575, 50))
    screen.blit(font.render(str(computer_score), True, WHITE), (625, 90))

    if player_choice:
        if animation_phase < 6:
            display_choice('rock', 110, 200, player_animation_angle)
            display_choice('rock', 550, 200, computer_animation_angle, flip=True)
            
            current_time = pygame.time.get_ticks()
            if current_time - animation_timer > 200:
                animation_timer = current_time
                player_animation_angle, player_animation_clockwise, animation_phase = update_animation_phase(player_animation_angle, player_animation_clockwise, animation_phase)
                computer_animation_angle, computer_animation_clockwise, animation_phase = update_animation_phase(computer_animation_angle, computer_animation_clockwise, animation_phase)
        else:
            display_choice(player_choice, 110, 200)
            display_choice(computer_choice, 550, 200, flip=True)

    if animation_phase >= 6 and result:
        if result == "Player wins!":
            result_color = GREEN_WIN
        elif result == "Computer wins!":
            result_color = WHITE
        elif result == "Draw":
            result_color = YELLOW
        else:
            result_color = RED_LOOSE

        result_font = pygame.font.Font(None, 48)
        result_text = result_font.render(result, True, result_color)
        
        text_width = result_text.get_width()
        text_height = result_text.get_height()
        text_x = screen_width // 2 - text_width // 2
        text_y = 350
        pygame.draw.rect(screen, (40,40,40), (text_x - 15, text_y - 15, text_width + 30, text_height + 30))
        pygame.draw.rect(screen, (80,80,80), (text_x - 10, text_y - 10, text_width + 20, text_height + 20))

        screen.blit(result_text, (text_x, text_y))

    pygame.display.flip()

pygame.quit()
