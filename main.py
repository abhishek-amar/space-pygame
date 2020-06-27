#Import modules
import pygame
import random
import math

# Initialize pygame
pygame.init()

# Global constants
size = (width, height) = (800, 600)
score_value = 0
lives = 20

# Create a window/screen
screen = pygame.display.set_mode(size)

# Application title and icons
pygame.display.set_caption("The Battle Of Tannhauser Gate")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png').convert()

# Font
font = pygame.font.Font("freesansbold.ttf", 32)  # Slow if you do this inside print_font()


class Ship:
    max_health = 100

    def __init__(self, x, y, x_change, y_change, image_path, health):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.health = health

    def draw_image(self):
        screen.blit(self.image, (round(self.x), round(self.y)))

    def print_healthbar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (round(self.x), round(
            self.y) + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(screen, (0, 255, 0), (round(self.x), round(self.y) + self.get_height() +
                                               10, self.get_width() * ((1 - (self.max_health - self.health)/self.max_health)), 10))

    def reduce_health(self):
        self.health -= (self.max_health/5)

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


class Enemy(Ship):
    def __init__(self, x, y, x_change, y_change, image_path, health):
        super().__init__(x, y, x_change, y_change, image_path, health)

    def respawn(self):
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)


class Player(Ship):
    def __init__(self, x, y, x_change, y_change, image_path, health):
        super().__init__(x, y, x_change, y_change, image_path, health)

    def respawn(self):
        self.x = 370
        self.y = 480


class Projectile(Ship):
    def __init__(self, x, y, x_change, y_change, image_path, state, health=None):
        super().__init__(x, y, x_change, y_change, image_path, health)
        self.state = state

    def draw_image(self):
        screen.blit(self.image, (round(self.x), round(self.y)))

    def fire(self, Ship):
        if lives > 0:
            pygame.mixer.Sound('laser.wav').play()
            self.x = Ship.x
            self.y = Ship.y
            self.state = 'Fire'

    def collision_check(self, Ship):
        if lives > 0:
            distance = math.sqrt((Ship.x - self.x)**2 + (Ship.y - self.y)**2)
            if distance < 40:
                pygame.mixer.Sound('explosion.wav').play()
                self.y = 480
                self.state = 'Ready'
                return True
            else:
                return False


# Font render function
def print_font(x, y, msg, r, g, b):
    screen.blit(font.render(msg, True, (r, g, b)), (x, y))


# Background music function
def backrgound_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


# Creating player, enemies and torpedoes
player = Player(370, 480, 0, 0, 'player.png', 100)
enemy1 = Enemy(random.randint(0, 736), random.randint(50, 150), 5, 20, 'enemy.png', 100)
enemy2 = Enemy(random.randint(0, 736), random.randint(50, 150), 5, 20, 'enemy.png', 100)
enemy3 = Enemy(random.randint(0, 736), random.randint(
    50, 150), 5, 20, 'enemy.png', 100)
enemy4 = Enemy(random.randint(0, 736), random.randint(
    50, 150), 5, 20, 'enemy.png', 100)
enemy5 = Enemy(random.randint(0, 736), random.randint(50, 150), 5, 20, 'enemy.png', 100)
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5]
torpedo1_player = Projectile(player.x, player.y, 0, 5, 'torpedo.png', 'Ready')
torpedo2_player = Projectile(player.x, player.y, 0, 5, 'torpedo.png', 'Ready')
torpedo3_player = Projectile(player.x, player.y, 0, 5, 'torpedo.png', 'Ready')
torpedo1_enemy = Projectile(enemy1.x, enemy1.y, 0, 1, 'enemy_torpedo.png', 'Ready')
torpedo2_enemy = Projectile(enemy2.x, enemy2.y, 0, 1, 'enemy_torpedo.png', 'Ready')
torpedo3_enemy = Projectile(enemy3.x, enemy3.y, 0, 1, 'enemy_torpedo.png', 'Ready')
torpedo4_enemy = Projectile(enemy4.x, enemy4.y, 0, 1, 'enemy_torpedo.png', 'Ready')
torpedo5_enemy = Projectile(enemy5.x, enemy5.y, 0, 1, 'enemy_torpedo.png', 'Ready')
torpedoes_player = [torpedo1_player, torpedo2_player, torpedo3_player]
torpedoes_enemy = [torpedo1_enemy, torpedo2_enemy, torpedo3_enemy, torpedo4_enemy, torpedo5_enemy]


def main():
    # Start of game loop
    global lives, score_value
    FPS = 60

    # Play backrgound_music
    backrgound_music('background.wav')
    while True:
        # Print background
        screen.blit(background, (0, 0))
        pygame.time.Clock().tick(FPS)

        # Check for keypresses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                # A key is pressed
                if event.key == pygame.K_LEFT:
                    player.x_change = -5
                if event.key == pygame.K_RIGHT:
                    player.x_change = 5
                if event.key == pygame.K_SPACE:
                    if torpedo1_player.state == 'Ready':
                        torpedo1_player.fire(player)
                    elif torpedo2_player.state == 'Ready':
                        torpedo2_player.fire(player)
                    elif torpedo3_player.state == 'Ready':
                        torpedo3_player.fire(player)
                if event.key == pygame.K_UP:
                    player.y_change = -5
                if event.key == pygame.K_DOWN:
                    player.y_change = 5
                player.x += player.x_change
            if event.type == pygame.KEYUP:
                # A key is released
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_change = 0

    # Player movement
        player.x += player.x_change
        player.y += player.y_change

        if player.x <= 0:
            player.x = 0
        elif player.x >= 736:
            player.x = 736
        if player.y <= 0:
            player.y = 0
        elif player.y >= 536:
            player.y = 536

        # Enemy movement
        for enemy in enemies:
            enemy.x += enemy.x_change
            if enemy.x <= 0:
                enemy.x_change = -enemy.x_change
                enemy.x += enemy.x_change
                enemy.y += enemy.y_change
            elif enemy.x >= 736:
                enemy.x_change = -enemy.x_change
                enemy.x += enemy.x_change
                enemy.y += enemy.y_change

        # Player torpedo fire
        for torpedo_player in torpedoes_player:
            if torpedo_player.state == 'Fire':
                torpedo_player.draw_image()
                torpedo_player.y -= torpedo_player.y_change
            if torpedo_player.y <= 0:
                torpedo_player.y = player.y
                torpedo_player.x = player.x
                torpedo_player.state = 'Ready'

    # Enemy health and respawn
        for torpedo_player in torpedoes_player:
            for enemy in enemies:
                if torpedo_player.collision_check(enemy) == True:
                    score_value += 1
                    enemy.reduce_health()
                if enemy.health <= 0:
                    enemy.health = enemy.max_health
                    enemy.respawn()

    # Player health
        for torpedo_enemy in torpedoes_enemy:
            if player.health > 0:
                if torpedo_enemy.collision_check(player) == True:
                    player.reduce_health()
            elif player.health <= 0:
                lives -= 1
                player.health = 100
                player.respawn()

        if lives <= 0:
            game_over()

        for enemy in enemies:
            if enemy.y >= 500:
                game_over()

    # Random enemy torpedo fire
        fire_or_not = random.randint(1, 5)
        if fire_or_not == 1:
            if torpedo1_enemy.state == 'Ready':
                torpedo1_enemy.fire(enemy1)
        elif fire_or_not == 2:
            if torpedo2_enemy.state == 'Ready':
                torpedo2_enemy.fire(enemy2)
        elif fire_or_not == 3:
            if torpedo3_enemy.state == 'Ready':
                torpedo3_enemy.fire(enemy3)
        elif fire_or_not == 4:
            if torpedo4_enemy.state == 'Ready':
                torpedo4_enemy.fire(enemy4)
        elif fire_or_not == 5:
            if torpedo5_enemy.state == 'Ready':
                torpedo5_enemy.fire(enemy5)

    # Enemy torpedo fire
        for torpedo_enemy in torpedoes_enemy:
            for enemy in enemies:
                if torpedo_enemy.state == 'Fire':
                    torpedo_enemy.draw_image()
                    torpedo_enemy.y += torpedo_enemy.y_change
                if torpedo_enemy.y >= 536:
                    torpedo_enemy.y = enemy.y
                    torpedo_enemy.x = enemy.x
                    torpedo_enemy.state = 'Ready'

        player.draw_image()
        player.print_healthbar(screen)
        enemy1.draw_image()
        enemy1.print_healthbar(screen)
        enemy2.draw_image()
        enemy2.print_healthbar(screen)
        enemy3.draw_image()
        enemy3.print_healthbar(screen)
        enemy4.draw_image()
        enemy4.print_healthbar(screen)
        enemy5.draw_image()
        enemy5.print_healthbar(screen)
        print_font(10, 10, f"Score: {score_value}", 255, 255, 255)
        print_font(10, 40, f"Lives: {lives}", 255, 255, 255)
        pygame.display.update()


# Main Menu Screen
def menu():
    while True:
        # Stop backrgound music
        pygame.mixer.music.stop()
        # Print background
        screen.blit(background, (0, 0))
        print_font(60, 250, "Welcome to The Battle Of Tannhauser Gate", 255, 255, 255)
        print_font(200, 300, "Click anywhere to begin...", 255, 255, 255)
        # Check for keypresses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

        pygame.display.update()


# Game over screen
def game_over():
    while True:
        # Stop background music
        pygame.mixer.music.stop()
        # Print background
        screen.blit(background, (0, 0))
        print_font(300, 250, "GAME OVER", 255, 255, 255)
        print_font(220, 300, "Click anywhere to quit...", 255, 255, 255)
        print_font(10, 10, f"Score: {score_value}", 255, 255, 255)
        print_font(10, 40, f"Lives: {lives}", 255, 255, 255)
        # Check for keypresses
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                quit()
        pygame.display.update()


# Start menu and later game on execution
if __name__ == '__main__':
    menu()
