from collections import deque
def fight(p1, p2, r, c):
    global arr, parr, ppos, answer
    _, _, _, s1, g1 = ppos[p1]
    _, _, _, s2, g2 = ppos[p2]

    # 1. compare to p1 and p2: s + g
    h1, h2 = s1 + g1, s2 + g2
    if h1 < h2: # p2 승
        winner, defeat = p2, p1
        answer[winner - 1] += abs(h1 - h2)
    elif h1 > h2: # p1 승
        winner, defeat = p1, p2
        answer[winner - 1] += abs(h1 - h2)
    else: # 동점인 경우
        if s1 < s2:
            winner, defeat = p2, p1
        else: #s1 > s2:
            winner, defeat = p1, p2

    # 2. defeat
    rw, cw, dw, sw, gw = ppos[winner]
    parr[rw][cw] = 0
    ppos[winner][:2] = [r,c]
    parr[r][c] = winner

    rd, cd, dd, sd, gd = ppos[defeat]
    if gd > 0:
        arr[r][c].append(gd)
        ppos[defeat][4] = 0
    for i in range(4):
        nxt_d = (dd + i) % 4
        nr, nc = r + dr[nxt_d], c + dc[nxt_d]
        if not (0 <= nr < n and 0 <= nc < n) or parr[nr][nc] != 0:
            continue

        ppos[defeat][:3] = [nr, nc, nxt_d]
        parr[nr][nc] = defeat
        if arr[nr][nc] : # 총이 있는 경우
            arr[nr][nc].sort()
            ppos[defeat][4] =  arr[nr][nc].pop()
        break
    # 3. winner
    _, _, _, _, gw = ppos[winner]
    if arr[r][c]:
        if gw > 0:
            arr[r][c].append(gw)
        arr[r][c].sort()
        ppos[winner][-1] = arr[r][c].pop()

# 1.init
T = 1
for ts in range(1, T + 1):
    n, m, k = map(int,input().split())
    arr = [
    [[x] if x > 0 else [] for x in map(int, input().split())]
    for _ in range(n)] # 1.
    ppos = {} # 2.
    parr = [[0]*n for _ in range(n)] # 3.
    for pid in range(1, m + 1):
        x, y, d, s = map(int,input().split())
        x, y = x - 1, y - 1
        ppos[pid] = [x,y,d,s,0]
        parr[x][y] = pid

    # 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    answer = [0 for _ in range(m)]

    for turn in range(1, k + 1):
        ##################################################
        # step1. player move and player or empty
        ##################################################
        for pid in range(1, m + 1):
            if pid in ppos:
                r, c, d, s, g = ppos[pid]
                # 1. nr, nc 초기화
                nr, nc = r + dr[d], c + dc[d]
                parr[r][c] = 0
                if not (0 <= nr < n and 0 <= nc < n):
                    d = (d + 2) %4
                    nr, nc = r + dr[d], c + dc[d]
                ppos[pid][2] = d
                # 2. player or empty or gun
                if parr[nr][nc] != 0:  # player
                    fight(pid, parr[nr][nc], nr, nc)
                else:  # not player
                    # empty + gun
                    parr[r][c] = 0
                    ppos[pid][:3] = [nr, nc, d]
                    parr[nr][nc] = pid
                    if arr[nr][nc] != []:  # only gun
                        if g > 0:
                            arr[nr][nc].append(g)
                        arr[nr][nc].sort()
                        ppos[pid][4] = arr[nr][nc].pop()
    print(*answer)

