import snake_game
from datetime import datetime

print(snake_game.snake_position)
print(snake_game.snake_position[0])
print(snake_game.apple_position)
print(snake_game.apple_position[0]-snake_game.snake_position[0][0])  #뱀 머리와 먹이 사이의 x값 차이
print(snake_game.apple_position[1]-snake_game.snake_position[0][1])  #뱀 머리와 먹이 사이의 y값 차이

navigator = True
while navigator:
    if (snake_game.apple_position[1]-snake_game.snake_position[0][1])<0:
        if not snake_game.direction =='D':                # 최근에 이동한 방향과 반대 방향으로는 이동할 수 없다
            snake_game.Snake.follow_head(snake_game.snake_position)
            snake_game.snake_position[0][1] -= 20         # 블록의 y 좌표를 20 뺀다
            snake_game.last_moved = datetime.now()        # 방향키를 입력한 시간을 기록
            snake_game.direction = 'U'                    # 방향 저장하는 변수에 상하좌우을 저장
    elif (snake_game.apple_position[1]-snake_game.snake_position[0][1])>0:
        if not snake_game.direction =='U':                # 최근에 이동한 방향과 반대 방향으로는 이동할 수 없다
            snake_game.Snake.follow_head(snake_game.Snake,snake_game.snake_position)
            snake_game.snake_position[0][1] += 20         # 블록의 y 좌표를 20 더한다
            snake_game.last_moved = datetime.now()         # 방향키를 입력한 시간을 기록
            snake_game.direction = 'D'                    # 방향 저장하는 변수에 상하좌우을 저장
    elif (snake_game.apple_position[0]-snake_game.snake_position[0][0])<0:
        if snake_game.direction == '':
            print("다른 방향키를 눌러 주세요!")
        elif not snake_game.direction =='R':                # 최근에 이동한 방향과 반대 방향으로는 이동할 수 없다
            snake_game.Snake.follow_head(snake_game.Snake,snake_game.snake_position)
            snake_game.snake_position[0][0] -= 20         # 블록의 x 좌표를 20 뺀다
            snake_game.last_moved = datetime.now()         # 방향키를 입력한 시간을 기록
            direction = 'L'                    # 방향 저장하는 변수에 상하좌우을 저장
    elif (snake_game.apple_position[0]-snake_game.snake_position[0][0])>0:
        if not snake_game.direction =='L':                # 최근에 이동한 방향과 반대 방향으로는 이동할 수 없다
            snake_game.Snake.follow_head(snake_game.Snake,snake_game.snake_position)
            snake_game.snake_position[0][0] += 20         # 블록의 x 좌표를 20 더한다
            snake_game.last_moved = datetime.now()        # 방향키를 입력한 시간을 기록
            snake_game.direction = 'R'                    # 방향 저장하는 변수에 상하좌우을 저장


snake_game.rungame()
pygame.quit()
