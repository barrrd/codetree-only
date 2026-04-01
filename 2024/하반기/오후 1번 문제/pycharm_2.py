from collections import deque
def step1():
    # 1. make a parent array
    parent = [[None]*n for _ in range(n)]
    parent[sr][sc] = [sr,sc]

    q = deque([(sr,sc)])
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    is_possible = False
    while q:
        cr, cc = q.popleft()
        if (cr, cc) == (er, ec):
            is_possible = True
            break
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]

            if not(0 <= nr < n and 0 <= nc < n):
                continue
            if parent[nr][nc] or arr[nr][nc] == 1:
                continue

            parent[nr][nc] = [cr, cc]
            q.append((nr,nc))

    if is_possible:
        path = []
        path.append((er,ec))

        cr, cc = er, ec
        while True:
            pr, pc = parent[cr][cc]


            if (pr, pc) == (sr, sc):
                break

            path.append((pr, pc))
            cr, cc = pr, pc

        # path.reverse()
        return is_possible, path
    else:
        return is_possible, []


def get_pos(f, l, d):
    if d == 0: # 상
        return sr - f, sc + l
    elif d == 1: # 하
        return sr + f, sc + l
    elif d == 2: # 좌
        return sr + l, sc - f
    elif d == 3: # 우
        return sr + l, sc + f

def make_blind(d):
    # catchcd = 0
    # 1. make a view
    view = [[False] * n for _ in range(n)]
    for f in range(1, n):
        for l in range(-f, f + 1):
            r, c = get_pos(f, l, d)
            if 0 <= r < n and 0 <= c < n:
                view[r][c] = True

    # 2. make a shadow
    shadow = [[False] * n for _ in range(n)]
    catchcd = 0
    ## 1. find the f, l
    for f in range(1, n):
        for l in range(-f, f + 1):
            r, c = get_pos(f, l, d)
            if not (0 <= r < n and 0 <= c < n):
                continue
            if not view[r][c]:
                continue
            if shadow[r][c]:
                continue
            if warr[r][c] == 0:
                continue

            catchcd += warr[r][c]

            ## 2. shadow
            for nf in range(f + 1, n):
                gap = nf - f
                if l == 0: # 중앙
                    left_l, right_l = 0, 0
                elif l < 0: # minus side
                    left_l, right_l = l - gap, l
                elif l > 0: # plus side
                    left_l, right_l = l, l + gap

                for nl in range(left_l, right_l + 1):
                    nr, nc = get_pos(nf, nl, d)
                    if 0 <= nr < n and 0 <= nc < n:
                        shadow[nr][nc] = True
    # 3. blind
    blind = [[False] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if view[r][c] and not shadow[r][c]:
                blind[r][c] = True

    return  catchcd, blind

def step2():
    global marr, answer
    # 모든 전사 이동 거리, 돌 전사, 메두사를 공격한 전사수
    # 1. 현재 위치에 전사 여부
    if warr[sr][sc] > 0:
        warr[sr][sc] = 0

    # 2. make a blind map
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]


    best_catecd = -1
    blind = []
    dir =  -1
    for i in range(4):
        catchcd, bli = make_blind(i)
        if best_catecd < catchcd:
            best_catecd = catchcd
            blind = bli
            dir = i
    answer[1] += best_catecd

    return blind

def step3(blind):
    global warr, answer
    new_warr = [row[:] for row in warr]

    # 1. 두번 이동
    for r in range(n):
        for c in range(n):
            if warr[r][c] > 0 and not blind[r][c]:
                people = warr[r][c]
                cr, cc = r, c

                for move_cnt in range(1, 2 + 1):
                    moved = False
                    if move_cnt == 1:
                        # 상하좌우
                        drc = [(-1,0),(1,0),(0,-1),(0,1)]
                    elif move_cnt == 2:
                        # 좌우상하
                        drc = [(0,-1),(0,1),(-1,0),(1,0)]


                    for dr, dc in drc:
                        nr, nc = cr + dr, cc + dc
                        c_dist, n_dist = abs(cr - sr) + abs(cc - sc), abs(nr - sr) + abs(nc - sc)
                        if not(0 <= nr < n and  0 <= nc < n):
                            continue
                        if blind[nr][nc]:
                            continue

                        if c_dist > n_dist:
                            moved = True
                            break

                    if moved:
                        cr, cc = nr, nc
                        answer[0] += people
                        if (cr, cc) == (sr, sc):
                            answer[2] += people
                        # print(f"메두사{sr, sc}, 전사:{cr, cc}")
                    else:
                        break


                new_warr[r][c] -= people
                if (cr, cc) != (sr, sc):
                    new_warr[cr][cc] += people

    warr = new_warr

# 1.init
T = 1
for ts in range(1, T + 1):
    n, m = map(int,input().split())
    sr, sc, er, ec = map(int,input().split())
    warr = [[0]*n for _ in range(n)] # 1.
    for _ in range(1):
        temp = list(map(int,input().split()))
        for i in range(m):
            ri, ci = temp[2*i: 2*(i + 1)]
            warr[ri][ci] += 1
    arr = [list(map(int,input().split())) for _ in range(n)] # 2.

    # step1. make a sp that snake's path and move a snake
    # 1. make a sp
    is_possible, path = step1()
    if not is_possible:
        print(-1)
    # 2. update a sr, sc
    else:
        while path:
            answer = [0, 0, 0] # 모든 전사 이동 거리, 돌 전사, 메두사를 공격한 전사수
            nxt_r, nxt_c = path.pop()
            if (nxt_r, nxt_c) == (er, ec):
                print(0)
                break
            else:
                sr, sc = nxt_r, nxt_c
                # step2. snake's view
                blind = step2()
                # step3. move warrior
                step3(blind)
                print(*answer)
