from collections import deque
def in_range(r, c):
    return 0 <= r < N and 0 <= c < N
def count_answer(r, c):
    global count
    count -= 1
    print(r + 1, c + 1)

def step1():
    global r, c, cdr, cdc, v
    is_possible = False
    check_lst = [(cdr, cdc), (-cdc, cdr), (cdc, -cdr), (-cdr, - cdc)]

    for dr, dc in check_lst:
        nr, nc = r + dr, c + dc

        if not in_range(nr,nc):
            continue
        if arr[nr][nc] == 1:
            continue
        if v[nr][nc]:
            continue

        is_possible = True
        cdr, cdc = dr, dc
        r, c = nr, nc
        v[nr][nc] = True
        return  is_possible

    return is_possible

def step2():
    global r, c, cdr, cdc, v
    best_dist = float("INF")
    cand = []

    cur_v = [[False]*N  for _ in range(N)]
    cur_v[r][c] = True
    q = deque([(r,c,0)])

    while q:
        sr, sc, sdist = q.popleft()
        for dr, dc in [(0, -1), (1, 0), (0, 1), (-1, 0)]: # 좌 하 우 상
            nr, nc = sr + dr, sc + dc

            if not in_range(nr,nc):
                continue
            if arr[nr][nc] == 1:
                continue
            if cur_v[nr][nc]:
                continue

            cur_v[nr][nc] = True

            if not v[nr][nc] and arr[nr][nc] == 0:
                if sdist < best_dist:
                    best_dist = sdist
                    cand = [(nr,nc, dr, dc)]
                elif sdist == best_dist:
                    cand.append((nr,nc, dr, dc))

            else:
                q.append((nr, nc, sdist + 1))

    cand.sort(key = lambda x: (x[0],x[1]))
    r, c, cdr, cdc = cand[0]
    v[r][c] = True

    return  True

# 1. init
T = 1
for ts in range(1, T + 1):
    N, r, c, d = map(int, input().split())
    r, c = r - 1, c  - 1
    d -= 1 # d = {1: 상, 2: 하 3: 좌 4: 우}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cdr, cdc = dirs[d]

    arr = [list(map(int, input().split())) for _ in range(N)]

    v = [[False]*N for _ in range(N)]
    v[r][c] = True

    count = N*N
    for a in arr:
        count -= sum(a)

    # 2. execute
    count_answer(r,c)
    while count > 0:
        if step1():
            count_answer(r, c)
        elif step2():
            count_answer(r, c)