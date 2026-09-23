from collections import deque

def in_range(r,c):
    return 0 <= r < N and  0 <= c < N

def cal_dist(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1 - c2)**2

def interaction(tid, dr, dc):
    global sdct, arr, alive, answer
    # 1. 부딛힌 산타
    cr, cc = sdct[tid]["pos"]
    cid = tid

    while True:
        nid = arr[cr][cc]

        arr[cr][cc] = cid
        sdct[cid]["pos"] = (cr, cc)

        if nid == 0:
            break

        nr, nc = cr + dr, cc + dc

        if not in_range(nr,nc):
            sdct[nid]["alive"] = False
            alive -= 1
            break

        cid = nid
        cr, cc = nr, nc


def collision(tid, val, dr, dc, turn):
    global sdct, arr, alive, answer
    # 1. 점수 획득
    answer[tid] += val

    # 2. 기절
    sdct[tid]["stun"] = turn + 1

    # 3. 산타 움직임
    tr, tc = sdct[tid]["pos"]
    arr[tr][tc] = 0
    nr, nc = tr + val*dr, tc + val*dc

    if not in_range(nr, nc):
        sdct[tid]["alive"] = False
        alive -= 1
    else:
        # 2. 상호작용
        ## Case1. not 상호작용
        sdct[tid]["pos"] = (nr, nc)
        if arr[nr][nc] == 0:
            arr[nr][nc] = tid

        ## Case2. 상호작용
        else:
            interaction(tid, dr, dc)

def step1(turn):
    global arr, sdct, rr, rc, answer, alive
    # 1. 루돌프 움직임
    ## 1. 후보 위치 찾기
    cands = []
    best_min = float("inf")
    for sid in sorted(sdct):
        if not sdct[sid]["alive"]:
            continue

        sr, sc = sdct[sid]["pos"]
        dist = cal_dist(rr, rc, sr, sc)

        if dist < best_min:
            cands = [(sid, sr, sc)]
            best_min = dist
        elif dist == best_min:
            cands.append((sid, sr, sc))

    cands.sort(key = lambda x: (-(x[1]), -x[2]))
    target = cands[0]

    ## 1.2 루돌프 움직음
    tid, tr, tc = target
    best_min = cal_dist(rr,rc,tr,tc)
    nrr, nrc = -1, -1
    ndr, ndc = 0, 0

    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0,1), (1,1), (1,0), (1, -1), (0, -1)]:
        nr, nc = rr + dr, rc + dc

        if not in_range(nr,nc):
            continue

        if best_min > cal_dist(nr,nc, tr, tc):
            ndr, ndc = dr, dc
            nrr, nrc = nr, nc
            best_min = cal_dist(nr,nc, tr, tc)

    rr, rc = nrr, nrc

    # 2. 충돌
    if (rr, rc) == (tr, tc):
        collision(tid, C, ndr, ndc, turn)

def step2(turn):
    global arr, sdct, rr, rc, answer, alive

    for sid in sorted(sdct):

        # 1. dead
        if not sdct[sid]["alive"]:
            continue

        # 2. 기절
        if sdct[sid]["stun"] >= turn:
            continue

        # 3.
        sr, sc = sdct[sid]["pos"]

        best_min = cal_dist(sr, sc, rr, rc)

        nr, nc = -1, -1
        ndr, ndc = 0, 0

        for dr, dc in [(-1,0), (0,1), (1,0), (0,-1)]:
            tr, tc = sr + dr, sc + dc

            if not in_range(tr, tc):
                continue

            if arr[tr][tc] != 0:
                continue

            dist = cal_dist(tr, tc, rr, rc)

            if dist < best_min:
                best_min = dist
                nr, nc = tr, tc
                ndr, ndc = dr, dc

        if nr == -1:
            continue

        # 4.
        arr[sr][sc] = 0

        sdct[sid]["pos"] = (nr, nc)

        # 5. 층덜
        if (nr, nc) == (rr, rc):
            collision(sid, D , -ndr, -ndc, turn)

        else:
            arr[nr][nc] = sid

# 1.init
T = 1
for ts in range(1, T + 1):
    N, M, P, C, D = map(int, input().split())
    rr, rc = map(int,input().split())
    rr, rc = rr - 1, rc - 1

    sdct = {}
    arr = [[0]*N for _ in range(N)]
    for _ in range(P):
        id, sr, sc = map(int, input().split())
        arr[sr - 1][ sc - 1] = id
        sdct.setdefault(id,{
            "pos": (sr - 1,sc - 1),
            "stun": 0,
            "alive": True
        })
    answer = [0] * (P + 1)
    alive = P

    for turn in range(1, M + 1):
        # step1. 루돌프 > 충돌 > 상호작용 > 기절
        step1(turn)

        if alive == 0:
            break

        # step2. 산타 > 충돌 > 상호작용 > 기절
        step2(turn)

        if alive == 0:
            break

        # step3. 살아있는 산타 +1점
        for sid in sdct:
            if sdct[sid]["alive"]:
                answer[sid] += 1

        if alive == 0:
            break

    print(*answer[1:])