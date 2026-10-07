from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
FRAME_SIZE = 100
FRAME_COUNT = 8
ROW_RUN_LEFT, ROW_RUN_RIGHT, ROW_IDLE_LEFT, ROW_IDLE_RIGHT = 0, 100, 200, 300
BOY_HALF_W, BOY_HALF_H = 33, 43
RUN_SPEED = 300

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
    if dir_x != 0 or dir_y != 0:
        return ROW_RUN_RIGHT if facing == 1 else ROW_RUN_LEFT
    return ROW_IDLE_RIGHT if facing == 1 else ROW_IDLE_LEFT


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x = 0
dir_y = 0
facing = 1
prev_time = get_time()

while running:
    now = get_time()
    frame_time = now - prev_time
    prev_time = now

    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character.clip_draw(frame * FRAME_SIZE, get_row(), FRAME_SIZE, FRAME_SIZE, x, y)
    update_canvas()
    handle_events()
    if dir_x != 0:
        facing = 1 if dir_x > 0 else -1
    frame = (frame + 1) % FRAME_COUNT
    distance = RUN_SPEED * frame_time
    x = clamp(BOY_HALF_W, x + dir_x * distance, TUK_WIDTH - BOY_HALF_W)
    y = clamp(BOY_HALF_H, y + dir_y * distance, TUK_HEIGHT - BOY_HALF_H)
    delay(0.01)

close_canvas()
