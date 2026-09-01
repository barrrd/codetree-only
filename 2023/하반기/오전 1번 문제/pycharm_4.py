from collections import deque

def in_range(r,c):
    return 0 <= r < L and 0 <= c < L

def can_move(id, d):
    global warr, wpos
    # 1.nxt pos 기사 여부
    if id in dead:
        return False, set()

    q = deque([id])
    can_possible = True
    cand = {id}
    while q:
        cid = q.popleft()

        cr, cc, h, w, k = wpos[cid]
        for r in range(cr, cr + h):
            for c in range(cc, cc + w):
                nr, nc = r + dr[d], c + dc[d]
                # 벽인 경우
                if not in_range(nr,nc):
                    return False, set()
                if arr[nr][nc] == 2:
                    return False, set()

                if warr[nr][nc] != cid and warr[nr][nc] not in cand and warr[nr][nc] != 0:
                    nid = warr[nr][nc]
                    q.append(nid)
                    cand.add(nid)

    return can_possible, cand

def update(cands, d):
    global warr, wpos
    new_warr = [[0]*L for _ in range(L)]
    for id in wpos:
        if id in dead or id in cands:
            continue
        r, c, h, w, k = wpos[id]
        for cr in range(r, r + h):
            for cc in range(c, c + w):
                new_warr[cr][cc] = id
    
    for id in cands:
        r, c, h, w, k = wpos[id]

        wpos[id] = (r + dr[d], c + dc[d], h, w, k)
        for cr in range(r, r + h):
            for cc in range(c, c + w):
                nr, nc = cr + dr[d], cc + dc[d]
                new_warr[nr][nc] = id

    warr = new_warr

def damage(cands, eid):
    global warr, wpos, answer, dead
    # 1. k update
    for id in cands:
        if id == eid:
            continue

        r, c, h, w, k = wpos[id]
        trap = 0
        # 2. count trap
        for cr in range(r, r + h):
            for cc in range(c, c + w):
                if arr[cr][cc] == 1:
                    trap += 1
                    answer[id] += 1

        # 3. dead 여부
        if trap >= k:
            dead.add(id)
            for cr in range(r, r + h):
                for cc in range(c, c + w):
                    warr[cr][cc] = 0

        else:
            k -= trap
            wpos[id] = (r,c,h,w,k)


# 1. init
T = 1
for ts in range(1, T + 1):
    # 상우하좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    L, N, Q = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(L)]

    warr = [[0]*L for _ in range(L)]
    wpos = {}
    for id in range(1, N + 1):
        r, c, h, w, k = map(int ,input().split())
        r, c  = r - 1, c - 1
        for rr in range(r, r + h):
            for cc in range(c, c + w):
                warr[rr][cc] = id
        wpos[id] = (r,c,h,w,k)

    dead = set()
    answer = {id: 0 for id in range(1, N + 1)}

    # 2. exe
    for _ in range(Q):
        id, d = map(int, input().split())
        # step1. 기사 이동가능한지
        possible, candidates = can_move(id, d)

        # step2.
        if possible:
            update(candidates, d)

            # step3.
            damage(candidates, id)

    fin = 0
    for id in answer:
        if id in dead:
            continue
        fin += answer[id]
    print(fin)
