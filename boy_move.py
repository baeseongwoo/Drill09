from pico2d import *

# 화면 (배경 이미지와 같은 크기)
TUK_WIDTH, TUK_HEIGHT = 1280, 1024

# 스프라이트 시트: 100x100 칸이 가로 8개(프레임), 세로 4줄(동작)
FRAME_SIZE = 100
FRAME_COUNT = 8
# 줄 위치는 이미지 아래쪽에서부터의 y좌표
ROW_RUN_LEFT, ROW_RUN_RIGHT, ROW_IDLE_LEFT, ROW_IDLE_RIGHT = 0, 100, 200, 300

# 칸 중심에서 실제 그림 끝까지의 거리 (경계 판정용)
BOY_HALF_W, BOY_HALF_H = 33, 43

RUN_SPEED = 300         # 이동 속도 (px/초)
FRAMES_PER_SEC = 12     # 애니메이션 속도 (프레임/초)
DIAGONAL = 0.7071       # 대각선 이동 보정값 (1/√2)

open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running, dir_x, dir_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1


def clamp(low, value, high):
    return max(low, min(value, high))


def get_row():
    # 이동 중이면 달리기, 아니면 IDLE. 좌우는 바라보는 방향을 따른다
    if dir_x != 0 or dir_y != 0:
        return ROW_RUN_RIGHT if facing == 1 else ROW_RUN_LEFT
    return ROW_IDLE_RIGHT if facing == 1 else ROW_IDLE_LEFT


def update(frame_time):
    global x, y, frame, facing
    # 위아래로만 움직일 때는 dir_x가 0이라 기존 방향이 유지된다
    if dir_x != 0:
        facing = 1 if dir_x > 0 else -1
    frame = (frame + FRAMES_PER_SEC * frame_time) % FRAME_COUNT
    distance = RUN_SPEED * frame_time
    if dir_x != 0 and dir_y != 0:
        distance *= DIAGONAL
    x = clamp(BOY_HALF_W, x + dir_x * distance, TUK_WIDTH - BOY_HALF_W)
    y = clamp(BOY_HALF_H, y + dir_y * distance, TUK_HEIGHT - BOY_HALF_H)


def draw():
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character.clip_draw(int(frame) * FRAME_SIZE, get_row(), FRAME_SIZE, FRAME_SIZE, x, y)
    update_canvas()


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x = 0       # 좌우 입력: -1, 0, 1
dir_y = 0       # 상하 입력: -1, 0, 1
facing = 1      # 1: 오른쪽, -1: 왼쪽
prev_time = get_time()

while running:
    now = get_time()
    frame_time = now - prev_time
    prev_time = now

    handle_events()
    update(frame_time)
    draw()
    delay(0.01)

close_canvas()
