import thumbox

# Create the Emulator object
thumby = thumbox.Thumby()
graphics = thumby.graphics
button = thumby.button

# Constants
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 6
BALL_SIZE = 8
PADDLE_SPEED = 1
BALL_SPEED = 1

# Variables
player1_pos = (graphics.display.height - PADDLE_HEIGHT) // 2
player2_pos = (graphics.display.height - PADDLE_HEIGHT) // 2
ball_x = (graphics.display.width - BALL_SIZE) // 2
ball_y = (graphics.display.height - BALL_SIZE) // 2
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED
player1_score = 0
player2_score = 0

# New sprite designs
paddle_map = bytearray([0b01111110,
                        0b11111111,
                        0b11111111,
                        0b01111110,
                        0b11111111,
                        0b01111110])

ball_map = bytearray([0b00111100,
                      0b01111110,
                      0b11111111,
                      0b11100111,
                      0b11100111,
                      0b11111111,
                      0b01111110,
                      0b00111100])

# Create Sprite objects
player1_sprite = thumby.Sprite(PADDLE_WIDTH, PADDLE_HEIGHT, paddle_map, 0, player1_pos)
player2_sprite = thumby.Sprite(PADDLE_WIDTH, PADDLE_HEIGHT, paddle_map, graphics.display.width - PADDLE_WIDTH, player2_pos)
ball_sprite = thumby.Sprite(BALL_SIZE, BALL_SIZE, ball_map, ball_x, ball_y)
# Background sprite
background_map = bytearray(72 * 40 // 8)
for i in range(0, 40, 2):
    background_map[i] = 0b11110000

background_sprite = thumby.Sprite(1, 40, background_map, 36, 0)

graphics.display.setFPS(60)

def draw_paddles():
    graphics.display.drawSprite(player1_sprite)
    graphics.display.drawSprite(player2_sprite)

def draw_ball():
    graphics.display.drawSprite(ball_sprite)

def update_paddles():
    global player1_pos, player2_pos, player1_sprite, player2_sprite

    if button.buttonU.pressed() and player1_pos > 0:
        player1_pos -= PADDLE_SPEED
    elif button.buttonD.pressed() and player1_pos < graphics.display.height - PADDLE_HEIGHT:
        player1_pos += PADDLE_SPEED

    if button.buttonA.pressed() and player2_pos > 0:
        player2_pos -= PADDLE_SPEED
    elif button.buttonB.pressed() and player2_pos < graphics.display.height - PADDLE_HEIGHT:
        player2_pos += PADDLE_SPEED
    
    # Update paddle sprite positions
    player1_sprite.x = 0
    player1_sprite.y = player1_pos
    player2_sprite.x = graphics.display.width - PADDLE_WIDTH
    player2_sprite.y = player2_pos

def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, ball_sprite

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y <= 0 or ball_y >= graphics.display.height - BALL_SIZE:
        ball_dy = -ball_dy

    if ball_x <= PADDLE_WIDTH and (player1_pos <= ball_y <= player1_pos + PADDLE_HEIGHT):
        ball_dx = -ball_dx
    elif ball_x >= graphics.display.width - PADDLE_WIDTH - BALL_SIZE and (player2_pos <= ball_y <= player2_pos + PADDLE_HEIGHT):
        ball_dx = -ball_dx
        
    # Update ball sprite position
    ball_sprite.x = ball_x
    ball_sprite.y = ball_y

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = (graphics.display.width - BALL_SIZE) // 2
    ball_y = (graphics.display.height - BALL_SIZE) // 2
    ball_dx = BALL_SPEED
    ball_dy = BALL_SPEED
    
def draw_scores():
    graphics.display.drawText(str(player1_score), graphics.display.width // 4, 2, 1)
    graphics.display.drawText(str(player2_score), (graphics.display.width * 3) // 4, 2, 1)

def update_scores():
    global player1_score, player2_score, ball_x

    if ball_x <= 0:
        player2_score += 1
    elif ball_x >= graphics.display.width - BALL_SIZE:
        player1_score += 1

def draw_background():
    graphics.display.drawSprite(background_sprite)

while True:
    graphics.display.fill(0)

    draw_background()
    update_paddles()
    update_ball()

    if ball_x <= 0 or ball_x >= graphics.display.width - BALL_SIZE:
        update_scores()
        reset_ball()

    draw_paddles()
    draw_ball()
    draw_scores()

    graphics.display.update()