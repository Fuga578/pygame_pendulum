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

# キー
INPUTS = {
    "up": False,
    "down": False,
    "left": False,
    "right": False
}

# 初期設定
fulcrum_point = pygame.math.Vector2()  # 支点位置
length = 100    # 糸の長さ
angle_deg = 45  # 角度 [deg]
offset_deg = 90
angle = math.radians(angle_deg + offset_deg)     # 角度 [rad]
angle_velocity = 0  # 角速度
angle_acceleration = 0  # 各加速度
gravity = 0.5     # 重力
is_hook = False
release_velocity = pygame.math.Vector2()  # 振り子リリース時の速度
input_velocity = pygame.math.Vector2()    # 入力による速度
player_point = pygame.math.Vector2(screen_width // 2, screen_height // 2)
player_speed = 5
on_ground = False
friction = 0.9

while True:
    # 背景の塗りつぶし
    screen.fill(WHITE)

    # プレイヤーの描画
    pygame.draw.circle(screen, RED, (player_point.x, player_point.y), 30)

    # 振り子の演算
    if is_hook:
        # 支点の描画
        pygame.draw.circle(screen, GREEN, (fulcrum_point.x, fulcrum_point.y), 10)

        # 糸の描画
        pygame.draw.line(screen, BLACK, (fulcrum_point.x, fulcrum_point.y), (player_point.x, player_point.y), 3)

        # 入力による加速
        swing_force = 0.3 / length
        if INPUTS["left"]:
            angle_velocity -= swing_force
        if INPUTS["right"]:
            angle_velocity += swing_force

        angle_acceleration = -(gravity / length) * math.sin(angle)  # 角加速度の計算
        angle_velocity += angle_acceleration  # 角速度の更新
        angle_velocity *= 0.99  # 減衰効果
        angle += angle_velocity  # 角度の更新

        # プレイヤーの位置の計算
        player_point = pygame.math.Vector2(
            fulcrum_point.x + length * math.sin(angle),
            fulcrum_point.y + length * math.cos(angle)
        )

    # 振り子中でない場合
    else:
        input_velocity.x = 0
        if INPUTS["left"]:
            if release_velocity.x > 0:
                release_velocity.x *= 0.95  # 逆方向の入力で徐々に減速
                if abs(release_velocity.x) < player_speed:
                    release_velocity.x = 0
            elif release_velocity.x < 0:
                input_velocity.x = -2
            else:
                input_velocity.x = -player_speed
        if INPUTS["right"]:
            if release_velocity.x < 0:
                release_velocity.x *= 0.95  # 逆方向の入力で徐々に減速
                if abs(release_velocity.x) < player_speed:
                    release_velocity.x = 0
            elif release_velocity.x > 0:
                input_velocity.x = 2
            else:
                input_velocity.x = player_speed
        if INPUTS["up"] and on_ground:
            release_velocity.y = -10  # ジャンプ
            on_ground = False

        # 合計速度 = リリース時の速度 + 入力による速度
        total_velocity = release_velocity + input_velocity
        player_point += total_velocity
        release_velocity.y += gravity

        if on_ground:
            release_velocity.x *= friction  # 地面でのみ摩擦を適用
            if abs(release_velocity.x) < 0.1:
                release_velocity.x = 0

        # 地面に当たったら停止
        if player_point.y >= screen_height - 30:
            player_point.y = screen_height - 30
            release_velocity.y = 0
            on_ground = True

    # イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # キーボード押下
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP:
                INPUTS["up"] = True
            if event.key == pygame.K_DOWN:
                INPUTS["down"] = True
            if event.key == pygame.K_LEFT:
                INPUTS["left"] = True
            if event.key == pygame.K_RIGHT:
                INPUTS["right"] = True
        # キーボード解放
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                INPUTS["up"] = False
            if event.key == pygame.K_DOWN:
                INPUTS["down"] = False
            if event.key == pygame.K_LEFT:
                INPUTS["left"] = False
            if event.key == pygame.K_RIGHT:
                INPUTS["right"] = False
        # マウスクリック
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 左クリック
            if event.button == 1:
                # 更新
                is_hook = True
                on_ground = False
                mx, my = pygame.mouse.get_pos()
                fulcrum_point = pygame.math.Vector2(mx, my)     # 支点位置
                length = math.sqrt((mx - player_point.x)**2 + (my - player_point.y)**2)  # 糸の長さ
                angle = math.atan2(player_point.x - mx, player_point.y - my)    # ※座標系が異なる（原点が左上）であるため、角度計算を一部専用に修正
                angle_velocity = 0  # 角速度

        # マウス解放
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_hook = False
                release_velocity = pygame.math.Vector2(
                    angle_velocity * length * math.cos(angle),
                    -angle_velocity * length * math.sin(angle)
                )

    # 更新
    pygame.display.update()
    clock.tick(FPS)
