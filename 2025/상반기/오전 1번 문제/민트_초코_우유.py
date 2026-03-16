from collections import deque
def morning():
    global barr
    for r in range(n):
        for c in range(n):
            barr[r][c] += 1

def lunch():
    global farr, barr
    v = [[False]*n for _ in range(n)]
    representaion = []
    for r in range(n):
        for c in range(n):
            if v[r][c]: continue
            q = deque([(r,c)])
            v[r][c] = True
            visited = [(r,c,barr[r][c])]
            ref = farr[r][c]
            while q:
                cr, cc = q.popleft()
                for d in range(4):
                    nr, nc = cr + dr[d], cc + dc[d]
                    if not(0 <= nr < n and 0 <= nc < n) or v[nr][nc]: continue
                    if farr[nr][nc] == ref:
                        v[nr][nc] = True
                        visited.append((nr,nc,barr[nr][nc]))
                        q.append((nr, nc))
            sorted_visited = sorted(visited, key=lambda x: (-x[2], x[0], x[1]))
            rr, rc, _ = sorted_visited[0]
            representaion.append((rr,rc))
            for mr, mc, _ in sorted_visited[1:]:
                barr[rr][rc] += 1
                barr[mr][mc] -= 1
    return representaion

def dinner(representaion):
    # 1. make a order
    global barr, farr
    single = []
    doubble = []
    triple = []
    for rep in representaion:
        ref_r, ref_c = rep
        if farr[ref_r][ref_c] in (1, 2, 4):
            single.append((barr[ref_r][ref_c], ref_r, ref_c, farr[ref_r][ref_c] ))
        elif farr[ref_r][ref_c] in (3, 5, 6):
            doubble.append((barr[ref_r][ref_c], ref_r, ref_c, farr[ref_r][ref_c] ))
        elif farr[ref_r][ref_c] == 7:
            triple.append((barr[ref_r][ref_c], ref_r, ref_c, farr[ref_r][ref_c] ))
    single.sort(key = lambda x: (-x[0], x[1], x[2]))
    doubble.sort(key = lambda x: (-x[0], x[1], x[2]))
    triple.sort(key = lambda x: (-x[0], x[1], x[2]))
    orders = single + doubble + triple

    # 2. propagation
    ans = []
    v = [[False]*n for _ in range(n)]
    for order in orders:
        # 1. init
        B, r, c, ref = order
        if v[r][c]:
            continue
        propa = B - 1
        barr[r][c] -= propa
        # 2. dir
        dir = B % 4
        # 3.
        q = deque([(r,c,propa)])
        while q:
            cr, cc, x = q. popleft()
            nr, nc = cr + dr[dir], cc + dc[dir]
            if not(0 <= nr < n and 0 <= nc < n) or x <= 0: 
                break
            if farr[nr][nc] == ref: 
                q.append((nr,nc,x))
            else:
                y = barr[nr][nc]
                v[nr][nc] = True
                # 3.1 강한 전파 x > y
                if x > y:
                    farr[nr][nc] = ref
                    barr[nr][nc] += 1
                    x -= (y+1)
                    q.append((nr,nc,x))
                # 3.2 약한 전파 x <= y
                else: 
                    farr[nr][nc] |= ref
                    barr[nr][nc] += x
                    break
                              
            
# 1. init
n, t = map(int,input().split())
farr = [list(input()) for _ in range(n)]
for r in range(n):
    for c in range(n):
        if farr[r][c] == "T":
            farr[r][c] = 4
        elif farr[r][c] == "C":
            farr[r][c] = 2
        elif farr[r][c] == "M":
            farr[r][c] = 1
barr = [list(map(int,input().split())) for _ in range(n)]
# 상 하 좌 우
dr = [-1, 1, 0 , 0]
dc = [0 , 0, -1, 1]


# 2. exexute
for turn in range(1,t + 1):
    ######################################
    # 1. morining: update a barr
    ######################################
    morning()
    ######################################
    # 2. lunch: choose a representaion
    ######################################
    representaion = lunch()
    ######################################
    # 3. dinner
    ######################################
    dinner(representaion)
    #################################
    # 4. answer
    ######################################
    ans = [0, 0, 0, 0, 0, 0, 0] # 7, 6, 5, 3, 1, 2, 4
    for r in range(n):
        for c in range(n):
            if farr[r][c] == 7:
                ans[0] += barr[r][c]
            elif farr[r][c] == 6:
                ans[1] += barr[r][c]
            elif farr[r][c] == 5:
                ans[2] += barr[r][c]
            elif farr[r][c] == 3:
                ans[3] += barr[r][c]
            elif farr[r][c] == 1:
                ans[4] += barr[r][c]
            elif farr[r][c] == 2:
                ans[5] += barr[r][c]
            elif farr[r][c] == 4:
                ans[6] += barr[r][c]
    print(*ans)
