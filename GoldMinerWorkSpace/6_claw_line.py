# 집게까지 직선을 그리기
import os
import pygame


class Claw(pygame.sprite.Sprite):
    # 집게 클래스
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

    def update(self):
        rect_center = self.position + self.offset
        self.rect = self.image.get_rect(center=rect_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3)  # 중심점 표시
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)  # 직선그리기


class Gemstone(pygame.sprite.Sprite):
    # 보석 클래스
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)


def setup_gemstone():
    # 작은 금                  0번쨰 이미지를 200,380좌표에
    small_gold = Gemstone(gemstone_images[0], (200, 380))
    gemstone_group.add(small_gold)  # 그룹에 추가
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    # 다이아
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))


# 기본 뼈대 생성
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()

# 게임 관련 변수
default_offset_x_claw = 40  # 중심점으로부터 집게까지의 기본x 간격

# 색깔 변수
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")),  # 작은 금
    pygame.image.load(os.path.join(current_path, "big_gold.png")),  # 큰 금
    pygame.image.load(os.path.join(current_path, "stone.png")),  # 돌
    pygame.image.load(os.path.join(current_path, "diamond.png")),
]  # 다이아

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()

# 집게
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width // 2, 110))

running = True
while running:
    clock.tick(30)  # FPS 값이 30으로 고정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    claw.update()
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
