from collections import deque
def step1(arr, last):
    cand = []
    best = float("inf")

    for r in range(n):
        for c in range(m):
            if arr[r][c] > 0:
                if arr[r][c] < best:
                    best = arr[r][c]
                    cand = [(arr[r][c], last[r][c], r, c)]
                elif arr[r][c] == best:
                    cand.append((arr[r][c], last[r][c], r, c))

    if not cand:
        return None
    
    # lowest 공격력, highest turn, highest r + c, highest c
    cand.sort(key = lambda x: (x[0], -x[1], -(x[2] + x[3]), -x[3]))
    start = (cand[0][2], cand[0][3])

    return start


def step2(arr, last, sr, sc):
    # 1. choose a target
    cand = []
    best = 0

    for r in range(n):
        for c in range(m):
            if (r,c) != (sr,sc):
                if arr[r][c] > best:
                    cand = [(arr[r][c], last[r][c], r, c)]
                    best = arr[r][c]
                else:
                    cand.append((arr[r][c], last[r][c], r, c))
    if not cand:
        return None
    # h 0, l 1, l 2, l 3
    cand. sort(key = lambda x: (-x[0], x[1], x[2]+ x[3], x[3]))
    tr, tc = cand[0][2], cand[0][3]

    # 2. choose a lazor or turret
    is_razor = False
    ## 우 하 좌 상
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]


    v = [[None]*m for _ in range(n)]
    v[sr][sc] = (sr,sc)
    q = deque([(sr,sc)])
    
    while q:
        cr, cc = q.popleft()

        # case1. fin
        if (cr, cc) == (tr, tc):
            is_razor = True
            break

        # case2. 진행
        for d in range(4):
            nr, nc = (cr + dr[d]) % n, (cc + dc[d]) % m
            if v[nr][nc] is None and arr[nr][nc] > 0:
                q.append((nr,nc))
                v[nr][nc] = (cr, cc)
    
    # 3.1 razor
    power = arr[sr][sc]
    if is_razor:
        path = [(sr,sc)]
        
        rr, cc = tr, tc
        
        while (rr, cc) != (sr, sc):
            path.append((rr, cc))
        

            if (rr,cc) == (tr, tc):
                arr[rr][cc] -= power
            else:
                arr[rr][cc] -= power//2
            
            if arr[rr][cc] < 0:
                arr[rr][cc] = 0

            rr, cc = v[rr][cc]

        return path

    # 3.2 turret
    else:
        dr = [-1, -1, 0, 1, 1, 1, 0, -1]
        dc = [0, 1, 1, 1, 0, -1, -1, -1]

        path = [(sr,sc), (tr,tc)]
        arr[tr][tc] -= power
        if arr[tr][tc] < 0:
            arr[tr][tc] = 0

        for d in range(8):
            nr, nc = (tr + dr[d]) % n, (tc + dc[d]) % m
            if (nr,nc) != (sr,sc) and arr[nr][nc] > 0:
                arr[nr][nc] -= power//2
                path.append((nr,nc))
            if arr[nr][nc] < 0:
                arr[nr][nc] = 0

        return path
        
def step3(arr, path):
    for r in range(n):
        for c in range(m):
            if (r,c) not in path and arr[r][c] > 0:
                arr[r][c] += 1
    

        

# 1. init
T = 1
for ts in range(1, T + 1):
    n, m, k = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(n)]
    last = [[0]*m for _ in range(n)]

    for turn in range(1, k + 1):
        # step0. alive is more than 2
        alive = 0
        for r in range(n):
            for c in range(m):
                if  arr[r][c] > 0 :
                    alive += 1
        if alive <= 1:
            break
        
        # step1.choose a attacker
        ans1 = step1(arr, last)
        if ans1 is None:
            break
        sr, sc = ans1
        last[sr][sc] = turn
        arr[sr][sc] += n + m

        # step2. attack and choose lazor or turret
        ans2 = step2(arr, last, sr, sc)
        if ans2 is None:
            break

        # step3. update a arr
        step3(arr, ans2)

    ################
    # answer
    ################
    ans = 0
    for r in range(n):
        for c in range(m):
            ans = max(ans, arr[r][c])
    print(ans)

        