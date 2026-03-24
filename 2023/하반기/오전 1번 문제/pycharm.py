from collections import deque

def can_move(player, d):
    global arr, parr, ppos
    # 1. make a candidates
    candidates = set([player])
    q = deque([player])
    while q:
        pla = q.popleft()
        pr, pc, ph, pw, pk = ppos[pla]
        # 1. make a all list
        for chr in range(pr, pr + ph):
            for chc in range(pc, pc + pw):
                nr, nc = chr + dr[d], chc + dc[d]
                if not(0 <= nr < l and 0 <= nc < l) or arr[nr][nc] == 2:
                    return False, set()
                nxt_pla = parr[nr][nc]
                if nxt_pla != 0 and nxt_pla != pla:
                    if nxt_pla not in candidates:
                        candidates.add(nxt_pla)
                        q.append(nxt_pla)
    return True, candidates

def move(player,lst, d):
    global parr, ppos, answer
    new_parr = [[0]*l for _ in range(l)]
    for r in range(l):
        for c in range(l):
            if parr[r][c] not in lst:
                new_parr[r][c] = parr[r][c]
    for pl in lst:
        pr, pc, ph, pw, pk = ppos[pl]
        ppos[pl][:2] = [pr + dr[d], pc + dc[d]]
        trap = 0
        for cr in range(pr, pr + ph):
            for cc in range(pc, pc + pw):
                nr, nc = cr + dr[d], cc + dc[d]
                if arr[nr][nc] == 1:
                    trap += 1
                new_parr[nr][nc] = pl
        if pl == player: continue
        if pk - trap <= 0:
            del ppos[pl]
            answer[pl] = 0
            for cr in range(pr, pr + ph):
                for cc in range(pc, pc + pw):
                    nr, nc = cr + dr[d], cc + dc[d]
                    new_parr[nr][nc] = 0
        else:
            ppos[pl][-1] = pk - trap
            answer[pl] += trap
    parr = new_parr

def step1(player, d):
    global arr, parr, ppos
    is_possible, push_list = can_move(player, d)
    if is_possible: # 이떄에는 움직일 수 있음
        # print("가능")
        move(player, push_list, d)
    # else:
        # print("불가능")
# 1.init
# T = int(input())
T = 1
# 상 우 하 좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
for ts in range(1, T + 1):
    l, n, q = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(l)]
    ppos = {}
    parr = [[0]*l for _ in range(l)]
    for i in range(n):
        r, c, h, w, k = map(int,input().split())
        r, c = r - 1, c - 1
        ppos[i+1] = [r, c, h, w, k]
        for nr in range(r, r + h):
            for nc in range(c, c + w):
                parr[nr][nc] = i + 1
    orders = [list(map(int,input().split())) for _ in range(q)]
    answer = [0 for _ in range(n + 1)]

    for order in orders:
        player, d = order
        if player not in ppos: continue
        #########################
        # step1. player move
        #########################
        step1(player, d)

    print(sum(answer))
