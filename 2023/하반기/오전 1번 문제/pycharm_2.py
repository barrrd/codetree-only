from collections import deque
def step1(wid, d):
    global warr, wpos, answer
    # 1. make a candidates
    # 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    candidates = set([wid])
    q = deque([wid])
    can_possible = True
    while q:
        id = q.popleft()
        sr, sc, h, w = wpos[id]["pos"]
        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                nr, nc = r + dr[d], c + dc[d]
                if not(0 <= nr  < L and 0 <= nc < L) or arr[nr][nc] == 2:
                    can_possible = False
                    break
                if warr[nr][nc] != id and warr[nr][nc] != 0 and warr[nr][nc] not in candidates:
                    q.append(warr[nr][nc])
                    candidates.add(warr[nr][nc])
            if not can_possible:
                break
        if not can_possible:
            break

    # 2. update a warr, wpos
    if can_possible: # 이동 가능
        # 2.1 candidates 안에 있는 거 모두 0 으로
        tmp = {id: 0 for id in candidates}
        for cid in candidates:
            sr, sc, h, w = wpos[cid]["pos"]
            for r in range(sr, sr + h):
                for c in range(sc, sc + w):
                    warr[r][c] = 0

        # 2.2 move a candidates
        for cid in candidates:
            sr, sc, h, w = wpos[cid]["pos"]
            nr, nc = sr + dr[d], sc + dc[d]
            wpos[cid]["pos"] = [nr, nc, h, w]
            for r in range(nr, nr + h):
                for c in range(nc, nc + w):
                    if cid != wid and arr[r][c] == 1:
                        tmp[cid] += 1
                    warr[r][c] = cid

        # 3 update a hp and answer
        if wid in tmp.keys():
            del tmp[wid]

        # 3.1
        if tmp: # 두 개 이상
            for id, damage in tmp.items():
                hp = wpos[id]["hp"]
                if damage >= hp:
                    sr, sc, h, w = wpos[id]["pos"]
                    for r in range(sr, sr + h):
                        for c in range(sc, sc + w):
                            warr[r][c] = 0
                    del wpos[id]
                    del answer[id]
                else:
                    answer[id] += tmp[id]
                    wpos[id]["hp"] -= damage

# 1. init
T = int(input())
for ts in range(1, T + 1):
    L, N, Q = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(L)] # 1.
    warr = [[0]*L for _ in range(L)] # 2.
    wpos = {} # 3.
    for wid in range(1, N + 1):
        sr, sc, h, w, k = map(int,input().split())
        sr, sc = sr - 1, sc - 1
        wpos[wid] ={
            "pos" : [sr,sc,h,w],
            "hp": k
        }
        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                warr[r][c] = wid

    # 2. execute
    answer = {i: 0 for i in range(N + 1)}
    for _ in range(Q):
        wid, d = map(int,input().split())
        if wid not in wpos:
            continue
        # step1. move a warrior
        step1(wid, d)


    print(sum( v for v in answer.values()))


