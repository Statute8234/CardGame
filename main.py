import pygame
import numpy as np
import random, sys, time

pygame.init()
current_time = time.time()
random.seed(current_time)
# Seting up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# color
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
PURPLE = (255, 0, 255)

# buttons
class Button:
    def __init__(self, x, y, width, height, text, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.color = self.active_color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                    self.color = self.active_color
        else:
            self.color = self.inactive_color
        self.textColor = self.color
            
    def reset(self):
        self.clicked = False
        self.color = self.inactive_color
        
# attributes
class Attributes:
    def __init__(self, x, y, width, height, text, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        text_surface = self.font.render(self.text, True, self.textColor)
        text_x = self.x + (self.width - text_surface.get_width()) / 2
        text_y = self.y + (self.height - text_surface.get_height()) / 2
        screen.blit(text_surface, (text_x, text_y))

# cards
class Cards(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, image_path, border_thickness):
        super().__init__()
        self.x = x
        self.original_y = y
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color_value = 0
        self.border_color = self.get_random_color_with_probability()
        self.border_thickness = border_thickness
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)
        self.clicked = False
        self.values = []

    def get_random_color_with_probability(self):
        colors_with_probabilities = {
            PURPLE: 10,
            RED: 20,
            GREEN: 30,
            BLUE: 40,
        }
        total_probability = sum(colors_with_probabilities.values())
        normalized_probabilities = {color: (prob / total_probability) for color, prob in colors_with_probabilities.items()}
        rand = random.random()
        # Determine which color this random number corresponds to
        cumulative_probability = 0.0
        for color, prob in normalized_probabilities.items():
            cumulative_probability += prob
            if rand < cumulative_probability:
                self.color_value = prob 
                return color
        return WHITE

    def inverse_scale(self, x, x_min, x_max, y_min, y_max):
        if x < x_min or x > x_max:
            return -1
        else:
            scale = (y_min - y_max) / (x_max - x_min)
            y = y_min - scale * (x - x_min)
            return y
        
    def add_attributes(self):
        if len(self.values) == 0:
            for _ in range(3):
                value = self.inverse_scale(self.color_value, 0.1, 0.4, 100, 10)
                max_value = min(100, round(value) + 5)
                self.values.append(random.randint(round(value) - 5, max_value))
        self.healthAttributes = Attributes(self.x + 5,self.y + 5,30,30,str(self.values[0]),r"Assets\heart.png")
        self.healthAttributes.draw(screen)
        self.shieldAttributes = Attributes(self.x + self.width - 35,self.y + 5,30,30,str(self.values[1]),r"Assets\shield.png")
        self.shieldAttributes.draw(screen)
        self.swordsAttributes = Attributes(self.x + 5,self.y + self.height - 35,30,30,str(self.values[2]),r"Assets\swords.png")
        self.swordsAttributes.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color, (self.x - self.border_thickness, self.y - self.border_thickness, self.width + (self.border_thickness * 2), self.height + (self.border_thickness * 2)), self.border_thickness) # draw border
        screen.blit(self.image, (self.x, self.y)) # draw image
        text_surface = self.font.render(self.text, True, self.textColor)
        text_x = self.x + (self.width - text_surface.get_width()) / 2
        text_y = self.y + (self.height - text_surface.get_height()) / 2
        screen.blit(text_surface, (text_x, text_y))
        self.add_attributes()

    def handle_event(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_over = self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height
        if mouse_over:
            if not self.clicked:
                self.y = self.original_y - 10
            # move the card
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = not self.clicked
                if self.clicked:
                    self.y = self.original_y / 1.55
                else:
                    self.y = self.original_y
        else:
            if not self.clicked:
                self.y = self.original_y
    
# Deck of acrds
class CardDeck:
    def __init__(self, x, y, width, height, text, image_path):
        self.x = x
        self.original_y = y
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)
        self.clicked = False
        self.card_spacing = 120
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y)) # draw image
        text_surface = self.font.render(self.text, True, self.textColor)
        text_x = self.x + (self.width - text_surface.get_width()) / 2
        text_y = self.y + (self.height - text_surface.get_height()) / 2
        screen.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        global amount, max_amount
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            if not self.clicked:
                if self.y != self.original_y - 10:
                    self.y -= 10
            # draw a card
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = not self.clicked
                if len(player_list) < 5 and amount > 0:
                    amount -= 1
                    player_list.add(Cards((len(player_list) * self.card_spacing) + 140,400,100,125,"Test",r"Assets\cardFront.png", 2))
                    self.text = f"{amount}/{max_amount}"
                    all_sprites.add(player_list)
        else:
            self.y = self.original_y

all_sprites = pygame.sprite.Group()
player_list = pygame.sprite.Group()
amount, max_amount = 50, 50
cardDeck = CardDeck(10,400,100,125,f"{amount}/{max_amount}",r"Assets\cardBack.png")
all_sprites.add(player_list)
endTurn = Button(WIDTH / 2, HEIGHT - 50, 100, 25, "End Turn", RED, BLACK)
# display
class PlayerDisplay:
    def __init__(self, x, y, width, height, text, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        text_surface = self.font.render(self.text, True, self.textColor)
        text_x = self.x + (self.width - text_surface.get_width()) / 2
        text_y = self.y + (self.height - text_surface.get_height()) / 2
        screen.blit(text_surface, (text_x, text_y))
Player_health = 100
playerDisplay = PlayerDisplay(10,540,50,50,f"{Player_health}",r"Assets\heart.png")
# This is running the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            sys.exit()
            quit()
        cardDeck.handle_event(event)
        for card in all_sprites:
            card.handle_event(event)
        endTurn.handle_event(event)
        if endTurn.clicked:
            for card in player_list:
                if card.clicked:
                    player_list.remove(card)
    screen.fill(WHITE)
    # draw elements
    cardDeck.draw(screen)
    playerDisplay.draw(screen)
    all_sprites.update()
    for card in all_sprites:
        card.draw(screen)
    endTurn.draw(screen)
    # This is to update the scene
    clock.tick(64)
    pygame.display.flip()
    pygame.display.update()