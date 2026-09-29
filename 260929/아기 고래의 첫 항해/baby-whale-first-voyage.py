from collections import deque

def in_range(r, c):
    return 0 <= r < N and 0 <= c < N

def count_answer(r, c):
    global count
    count -= 1
    print(r + 1, c + 1)

def step1():
    global v, r, c, cdr, cdc
    # {0: 상, 1: 하, 2: 좌, 3: 우}
    # 1. can_move
    can_move = False
    ndrc = [(cdr, cdc), (-cdc, cdr), (cdc, -cdr), (-cdr, -cdc)]
    for dr, dc in ndrc:
        nr, nc = r + dr, c + dc

        if not in_range(nr,nc):
            continue
        if v[nr][nc]:
            continue
        if arr[nr][nc]:
            continue

        v[nr][nc] = True
        can_move = True
        break

    # 2. can_move시
    if can_move:
        r, c = nr, nc
        cdr, cdc = dr, dc
    return can_move

def step2():
    global v, r, c, cdr, cdc
    # 1. cands
    cands = []
    best = N*N

    cur_v = [[False]*N for _ in range(N)]
    cur_v[r][c] = True
    q = deque([(r,c,0)])
    while q:
        cr, cc, cdist = q.popleft()
        for dr, dc in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nr, nc = cr + dr, cc + dc

            if not in_range(nr,nc):
                continue
            if cur_v[nr][nc]:
                continue
            if arr[nr][nc] == 1:
                continue

            cur_v[nr][nc] = True

            if not v[nr][nc] and arr[nr][nc] == 0:
                if best > cdist + 1:
                    cands = [(nr,nc, dr, dc)]
                    best = cdist + 1
                elif best == cdist + 1:
                    cands.append((nr,nc, dr, dc))
            else:
                q.append((nr, nc, cdist + 1))

    # 2.
    cands.sort(key = lambda x: (x[0], x[1]))
    target = cands[0]
    r, c, cdr, cdc = target
    v[r][c] = True

    return True
# 1.init
T = 1
for ts in range(1, T + 1):
    # 2. execute
    N, r, c, d = map(int, input().split())
    r, c, d  = r - 1, c - 1, d - 1 # {0: 상, 1: 하, 2: 좌, 3: 우}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cdr, cdc = dirs[d]

    arr = [list(map(int, input().split())) for _ in range(N)]
    v = [[False]*N for _ in range(N)]
    v[r][c] = True

    count = N*N
    for row in arr:
        count -= sum(row)

    count_answer(r,c)
    while count > 0:
        # step1: 인전 탐험 > 4가지 우선 순위 >
        if step1():
            count_answer(r, c)
        elif step2():
            count_answer(r,c)
