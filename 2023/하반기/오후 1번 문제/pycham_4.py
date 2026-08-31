from collections import  deque

def in_range(r,c):
    return 0 <= r < N and  0 <= c < N

def cal_dist(r1,c1,r2,c2):
    return (r1 - r2)**2 + (c1 -c2)**2

def collision_interaction(id, mul, dr, dc, turn):
    global arr, sdct, answer, alive
    # 1. 충돌 후의 위치
    sdct[id]["stun"] = turn + 1
    r, c = sdct[id]["pos"]
    arr[r][c] = 0
    q = deque([(id, mul)])
    while q:
        cid, m = q.popleft()
        # sdct[cid]["turn"] = turn + 1
        cr, cc = sdct[cid]["pos"]
        # arr[cr][cc] = 0

        nr, nc = cr + dr*m, cc + dc*m
        # case1. 밖
        if not in_range(nr, nc):
            sdct[cid]["alive"] = False
            alive -= 1
            continue

        # case2. 벽 안
        ## case 2.1 다른 산타
        if arr[nr][nc] != 0:
            nid = arr[nr][nc]
            if sdct[nid]["alive"]:
                q.append((nid,1))

        arr[nr][nc] = cid
        sdct[cid]["pos"] = (nr, nc)


def step1(turn):
    global rr, rc, arr, sdct, answer, alive
    # 1. 가까운 산타
    cand = []
    best_min = float("inf")
    for id in sorted(sdct):
        if not sdct[id]["alive"]:
            continue
        r, c = sdct[id]["pos"]

        dist = cal_dist(rr, rc, r, c)
        if dist < best_min:
            cand = [(r, c, id)]
            best_min = dist
        elif dist == best_min:
            cand.append((r,c,id))

    target = sorted(cand, key= lambda x: (-x[0], -x[1]))[0]

    # 2. 이동
    tr, tc, tid = target
    n_rr, n_rc = -1, -1
    best_min = cal_dist(rr, rc, tr, tc)
    ndr, ndc = 0,0

    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0,1), (1,1), (1,0), (1, -1), (0, -1)]:
        nr, nc = rr + dr, rc + dc
        if not in_range(nr,nc):
            continue

        ndist  = cal_dist(nr, nc, tr, tc)
        if ndist < best_min:
            best_min = ndist
            n_rr, n_rc = nr, nc
            ndr, ndc = dr, dc

    rr, rc = n_rr, n_rc

    # 3. 다음 루돌프 == 산타
    if arr[rr][rc] != 0:
        sid = arr[rr][rc]
        answer[sid] += C
        collision_interaction(sid, C, ndr, ndc, turn)

def step2(turn):
    global rr, rc, arr, sdct, answer, alive
    # 1. 산타 움직임 that 가까운 위치
    for id in sorted(sdct):
        if sdct[id]["alive"] and sdct[id]["stun"] < turn:
            r, c = sdct[id]["pos"]
            n_rr, n_rc = -1, -1
            ndr, ndc = 0, 0
            dist = cal_dist(rr, rc, r, c)

            for dr, dc in [(-1, 0), (0, 1), (1,0), (0, -1)]: # 상 우 하 좌
                nr, nc = r + dr, c + dc

                if not in_range(nr, nc):
                    continue
                if arr[nr][nc] != 0:
                    continue

                ndist = cal_dist(nr, nc, rr, rc)

                if ndist < dist:
                    dist = ndist
                    n_rr, n_rc = nr, nc
                    ndr, ndc = dr, dc

            # 이동 불가능
            if (n_rr, n_rc) == (-1, -1):
                continue

            # 이동 가능
            sdct[id]["pos"] = (n_rr, n_rc)
            arr[r][c] = 0
            arr[n_rr][n_rc] = id
            # case1. 루돌프와  충돌
            if (n_rr, n_rc) == (rr, rc):
                answer[id] += D
                collision_interaction(id, D , -ndr, -ndc, turn)


# 1. init
T = 1
for ts in range(1 ,T + 1):
    ####################
    # if ts == 2:
    #     break
    ####################
    N, M, P, C, D = map(int,input().split())
    rr, rc = map(int, input().split())
    rr, rc = rr - 1, rc - 1

    arr = [[0]*N for _ in range(N)]
    sdct = {}
    for _ in range(P):
        id, r, c = map(int,input().split())
        r, c = r - 1, c - 1
        arr[r][c] = id
        sdct.setdefault(id,{
            "pos": (r,c),
            "stun": 0,
            "alive": True
        })

    answer = {id: 0 for id in range(1, P + 1)}
    alive = P

    # 2.exe
    for turn in range(1, M + 1):
        # step1. 루돌프 움직임 ;  다음 위치 > 충돌 > 상호작용 > 기절
        step1(turn)

        if alive == 0:
            break

        # step2. 산타 움직임 ;  다음 위치 > 충돌 > 상호작용 > 기절
        step2(turn)

        if alive == 0:
            break

        for id in sdct:
            if sdct[id]["alive"]:
                answer[id] += 1

    ans = []
    for id in sorted(sdct):

        ans.append(answer[id])
    print(*ans)
