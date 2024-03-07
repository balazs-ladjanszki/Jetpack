import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game")

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (25,70,230)
RED =  (188,39,50)
DARK_GREY = (80,71,81)

FONT = pygame.font.SysFont("comicsans", 30)
TOWER_IMAGE = pygame.image.load("tower-removebg.png")
DRIPSTONE_IMAGE = pygame.image.load("dripstone-removebg.png")
MOUNTAIN_IMAGE = pygame.image.load("mountain-removebg.png")
SKY_IMAGE = pygame.image.load("sky.png")
FOREGROUND_IMAGE = pygame.image.load("foreground3.png")
BAT1_IMG = pygame.image.load("bat1-removebg.png") #lent
BAT2_IMG = pygame.image.load("bat2-removebg.png") #fent
FIREBALL_IMG = pygame.image.load("fireblast-removebg.png")


#<>
class Human:
    TIMESTEP = 0.2
    HUMAN_IMAGE = pygame.image.load("human_nobg.png")
    HUMAN_W_FIRE_IMAGE = pygame.image.load("human_nobg_fire.png")
    def __init__(self):
        self.y_position = 0
        self.x_position = 150
        self.velocity = 0
        self.acceleration = 13
        self.width = 100
        self.height = 100
        self.up = 0
        self.distance = 0
        self.alive = 1
        self.score = 0

    def draw(self):
        if(self.up == 0):
            WIN.blit(self.HUMAN_IMAGE,(self.x_position,self.y_position))
        elif(self.up == 1):
            WIN.blit(self.HUMAN_W_FIRE_IMAGE,(self.x_position,self.y_position))

    def update_position(self):
        self.velocity += self.acceleration*self.TIMESTEP
        self.y_position += self.velocity*self.TIMESTEP
        if(self.y_position >= 700):
            self.y_position = 700
            self.velocity = 0
        elif(self.y_position <= 0):
            self.y_position = 0
            self.velocity = 0
        self.distance += 1
        self.score += 1


class Obstacle:
    
    def __init__(self, x, y, image, background):
        self.x_position = x
        self.y_position = y
        self.height = image.get_height()
        self.width = image.get_width()
        self.image = image
        self.background = background
    

    def update_position(self):
        if(self.background == 0):
            self.x_position = self.x_position-13
        elif(self.background == 1):
            if(self.image == FOREGROUND_IMAGE):
                self.x_position -= 1

    def draw(self):
        WIN.blit(self.image,(self.x_position, self.y_position))


class Fireball:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.height = image.get_height()
        self.width = image.get_width()
        self.image = image
        self.viable = 1
    
    def update_position(self):
        self.x = self.x + 20

    def draw(self):
        if(self.viable == 1):
            WIN.blit(self.image, (self.x, self.y))

class Text():
    plus50 = FONT.render("+50", 20, WHITE)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update_position(self):
        self.y -= 12
        self.x -= 13

    def draw(self):
        WIN.blit(self.plus50,(self.x, self.y))


class Monster:
    BAT1_IMG = pygame.image.load("bat1-removebg.png") #wings down
    BAT2_IMG = pygame.image.load("bat2-removebg.png") #wings up

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wings = 1
        self.viable = 1

    def update_position(self, distance):
        self.x = self.x - 13
        if(distance % 15 == 0):
            if(self.wings == 1):
                self.wings = 0
            elif(self.wings == 0):
                self.wings = 1

    def draw(self, distance):
        if(self.viable == 1):
            if(self. wings == 1):
                WIN.blit(self.BAT1_IMG, (self.x-53, self.y))
            elif(self. wings == 0):
                WIN.blit(self.BAT2_IMG, (self.x, self.y))

class Coin:
    COIN1 = pygame.image.load("coin1.png")
    COIN2 = pygame.image.load("coin2.png")
    COIN3 = pygame.image.load("coin3.png")
    COIN4 = pygame.image.load("coin4.png")
    COIN5 = pygame.image.load("coin5.png")
    COIN6 = pygame.image.load("coin6.png")
    COIN7 = pygame.image.load("coin7.png")
    COIN8 = pygame.image.load("coin8.png")

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.currentcoin = 1
        self.width = 120
        self.height = 120
        self.viable = 1

    def update(self, distance):
        self.x -= 13
        if(distance % 4 == 0):
            if(self.currentcoin == 8):
                self.currentcoin = 1
            else:
                self.currentcoin += 1

    def draw(self):
        if(self.viable == 1):
            if(self.currentcoin == 1):
                WIN.blit(self.COIN1, (self.x, self.y))
            elif(self.currentcoin == 2):
                WIN.blit(self.COIN2, (self.x, self.y))
            elif(self.currentcoin == 3):
                WIN.blit(self.COIN3, (self.x, self.y))
            elif(self.currentcoin == 4):
                WIN.blit(self.COIN4, (self.x, self.y))
            elif(self.currentcoin == 5):
                WIN.blit(self.COIN5, (self.x, self.y))
            elif(self.currentcoin == 6):
                WIN.blit(self.COIN6, (self.x, self.y))
            elif(self.currentcoin == 7):
                WIN.blit(self.COIN7, (self.x, self.y))
            elif(self.currentcoin == 8):
                WIN.blit(self.COIN8, (self.x, self.y))


class Game:

    def __init__(self) -> None:
        pass

    def Create_Fireball(self, player):
        fireball = Fireball(player.x_position, player.y_position+30, FIREBALL_IMG)
        return fireball



    #We crate obstacles based on the player's position
    def CreateObstacle(self, position): 
        obstacle = None
        monster = None
        coin = None
        value = random.randint(1,10)
        coin_num = random.randint(1,100)
        adjustment = random.randint(1,300)
        if(position >= 400):
            if(value <= 5):
                obstacle = Obstacle(1300-adjustment,330, TOWER_IMAGE,0)
                if(coin_num <= 50):
                    coin = Coin(1300, 0 + adjustment)
            elif(value < 8):
                obstacle = Obstacle(1300- adjustment,0, DRIPSTONE_IMAGE,0)
                if(coin_num <= 50):
                    coin = Coin(1300, 400 + adjustment)
            else:
                monster = Monster(1300- adjustment,400)
                if(coin_num <= 50):
                    coin = Coin(1300, 0 + adjustment)
        else:
            if(value <= 5):
                obstacle = Obstacle(1300- adjustment,0, DRIPSTONE_IMAGE,0)
                if(coin_num <= 50):
                    coin = Coin(1300, 400 + adjustment)
            elif(value < 8):
                obstacle = Obstacle(1300- adjustment,330, TOWER_IMAGE,0)
                if(coin_num <= 50):
                    coin = Coin(1300, 0 + adjustment)
            else:
                monster = Monster(1300 - adjustment,250)
                if(coin_num <= 50):
                    coin = Coin(1300, 250 + adjustment)

        return [obstacle, monster, coin]
    
    def checkCollision(self, player, obstacles, fireballs, monsters, texts, coins):
        player_box = pygame.Rect(player.x_position+10,player.y_position+10, player.width - 20, player.height - 20)

        for obstacle in obstacles:
            obstacle_box = None
            #Checking for Human and obstacle collision
            if(obstacle.background == 0):
                if(obstacle.image == TOWER_IMAGE):
                    obstacle_box = pygame.Rect(obstacle.x_position + 130, obstacle.y_position + 80, 200, 420)
                    #pygame.draw.rect(WIN, WHITE, (obstacle.x_position + 130, obstacle.y_position + 80, 200, 420),2)
                if(obstacle.image == DRIPSTONE_IMAGE):
                    obstacle_box = pygame.Rect(obstacle.x_position + 50, obstacle.y_position, obstacle.width - 100, obstacle.height)
                    #pygame.draw.rect(WIN, WHITE, (obstacle.x_position + 50, obstacle.y_position, obstacle.width - 100, obstacle.height), 2)
                collision = obstacle_box.colliderect(player_box)
                if(collision):
                    return 1
            #Checking for fireball and obstacle collision
                for fireball in fireballs:
                    fireball_box = pygame.Rect(fireball.x, fireball.y, fireball.width, fireball.height)
                    collision_w_obstacle = fireball_box.colliderect(obstacle_box)
                    if(collision_w_obstacle):
                        fireball.viable = 0
        for fireball in fireballs:
                    fireball_box = pygame.Rect(fireball.x, fireball.y, fireball.width, fireball.height)
                    #Checking for fireball and monster collision
                    for monster in monsters:
                        monster_box = pygame.Rect(monster.x+30, monster.y, 150, 150)
                        #pygame.draw.rect(WIN, WHITE, (monster.x+30, monster.y, 150, 150), 2)
                        collision_w_monster = fireball_box.colliderect(monster_box)
                        if(collision_w_monster):
                            if(monster.viable == 1 and fireball.viable == 1):
                                player.score += 50
                            texts.append(Text(monster.x+50,monster.y+50))
                            monster.viable = 0
                            fireball.viable = 0
            #Checking player and monster collision
        for monster in monsters:
                    monster_box = pygame.Rect(monster.x+30, monster.y, 150, 150)
                    collision = monster_box.colliderect(player_box)
                    if(collision):
                        return 1
            #Checking player and coi collision
        for coin in coins:
                    coin_box = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
                    collision = coin_box.colliderect(player_box)
                    if(collision):
                        if(coin.viable == 1):
                            player.score += 50
                            texts.append(Text(coin.x+50,coin.y+50))
                        coin.viable = 0

                    

            
    def restart(self, player):
        player.y_position = 0
        player.x_position = 150
        player.velocity = 0
        player.acceleration = 13
        player.width = 100
        player.height = 100
        player.up = 0
        player.distance = 0
        player.alive = 1
        player.score = 0

    def backgroundElements(self, distance):
        b_elements = []
        if(distance == 0):
            b_elements.append(Obstacle(0,0,FOREGROUND_IMAGE,1))
        if(distance % 3641 == 0):
            b_elements.append(Obstacle(3641,0,FOREGROUND_IMAGE,1))
        
        
        return b_elements


def main():
    run = True
    clock = pygame.time.Clock()
    player = Human()
    map = Game()
    obstacles = []
    fireballs = []
    monsters = []
    texts = []
    coins = []

    def on_mouse_button_down(event):
        player.acceleration = -20
        player.up = 1
    def on_mouse_button_up(event):
        player.acceleration = 13
        player.up = 0
    def on_space_down(event):
        fireballs.append(map.Create_Fireball(player))


    while run:
        clock.tick(60)

        if(player.alive == 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    on_mouse_button_down(event)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    on_mouse_button_up(event)
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        on_space_down(event)

            if(player.distance % 60 == 0 and player.distance != 0):
                new_obstacle = map.CreateObstacle(player.y_position)
                if(new_obstacle[0] != None):
                    obstacles.append(new_obstacle[0])
                elif(new_obstacle[1] != None):
                    monsters.append(new_obstacle[1])
                if(new_obstacle[2] != None):
                    coins.append(new_obstacle[2])
            
            background = map.backgroundElements(player.distance)
            for element in background:
                obstacles.append(element)

            for obstacle in obstacles:
                obstacle.update_position()
                obstacle.draw()

            for fireball in fireballs:
                fireball.update_position()
                fireball.draw()

            for text in texts:
                text.update_position()
                text.draw()

            for monster in monsters:
                monster.update_position(player.distance)
                monster.draw(player.distance)

            for coin in coins:
                coin.update(player.distance)
                coin.draw()

            for obstacle in obstacles:
                if(obstacle.x_position < -3641):
                    obstacles.pop(obstacles.index(obstacle))

            for fireball in fireballs:
                if(fireball.x > 1200 or fireball.viable == 0):
                    fireballs.pop(fireballs.index(fireball))
            
            for monster in monsters:
                if(monster.x < -1400 or monster.viable == 0):
                    monsters.pop(monsters.index(monster))

            for coin in coins:
                if(coin.x < -1200 or coin.viable == 0):
                    coins.pop(coins.index(coin))




            player.update_position()
            player.draw()
            score = FONT.render(str(player.score), 8, WHITE)
            WIN.blit(score,(900,100))

            if(map.checkCollision(player,obstacles,fireballs, monsters, texts, coins) == 1):
                player.alive = 0
        else:
            gameover_text = FONT.render("GAME OVER", 20, WHITE)
            restart_text = FONT.render("RESTART", 15, WHITE)
            WIN.blit(gameover_text, (400,300))
            WIN.blit(score, (450,400))
            WIN.blit(restart_text, (400,500))
            restart_box = pygame.draw.rect(WIN, WHITE, (398, 500, 150, 50),2)
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and restart_box.collidepoint(mouse_position):
                    map.restart(player)
                    obstacles = []
                    fireballs = []
                    monsters = []
                    coins = []


        pygame.display.update()

    pygame.quit()
    
main()