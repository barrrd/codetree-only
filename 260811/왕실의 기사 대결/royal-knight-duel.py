from collections import deque

def can_propagtion(id, d):
    global wpos
    q = deque([id])

    is_possible = True
    cand = set([id])

    while q:
        cur_id = q.popleft()
        sr, sc, h, w = wpos[cur_id]["pos"]
        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                nr, nc = r + dr[d], c + dc[d]

                if not(0 <= nr < l and 0 <= nc <l) or arr[nr][nc] == 2:
                    is_possible = False
                    break

                if warr[nr][nc] != cur_id and warr[nr][nc] != 0 and warr[nr][nc] not in cand:
                    nxt_id = warr[nr][nc]
                    cand.add(nxt_id)
                    q.append(nxt_id)

            if not is_possible:
                break

        if not is_possible:
            break

    return is_possible, cand

def update(cand, d):
    global wpos
    # 1. remove the cand
    for cur_id in cand:
        sr, sc, h, w = wpos[cur_id]["pos"]

        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                warr[r][c] = 0

    # 2. warrior move
    for cur_id in cand:
        sr, sc, h, w = wpos[cur_id]["pos"]

        nr, nc = sr + dr[d], sc + dc[d]

        wpos[cur_id]["pos"] = [nr, nc, h , w]
    # 3. update
    for cur_id in cand:
        sr, sc, h, w = wpos[cur_id]["pos"]

        for rr in range(sr, sr + h):
            for cc in range(sc, sc + w):
                warr[rr][cc] = cur_id

def damage(cand, id):
    global answer, dead
    for cur_id in cand:

        if cur_id == id:
            continue

        sr, sc, h, w = wpos[cur_id]["pos"]
        power = 0

        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                if arr[r][c] == 1:
                    power += 1

        answer[cur_id] += power
        wpos[cur_id]["hp"] -= power

        if wpos[cur_id]["hp"] <= 0:
            for r in range(sr, sr + h):
                for c in range(sc, sc + w):
                    warr[r][c] = 0
            dead.add(cur_id)

def step(id, d):
    global arr, wpos, warr, dead
    # 0. 이미 죽은 기사라면 아무것도 하지 않음
    if wpos[id]["hp"] <= 0:
        return

    # 1. can_propagation
    can_move, candidates = can_propagtion(id, d)

    # 2.update wpos, warr
    if not can_move:
        return
    update(candidates, d)

    # 3. damage
    damage(candidates, id)


# 1.init
T = 1

# 0: 상, 1: 우, 2: 하, 3: 좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

for ts in range(1, T + 1):
    l, n, q = map(int,input().split())

    arr = [list(map(int,input().split())) for _ in range(l)]
    wpos = {}
    warr = [[0]*l for _ in range(l)]

    for id in range(1, n + 1):
        r, c, h, w, k = map(int,input().split())
        r, c = r - 1, c- 1
        wpos[id] = {
            "pos": [r,c,h,w],
            "hp": k
        }
        for sr in range(r, r + h):
            for sc in range(c, c + w):
                warr[sr][sc] = id

    #2.execute
    answer = { id: 0 for id in range(1, n + 1)}
    dead = set()

    for _ in range(q):
        id, d = map(int,input().split())

        # step. 기사 이동 and 대결
        step(id, d)

        if len(dead) == n:
            break

    final = 0
    for i in answer.keys():
        if i not in dead:
            final += answer[i]
    print(final)

