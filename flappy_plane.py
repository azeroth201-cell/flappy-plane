import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Plane")
clock = pygame.time.Clock()

try:
    plane_img = pygame.image.load("assets/images/plane.png").convert_alpha()
    cloud_img = pygame.image.load("assets/images/cloud.png").convert_alpha()
except:
    plane_img = None
    cloud_img = None

try:
    wing_sound = pygame.mixer.Sound("assets/audio/wing.wav")
    score_sound = pygame.mixer.Sound("assets/audio/score.wav")
    crash_sound = pygame.mixer.Sound("assets/audio/crash.wav")
except:
    wing_sound = score_sound = crash_sound = None

font = pygame.font.SysFont("Arial", 36, bold=True)

class CloudPair:
    def __init__(self):
        self.gap = 160
        self.width = 70
        self.x = WIDTH
        self.top_height = random.randint(80, HEIGHT - self.gap - 80)
        self.bottom_y = self.top_height + self.gap
        self.passed = False
        self.speed = 3

    def update(self):
        self.x -= self.speed
        return self.x > -self.width

    def draw(self):
        if cloud_img:
            top_scaled = pygame.transform.scale(cloud_img, (self.width, self.top_height))
            top_flipped = pygame.transform.flip(top_scaled, False, True)
            screen.blit(top_flipped, (self.x, self.top_height - top_scaled.get_height()))
            bottom_scaled = pygame.transform.scale(cloud_img, (self.width, HEIGHT - self.bottom_y))
            screen.blit(bottom_scaled, (self.x, self.bottom_y))
        else:
            pygame.draw.rect(screen, (192, 192, 192), (self.x, 0, self.width, self.top_height))
            pygame.draw.rect(screen, (192, 192, 192), (self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y))

    def collide(self, plane_rect):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y)
        return plane_rect.colliderect(top_rect) or plane_rect.colliderect(bottom_rect)

def main():
    plane_x = 100
    plane_y = HEIGHT // 2
    gravity = 0.5
    lift = -8
    velocity = 0
    score = 0
    game_active = True
    cloud_timer = 0
    clouds = []

    while True:
        dt = clock.tick(FPS)
        screen.fill((135, 206, 235))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    velocity = lift
                    if wing_sound:
                        wing_sound.play()
                if event.key == pygame.K_r and not game_active:
                    main()

        if game_active:
            velocity += gravity
            plane_y += velocity

            plane_rect = pygame.Rect(plane_x, plane_y, 40, 20)
            if plane_img:
                screen.blit(plane_img, (plane_x, plane_y))
            else:
                pygame.draw.rect(screen, (100, 100, 100), plane_rect)

            cloud_timer += dt
            if cloud_timer > 1800:
                clouds.append(CloudPair())
                cloud_timer = 0

            for cloud in list(clouds):
                if not cloud.update():
                    clouds.remove(cloud)
                    continue
                cloud.draw()
                if cloud.collide(plane_rect):
                    game_active = False
                    if crash_sound:
                        crash_sound.play()
                if not cloud.passed and cloud.x + cloud.width < plane_x:
                    cloud.passed = True
                    score += 1
                    if score_sound:
                        score_sound.play()

            if plane_y < 0 or plane_y > HEIGHT:
                game_active = False
                if crash_sound:
                    crash_sound.play()

            score_text = font.render(str(score), True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
            screen.blit(score_text, score_rect)

        else:
            game_over = font.render("GAME OVER", True, (0, 0, 0))
            game_over_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(game_over, game_over_rect)

            final_score = font.render(f"Score: {score}", True, (0, 0, 0))
            final_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(final_score, final_rect)

            restart = font.render("Press R to restart", True, (0, 0, 0))
            restart_rect = restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(restart, restart_rect)

        pygame.display.update()

if __name__ == "__main__":
    main()