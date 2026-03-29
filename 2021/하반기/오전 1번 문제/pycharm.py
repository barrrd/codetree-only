from collections import deque
def update_dice(d):
    global dices
    top, down, west, east, north, south = dices

    if d == 0: # 우
        top, down, west, east = west, east, down, top
    elif d == 1: # 하
        top, down, north, south = north, south, down, top
    elif d == 2: # 좌
        top, down, west, east = east, west, top, down
    else: # d == 3: # 상
        top, down, north, south = south, north, top, down

    dices = [top, down, west, east, north, south]

def step1():
    global sr, sc, d
    # 1. move a sr, sc
    nr, nc = sr + dr[d], sc + dc[d]
    if not(0 <= nr < n and 0 <= nc < n):
        d = (d + 2)  % 4
        nr, nc = sr + dr[d], sc + dc[d]
    sr, sc = nr, nc
    # 2. update dices
    update_dice(d)
    # 3. update a dir
    down = dices[1]
    if down > arr[sr][sc]:
        d = (d+1)% 4
    elif down < arr[sr][sc]:
        d = (d-1)% 4


def step2():
    global sr, sc, answer
    v = set()
    q = deque([(sr,sc)])
    axis = arr[sr][sc]
    best = 1
    v.add((sr,sc))
    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not(0 <= nr < n and 0 <= nc < n) or (nr,nc) in v:
                continue
            if axis == arr[nr][nc]:
                v.add((nr,nc))
                best += 1
                q.append((nr,nc))
    answer += best * axis


# 1.init
T = 1
for ts in range(1, T + 1):
    n, m = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(n)]
    # 우 하 좌 상
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    # 0: top, 1: down, 2: west, 3: east, 4: north, 5: south
    dices = [1, 6, 4, 3, 5, 2]
    sr, sc, d = 0, 0, 0
    answer = 0
    # dices = {"top": 1, "down": 6, "west": 4, "east": 3, "no"}
    for turn in range(1, m + 1):
        # 1. mova a sr,sc and update d
        step1()
        # 2. score
        step2()
    print(answer)
