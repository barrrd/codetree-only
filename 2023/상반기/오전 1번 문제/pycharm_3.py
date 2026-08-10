from collections import deque

def step1(arr, last_attack):
    """
    1.lowest power 
    2.lowest last attack 
    3.highest r + c
    4.highest c
    """
    candidates = []
    best_min = float("inf")

    # 1.alive turret
    for r in range(n):
        for c in range(m):
            if arr[r][c] > 0:
                if arr[r][c] < best_min:
                    best_min = arr[r][c]
                    candidates = [(arr[r][c], last_attack[r][c], (r+c), c)]
                elif best_min == arr[r][c]:
                    candidates.append((arr[r][c], last_attack[r][c], (r+c), c))

    if not candidates:
        return None

    # 2. sort
    candidates.sort(key = lambda x:  (x[0],-x[1],-x[2],-x[3]))

    nr, nc = candidates[0][2] - candidates[0][3], candidates[0][3]

    return nr,nc


def step2(arr, last_attack, except_r, except_c,turn):
    """
    1.highest arr
    2.lowest last_attack
    3. lowest r+c
    4. lowest c
    """
    cand = []
    best = -1

    for r in range(n):
        for c in range(m):
            if (r,c) != (except_r, except_c) and arr[r][c] > 0:
                if arr[r][c] > best:
                    best = arr[r][c]
                    cand = [(arr[r][c], last_attack[r][c], r, c)]
                elif arr[r][c] == best:
                    cand.append((arr[r][c], last_attack[r][c], r, c))
                
    if not cand:
        return None

    # 2. sort
    cand.sort(key = lambda x: (-x[0], x[1], (x[2]+x[3]), x[3]))
    last_attack[except_r][except_c] = turn

    target_r, target_c =  cand[0][2], cand[0][3]

    # 3. choose razor or turret
    ## 우하좌상
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]   

    q = deque([(except_r, except_c)])
    v = [[None]*m  for _ in range(n)]
    v[except_r][except_c] = (except_r, except_c)
    is_razor = False
    
    while q:
        cr, cc = q.popleft()

        # break cond.
        if (cr,cc) == (target_r, target_c):
            is_razor = True
            break
        # process
        for d in range(4):
            nr = (cr + dr[d]) % n
            nc = (cc + dc[d]) % m

            if arr[nr][nc] > 0 and v[nr][nc] is None:
                v[nr][nc] = (cr, cc)
                q.append((nr,nc))

    # 3.1  razor
    power = arr[except_r][except_c]
    if is_razor:
        ## 1. path
        rr, cc = target_r, target_c
        path = [(except_r, except_c)]

        while (except_r, except_c) != (rr, cc):
            path.append((rr,cc))
            if (rr,cc) == (target_r, target_c):
                arr[rr][cc] -= power
            else:
                arr[rr][cc] -= power//2
            
            if arr[rr][cc] <= 0:
                arr[rr][cc] = 0
            
            rr, cc = v[rr][cc]
        
        return path

    # 3.2 turret
    else:
        sr, sc = except_r, except_c
        tr, tc = target_r, target_c
        path = [(tr,tc), (sr,sc)]
        arr[tr][tc] -= power
        if arr[tr][tc] < 0:
            arr[tr][tc] = 0

        ## 12~1
        dr = [-1, -1, 0, 1, 1, 1, 0, -1]
        dc = [0, 1, 1, 1, 0, -1, -1, -1]
        
        for d in range(8):
            nr = (tr + dr[d]) % n
            nc = (tc + dc[d]) % m

            if (nr,nc) != (sr,sc) and arr[nr][nc] > 0:
                path.append((nr,nc))
                if arr[nr][nc] <= power//2:
                    arr[nr][nc] = 0
                else:
                    arr[nr][nc] -= power//2
        
        return path

def step3(arr,path):
    for r in range(n):
        for c in range(m):
            if not(arr[r][c] <= 0 or (r,c) in path):
                arr[r][c] += 1


# 1.init
T = 1
for ts in range(1, T + 1):
    n, m, k = map(int,input().split())

    # new_array
    arr = [list(map(int,input().split())) for _ in range(n)]
    last_attack = [[0]*m for _ in range(n)]

    for turn in range(1, k + 1):
        #################################
        # !. 놓친 조건
        alive = 0

        for r in range(n):
            for c in range(m):
                if arr[r][c] > 0:
                    alive += 1

        if alive <= 1:
            break
        #################################
        # step1. find a  attacker that is lowest power & lowestlast_attack 
        ans1 = step1(arr, last_attack)

        if ans1 is None:
            break
        r1, c1  = ans1
        arr[r1][c1] += n + m

        # step2. attack
        ans2 = step2(arr, last_attack, r1, c1, turn)

        if ans2 is None:
            break

        # step3.
        step3(arr,ans2)


    #############
    # answer
    #############
    ans = 0
    for r in range(n):
        for c in range(m):
            if arr[r][c] > ans:
                ans = arr[r][c]

    print(ans)

