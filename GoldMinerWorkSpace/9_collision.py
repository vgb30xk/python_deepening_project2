# 충돌 처리
import math
import os
import pygame


class Claw(pygame.sprite.Sprite):
    # 집게 클래스
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT  # 집게의 이동 방향
        self.angle_speed = 2.5  # 집게의 각도 변경 폭(좌우 이동속도)
        self.angle = 10  # 최초 각도 정의 ( 오른쪽 끝)

    def update(self, to_x):
        if self.direction == LEFT:  # 왼쪽 으로 이동시
            self.angle += self.angle_speed  # 이동속도 만큼 각도증가
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed

        # 만약에 허용 각도 범위를 벗어나면?
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x
        self.rotate()  # 회전처리

    def rotate(self):
        # 회전대상 이미지, 회전각도, 이미지크기(1배)
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.position + offset_rotated)

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)  # 직선그리기

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT


class Gemstone(pygame.sprite.Sprite):
    # 보석 클래스
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        r = self.rect.size[0] // 2
        rad_angle = math.radians(angle)  # 각도
        to_x = r * math.cos(rad_angle)  # 삼각형의 밑변
        to_y = r * math.sin(rad_angle)  # 삼각형의 높이
        self.rect.center = (position[0] + to_x, position[1] + to_y)


def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamod_price, diamond_speed = 600, 7

    # 작은 금                  0번쨰 이미지를 200,380좌표에
    small_gold = Gemstone(
        gemstone_images[0], (200, 380), small_gold_price, small_gold_speed
    )
    gemstone_group.add(small_gold)  # 그룹에 추가
    # 큰 금
    gemstone_group.add(
        Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed)
    )
    # 돌
    gemstone_group.add(
        Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed)
    )
    # 다이아
    gemstone_group.add(
        Gemstone(gemstone_images[3], (900, 420), diamod_price, diamond_speed)
    )


# 기본 뼈대 생성
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()

# 게임 관련 변수
default_offset_x_claw = 40  # 중심점으로부터 집게까지의 기본x 간격
to_x = 0  # x좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수
caught_gemstone = None  # 집게를 뻗어서 잡은 보석 정보

# 속도 변수
move_speed = 12  # 발사할 때 이동 스피드(x 좌표 기준으로 증가되는값)
return_speed = 20

LEFT = -1  # 왼쪽 방향
RIGHT = 1  # 오른쪽 방향
STOP = 0  # 고정인상태(집게 뻗음)

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

        if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스버튼 눌렀을떄
            claw.set_direction(STOP)
            to_x = move_speed

    # 벽에 충돌했을때
    if (
        claw.rect.left < 0
        or claw.rect.right > screen_width
        or claw.rect.bottom > screen_height
    ):
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw:  # 원위치에 오면
        to_x = 0
        claw.set_init_state()  # 처음상태로 되돌림

        if caught_gemstone:  # 잡혔으면
            # update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)  # 그룹에서 보석제거
            caught_gemstone = None

    if not caught_gemstone:  # 잡힌 보석이 없다면 충돌 체크
        for gemstone in gemstone_group:
            if claw.rect.colliderect(gemstone.rect):
                caught_gemstone = gemstone  # 잡힌 보석
                to_x = -gemstone.speed  # 잡힌 보석의  속도에 -한값을 이동속도로
                break

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))

    gemstone_group.draw(screen)
    claw.update(to_x)
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
