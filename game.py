import random
from time import sleep

import pygame
from pathlib2 import Path


class CarRacing:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.root_path = str(Path(__file__).parent)

        self.initialize()

    def initialize(self):

        self.crashed = False

        self.carImg = pygame.image.load(self.root_path + "/img/car.png")
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car = pygame.image.load(self.root_path + "/img/enemy_car_1.png")
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load(self.root_path + "/img/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race -- suppi')
        self.main_menu()

    def main_menu(self):
        menu = True
        while menu:
            self.gameDisplay.fill(self.black)
            self.display_message("Car Racing Game", 64, (self.display_width // 2, self.display_height // 3))

            # Button settings
            button_x, button_y, button_w, button_h = self.display_width // 3, self.display_height // 2, 200, 50
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), [button_x, button_y, button_w, button_h])

            font = pygame.font.SysFont("comicsansms", 32)
            text = font.render("Start", True, self.white)
            self.gameDisplay.blit(text, (button_x + 65, button_y + 10))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # Check if the button is clicked
            if button_x + button_w > mouse[0] > button_x and button_y + button_h > mouse[1] > button_y:
                if click[0] == 1:
                    menu = False
                    self.run_car()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()
            self.clock.tick(15)

    def run_car(self):

        while not self.crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_coordinate -= 50
                    if event.key == pygame.K_RIGHT:
                        self.car_x_coordinate += 50

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.highscore(self.count)
            self.count += 1
            if self.count % 100 == 0:
                self.enemy_car_speed += 1
                self.bg_speed += 1

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!", 72, (self.display_width // 2, self.display_height // 2))

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                self.display_message("Game Over !!!", 72, (self.display_width // 2, self.display_height // 2))

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg, font_size, position):
        font = pygame.font.SysFont("comicsansms", font_size, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (position[0] - text.get_width() // 2, position[1] - text.get_height() // 2))

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks & Regards,", True, self.white)
        self.gameDisplay.blit(text, (600, 520))
        text = font.render("Supriya M", True, self.white)
        self.gameDisplay.blit(text, (600, 540))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
