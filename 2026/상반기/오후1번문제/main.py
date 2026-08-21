from collections import deque

def step1():
    global sr, sc, cdr, cdc, turn, marr
    is_possible = False
    check_lst = [(cdr, cdc), (-cdc, cdr), (cdc, -cdr), (-cdr, -cdc)]
    # 우선순위
    for dr, dc in check_lst:
        nr, nc = sr + dr, sc + dc
        if not(0 <= nr < N and 0 <= nc < N):
            continue
        if marr[nr][nc] > 0:
            continue

        marr[nr][nc] = 2
        sr, sc = nr, nc
        cdr, cdc = dr, dc
        turn -= 1

        is_possible = True
        break

    return is_possible

def step2():
    global sr, sc, cdr, cdc, turn, marr
    # 1. candidates
    best_dist = float("INF")
    cand = []

    q = deque([(sr, sc, 0)])
    v = [[False]*N for _ in range(N)]
    v[sr][sc] = True

    while q:
        cr, cc, cdist = q.popleft()

        if cdist >= best_dist:
            continue

        for dr, dc in [(0, -1), (1, 0), (0, 1), (-1, 0)]: # 좌 하 우 상
            nr, nc = cr + dr, cc + dc

            # 이동 불가능
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if marr[nr][nc] == 1:
                continue
            if v[nr][nc]:
                continue

            # 이동 가능
            ndist = cdist + 1
            v[nr][nc] = True
            if marr[nr][nc] == 2:
                q.append((nr,nc,ndist))
            elif marr[nr][nc] == 0:
                if ndist < best_dist:
                    best_dist = ndist
                    cand = [(nr, nc)]
                elif ndist == best_dist:
                    cand.append((nr, nc))
    cand.sort(key= lambda x: (x[0], x[1]))
    tr, tc = cand[0]

    # 2. 이동 후 방향
    dist = [[-1]*N for _ in range(N)]
    dist[sr][sc] = 0
    q = deque([(sr,sc)])
    found = False
    while q:
        cr, cc = q.popleft()
        for dr, dc in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # 좌 하 우 상
            nr, nc = cr + dr, cc + dc

            # 이동 불가능
            if not (0 <= nr < N and 0 <= nc < N):
                continue
            if marr[nr][nc] == 1:
                continue

            nxt_dist = dist[cr][cc] + 1

            if dist[nr][nc] != -1:
                continue
            else:
                dist[nr][nc] = nxt_dist
                q.append((nr,nc))


            if (nr, nc) == (tr, tc):
                cdr, cdc = dr, dc
                sr, sc = nr, nc
                found = True
                break
        if found:
            break

    # 3. update
    marr[tr][tc] = 2
    turn -= 1

# 1. init
T = int(input())
for ts in range(1, T + 1):
    N, r, c, d = map(int, input().split())
    sr, sc, d = r - 1, c - 1, d - 1
    # 1: 암초 2: visited
    marr = [list(map(int, input().split())) for _ in range(N)]

    turn = N*N - 1
    for m in marr:
        turn -= sum(m)
    marr[sr][sc] = 2

    # 상 하 좌 우
    dr0 = [-1, 1, 0, 0]
    dc0 = [0, 0, -1, 1]
    cdr, cdc = dr0[d], dc0[d]

    print(sr + 1, sc + 1)
    # 2. execute
    while turn > 0:
        if step1():
            print(sr + 1, sc + 1)
        else:
            step2()
            print(sr + 1, sc + 1)
