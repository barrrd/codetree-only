from collections import deque

def step1():
    global arr
    # 1. 공격자 당할
    candidates = []
    for r in range(n):
        for c in range(m):
            if arr[r][c][0] == 0: continue
            candidates.append([r, c, *arr[r][c]])

    candidates.sort(key = lambda x: (x[2], -x[3], -(x[0]+x[1]), -x[1]), reverse = True)
    attacker = candidates.pop()
    target = candidates[0]

    # 2. update a 공격력
    cr, cc, _, _ = attacker
    attacker[2] += n + m
    attacker[3] = turn
    arr[cr][cc] = attacker[2:]
    return attacker, target

def step2(at, ta):
    global arr
    ar, ac = at[:2]
    damage = arr[ar][ac][0]
    tr, tc = ta[:2]

    # 1. razor
    # 우하좌상
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]
    parent = [[None]*m for _ in range(n)]
    parent[ar][ac] = [ar,ac]
    possible = False
    q = deque([(ar, ac)])

    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = (cr + dr[i]) % n, (cc + dc[i]) % m
            if arr[nr][nc][0] == 0 or parent[nr][nc] != None: continue
            parent[nr][nc] = [cr,cc]
            if (nr, nc) == (tr, tc):
                possible = True
                break
            else:
                q.append((nr,nc))
        if possible:
            break
    if possible:
        # order = [(tr, tc)]
        order = []
        q = deque([(tr,tc)])
        while q:
            sr, sc = q.popleft()
            srr, scc = parent[sr][sc]
            if (srr,scc) == (ar, ac):
                break
            order.append((srr,scc))
            q.append((srr, scc))
        order.reverse()
        # 2.
        if arr[tr][tc][0] - damage > 0:
            arr[tr][tc][0] -= damage
        else:
            arr[tr][tc][0] = 0
        for aar, aac in order:
            if arr[aar][aac][0] - damage//2 > 0:
                arr[aar][aac][0] -= damage//2
            else:
                arr[aar][aac][0] = 0
            # 3. update
        for r in range(n):
            for c in range(m):
                if arr[r][c][0] == 0 or  (r, c) in order or (r, c) == (ar, ac) or (r, c) == (tr,tc): continue

                arr[r][c][0] += 1

    else: # 2. turret
        candidates = []
        check_lst = [[0, -1], [-1, -1], [-1,0], [-1,1],[0,1], [1,1],[1,0],[1,-1]]
        for plus_r, plus_c in check_lst:
            nr, nc = (tr + plus_r) % n, (tc + plus_c) % m
            if arr[nr][nc][0] == 0: continue
            if (nr, nc) == (ar, ac): 
                continue
            candidates.append((nr,nc))
        # 2.
        if arr[tr][tc][0] - damage > 0:
            arr[tr][tc][0] -= damage
        else:
            arr[tr][tc][0] = 0
        for aar, aac in candidates:
            if arr[aar][aac][0] - damage//2 > 0:
                arr[aar][aac][0] -= damage//2
            else:
                arr[aar][aac][0] = 0
        # 3. update
        for r in range(n):
            for c in range(m):
                if arr[r][c][0] == 0 or (r,c) in candidates or  (r,c) == (ar,ac) or (r,c) == (tr, tc): continue
                arr[r][c][0] += 1

# 1.init
# T = int(input())
T = 1
for ts in range(1, T + 1):
    n, m, k = map(int, input().split())
    arr = [list(map(int,input().split())) for _ in range(n)]
    for r in range(n):
        for c in range(m):
            arr[r][c] = [arr[r][c], 0]
    for turn in range(1, k + 1):
        alive = 0
        for r in range(n):
            for c in range(m):
                if arr[r][c][0] > 0:
                    alive += 1
        if alive <= 1:
            break
        #####################################
        # step1. choose a attacker
        #####################################
        attaker, target = step1()
        #####################################
        # step2. choose a 공격 당할
        #####################################

        step2(attaker, target)
    ####################
    # 출력
    ###################
    answer = -1
    for r in range(n):
        for c in range(m):
            answer = max(answer, arr[r][c][0])
    print(answer)


