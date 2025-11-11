import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид - Skrim Games")

clock = pygame.time.Clock()

class GameObject: 
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Ball(GameObject):
    def __init__(self):
        super().__init__(screen_width // 2 - 10, screen_height // 2, 20, 20, (240, 240, 240))
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -5
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1
    
    def reset(self):
        self.rect.x = screen_width // 2 - 10
        self.rect.y = screen_height // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -5

class Paddle(GameObject):
    def __init__(self):
        super().__init__(screen_width // 2 - 75, screen_height - 40, 150, 20, (80, 180, 255))
        self.speed = 9
    
    def move_left(self):
        if self.rect.left > 5:
            self.rect.x -= self.speed
    
    def move_right(self):
        if self.rect.right < screen_width - 5:
            self.rect.x += self.speed

class Brick(GameObject):
    def __init__(self, x, y):
        colors = [
            (255, 90, 90),
            (90, 255, 90),  
            (90, 90, 255),
            (255, 255, 90),
            (255, 90, 255)
        ]
        super().__init__(x, y, 76, 30, random.choice(colors))

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.create_bricks()
    
    def create_bricks(self):
        for row in range(5):
            for col in range(9):
                brick = Brick(col * 85 + 25, row * 40 + 60)
                self.bricks.append(brick)
    
    def check_collisions(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y *= -1
            hit_pos = (self.ball.rect.centerx - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
            self.ball.speed_x = hit_pos * 6
        
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.bricks.remove(brick)
                self.ball.speed_y *= -1
                self.score += 15
    
    def update(self):
        self.ball.move()
        self.check_collisions()
        
        if self.ball.rect.bottom >= screen_height:
            self.lives -= 1
            if self.lives > 0:
                self.ball.reset()
            else:
                self.game_over()
        
        if len(self.bricks) == 0:
            self.level_complete()
    
    def game_over(self):
        big_font = pygame.font.SysFont('arial', 68)
        small_font = pygame.font.SysFont('arial', 36)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            
            screen.fill((30, 30, 60))
            
            text1 = big_font.render("ИГРА ОКОНЧЕНА", True, (255, 70, 70))
            text2 = small_font.render(f"Счет: {self.score}", True, (240, 240, 240))
            text3 = small_font.render("R - Начать заново", True, (180, 180, 180))
            text4 = small_font.render("ESC - Выход", True, (180, 180, 180))
            
            screen.blit(text1, (screen_width//2 - text1.get_width()//2, 200))
            screen.blit(text2, (screen_width//2 - text2.get_width()//2, 300))
            screen.blit(text3, (screen_width//2 - text3.get_width()//2, 350))
            screen.blit(text4, (screen_width//2 - text4.get_width()//2, 400))
            
            pygame.display.flip()
            clock.tick(60)
    
    def level_complete(self):
        big_font = pygame.font.SysFont('arial', 68)
        small_font = pygame.font.SysFont('arial', 36)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            
            screen.fill((30, 60, 30))
            
            text1 = big_font.render("УРОВЕНЬ ПРОЙДЕН!", True, (70, 255, 70))
            text2 = small_font.render(f"Счет: {self.score}", True, (240, 240, 240))
            text3 = small_font.render("R - Следующий уровень", True, (180, 180, 180))
            text4 = small_font.render("ESC - Выход", True, (180, 180, 180))
            
            screen.blit(text1, (screen_width//2 - text1.get_width()//2, 200))
            screen.blit(text2, (screen_width//2 - text2.get_width()//2, 300))
            screen.blit(text3, (screen_width//2 - text3.get_width()//2, 350))
            screen.blit(text4, (screen_width//2 - text4.get_width()//2, 400))
            
            pygame.display.flip()
            clock.tick(60)
    
    def draw(self):
        screen.fill((25, 25, 50))
        
        for brick in self.bricks:
            brick.draw(screen)
        
        self.paddle.draw(screen)
        self.ball.draw(screen)
        
        font = pygame.font.SysFont('arial', 32)
        score_text = font.render(f"Счет: {self.score}", True, (240, 240, 240))
        lives_text = font.render(f"Жизни: {self.lives}", True, (240, 240, 240))
        
        screen.blit(score_text, (20, screen_height - 40))
        screen.blit(lives_text, (screen_width - 150, screen_height - 40))

def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            game.paddle.move_right()
        if keys[pygame.K_ESCAPE]:
            running = False
        
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
