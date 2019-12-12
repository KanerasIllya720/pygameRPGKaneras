import numpy as np
import random
import time


# 본 프로그램은 numpy 3차원 배열을 맵으로 사용함.
# 프로그램은 시작점에서부터 한 칸씩 임의의 방향으로 이동하며 길을 생성함.
# 맵의 각 원소는 크기가 2인 순서쌍으로, 이전 칸의 좌표를 담음.
# 예컨대 [3,2]에서 [3,3]으로 이동했다고 하면, map[3,3] =[3,2]가 됨.
# 한 번도 가본 적 없는 칸의 경우, 기본값은 [-1,-1]로 설정되어 있음.
# 따라서 맵은 [세로,가로,2]의 크기를 가지는 3차원 배열이 됨.
# 프로그램은 이동하면서, 현재 칸의 위치를 visited 배열에 담음.
# 만약 가다가 전후좌우가 모두 막힌 곳을 발견하면, visited 배열에서 현재 칸을 지운 후,
# visited 배열 내의 임의의 칸으로 이동함.
# 요약하면 더이상 갈 곳이 없을 때까지 이동하다가, 길이 막혀버리면 왔던 길 중 아무 곳에서나 다시 길을 찾기 시작함.


# 배열에서 임의의 원소를 선택하여 반환함.
def random_select(arr):
    return arr[random.randint(0, len(arr) - 1)]


# 맵에서 주위의 '가본 적 없는'칸들, 즉 다음에 갈 수 있는 칸들의 좌표를 반환함.
def get_around(cur, map):
    next = []
    h = map.shape[0]
    w = map.shape[1]
    if cur[0] > 0 and map[cur[0] - 1, cur[1]][0] < 0: next.append([cur[0] - 1, cur[1]])
    if cur[0] < h - 1 and map[cur[0] + 1, cur[1]][0] < 0: next.append([cur[0] + 1, cur[1]])
    if cur[1] > 0 and map[cur[0], cur[1] - 1][0] < 0: next.append([cur[0], cur[1] - 1])
    if cur[1] < w - 1 and map[cur[0], cur[1] + 1][0] < 0: next.append([cur[0], cur[1] + 1])
    return next


def go_next(cur, map, visited):
    nexts = get_around(cur, map)
    if len(nexts) > 0:  # 만약 다음에 갈 곳이 있으면
        visited.append(cur)  # visited 배열에 현재 좌표를 추가하고
        next = random_select(nexts)  # 주변의 칸 중 이동할 칸을 정한다.
        map[next[0], next[1]] = cur  # 이동할 칸에 현재 칸의 좌표를 적는다.
        return next  # 이동할 칸을 반환한다.
    else:  # 만약 갈 곳이 없으면
        # visited 배열에서 현재 칸의 좌표를 지운다.
        if cur in visited:
            visited.remove(cur)
        # 만약 visited 배열이 비었으면,
        # 이 상태는 여태까지 방문했던 모든 칸들에 대해서, 사방이 전부 한 번 이상 방문했던 칸이라는 뜻이다.
        # 즉, 맵의 모든 칸들을 전부 다 방문하였다.
        if len(visited) == 0:
            return None  # 따라서 None 을 반환하여 마지막 칸을 방문했음을 알린다.
        return random_select(visited)  # 만약 visited 배열이 안 비었으면 visited 배열 중 아무 칸을 반환한다.


# 본 프로그램에서 다루는 맵은 각 칸에 그 이전 칸의 정보가 담겨있다.
# 이를 시각적으로 볼 수 있도록 변환하는 메서드.
# 맵의 크기를 2배로 늘린 뒤, 각 칸과, 각 칸의 이전 칸,그리고 그 사이를 1로 한다.
# 그리고 나머지는 0으로 한다.
# 이렇게 하면 벽을 0으로, 경로를 1로 표시한 2차원 배열이 나온다.
def drawMap(map):
    h = map.shape[0] * 2 - 1
    w = map.shape[1] * 2 - 1
    draw = np.ndarray([w, h], np.int)
    draw[::] = 0

    for y in range(map.shape[0]):
        for x in range(map.shape[1]):
            pos = map[y, x]
            draw[y * 2, x * 2] = 1
            draw[pos[0] * 2, pos[1] * 2] = 1
            draw[y + pos[0], x + pos[1]] = 1

    return draw


# 위의 drawMap 메서드로 만든 2차원 배열을 네모 모양으로 시각화하여 출력하는 메서드.
# 위의 메서드는 미로의 외벽을 표현하지 않으므로, 외벽을 추가해준다.
# 빈 네모는 경로, 색칠된 네모는 벽을 뜻한다.
def printMap(map, line_end=''):
    assert len(map.shape) is 2
    for i in range(map.shape[1] + 1):
        print('■', end=line_end)
    print('■')
    for row in map:
        print('■', end=line_end)
        for item in row:
            if item == 0:
                print('■', end=line_end)
            elif item == 2:
                print('◆', end=line_end)
            else:
                print('□', end=line_end)
        print('■')
    for i in range(map.shape[1] + 1):
        print('■', end=line_end)
    print('■')


w = 9  # 미로의 가로 크기
h = 9  # 미로의 세로 크기

map = np.ndarray([w, h, 2], np.int)
map[::] = -1
current = [0, 0]  # 현재 칸. 초기값은 시작점을 뜻한다. 예컨대 [w/2,h/2]로 설정하면 중간에서부터 미로를 만든다.
visited = []

print('Start generating...')
start_time = time.time()
while True:
    map[0, 0, :] = 0
    current = go_next(current, map, visited)
    if current is None:
        break
end_time = time.time()

printMap(drawMap(map))
print('It took ', round(end_time - start_time, 2), 's to generate ', w, ' x ', h, ' size map.', sep='')
