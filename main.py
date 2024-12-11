import math
import sys

import pygame

pygame.init()

# ウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pendulum")

# FPSの設定
clock = pygame.time.Clock()
FPS = 60

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)

# 設定
fulcrum_point = pygame.math.Vector2(screen_width // 2, screen_height // 2)  # 支点位置
length = 100    # 糸の長さ
angle_deg = 45  # 角度 [deg]
offset_deg = 90
angle = math.radians(angle_deg + offset_deg)     # 角度 [rad]
angle_velocity = 0  # 角速度
angle_acceleration = 0  # 各加速度
g = 0.5     # 重力

while True:

    # 背景の塗りつぶし
    screen.fill(WHITE)

    # 振り子の演算
    angle_acceleration = -(g / length) * math.sin(angle)  # 角加速度の計算
    angle_velocity += angle_acceleration  # 角速度の更新
    angle_velocity *= 0.99  # 減衰効果
    angle += angle_velocity  # 角度の更新

    # プレイヤーの位置の計算
    player_point = pygame.math.Vector2(
        fulcrum_point.x + length * math.sin(angle),
        fulcrum_point.y + length * math.cos(angle)
    )

    # 支点の描画
    pygame.draw.circle(screen, GREEN, (fulcrum_point.x, fulcrum_point.y), 10)

    # プレイヤーの描画
    pygame.draw.circle(screen, RED, (player_point.x, player_point.y), 30)

    # 糸の描画
    pygame.draw.line(screen, BLACK, (fulcrum_point.x, fulcrum_point.y), (player_point.x, player_point.y), 3)

    # イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # 更新
    pygame.display.update()
    clock.tick(FPS)
