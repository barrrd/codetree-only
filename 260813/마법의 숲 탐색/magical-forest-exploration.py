from collections import deque
def update(sr, sc, id, d):
    global arr
    arr[sr][sc] = id

    for i in range(4):
        nr, nc = sr + dr[i], sc + dc[i]
        if i == d:
            arr[nr][nc] = -id
        else:
            arr[nr][nc] = id


def down(sr, sc):
    # Case1. 벽 밖
    if sr == R + 2:
        return False

    # Case2. 벽안: empty
    is_possible = True
    if arr[sr][sc] != 0:
        is_possible = False
    for i in range(4):
        nr, nc = sr + dr[i], sc + dc[i]
        if not (0 <= nr < R + 3 and 0 <= nc < C):
            return False
        if arr[nr][nc] != 0:
            is_possible = False
            break

    return is_possible

def left_right(sr, sc):
    is_left = True
    is_right = True
    flag = None

    left = [(-1, -1), (0, -2), (1, - 1), (1, -2), (2, -1)]
    right = [(-1, 1), (0, 2), (1, 1), (1, 2), (2, 1)]

    for dr, dc in left:
        nr, nc = sr + dr, sc + dc
        if not(0 <= nr < R+ 3 and 0 <= nc < C) or arr[nr][nc] != 0:
            is_left = False
            break

    if not(is_left):
        for dr, dc in right:
            nr, nc = sr + dr, sc + dc
            if not (0 <= nr < R + 3 and 0 <= nc < C) or arr[nr][nc] != 0:
                is_right = False
                break
    if is_left:
        flag = "left"
    elif is_right:
        flag = "right"

    return flag

def step1(id, sc, d):
    global arr, answer, golem
    sr = 1
    go_step2 = True

    # 1. choose a row
    while True:
        if down(sr + 1, sc):
            sr += 1
            continue

        # 2. 아래에 정령
        flag  = left_right(sr, sc)
        if flag == "left":
            sr, sc = sr + 1, sc - 1
            d = (d - 1) % 4
            continue

        elif flag == "right":
            sr, sc = sr + 1, sc + 1
            d = (d + 1) % 4
            continue

        # 3. 셋다 불가
        break

    ## case1. 초기화
    if sr <= 3:
        arr = [[0] * C for _ in range(R + 3)]
        go_step2 = False
        return go_step2

    update(sr, sc, id, d)
    golem[id] = {
        "row": sr + 1 - 2,
        "exit": (sr + dr[d], sc + dc[d])
    }

    return go_step2

def step2(id):
    global golem, answer

    # 1. bfs
    v = [[False] * C for _ in range(R + 3)]
    er, ec = golem[id]["exit"]
    v[er][ec] = True
    best = er

    q = deque([(id, er, ec)])

    while q:
        cur_id, er, ec = q.popleft()
        for i in range(4):
            nr, nc = er + dr[i], ec + dc[i]
            if not (0 <= nr < R + 3 and 0 <= nc < C):
                continue
            if v[nr][nc]:
                continue
            if arr[nr][nc] == 0:
                continue


            # 이때에 다른 통로로 이동 가능
            if arr[er][ec] < 0 and cur_id != abs(arr[nr][nc]):
                nxt_id = abs(arr[nr][nc])
                q.append((nxt_id, nr, nc))
                v[nr][nc] = True
                if best < nr:
                    best = nr
            elif cur_id == abs(arr[nr][nc]):
                q.append((cur_id, nr, nc))
                v[nr][nc] = True
                if best < nr:
                    best = nr

    if best != 0:
        best -= 2
        answer += best
        


# 1. init
T = 1
# 북 동 남 서
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
for ts in range(1, T + 1):
    R, C, K = map(int,input().split())

    answer = 0
    arr = [[0]*C for _ in range(R+3)]
    golem = {}

    # 2. execute
    for id in range(1, K + 1):
        sc, d = map(int,input().split())
        sc -= 1
        # step1. down
        go_step2 = step1(id, sc, d)

        # step2.
        if go_step2:
            step2(id)
        else:
            golem = {}
    
    print(answer)




