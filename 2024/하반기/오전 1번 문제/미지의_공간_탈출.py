from collections import deque
def step1():
    # 1. find the arr[r][c]
    sr, sc = -1, -1
    found = False
    for r in range(n):
        for c in range(n):
            if arr_2d[r][c] == 3:
                sr, sc = r, c
                found = True
                break
        if found:
            break

    # 2. find the path which is 3 and make a max and min r, c
    max_r, min_r, max_c, min_c = -1, n, -1, n
    path = [(sr,sc)]
    q = deque([(sr,sc)])
    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]

            if not(0 <= nr < n and 0 <= nc < n) or (nr,nc) in path or arr_2d[nr][nc] != 3:
                continue

            max_r, max_c = max(max_r, nr), max(max_c, nc)
            min_r, min_c = min(min_r, nr), min(min_c, nc)

            path.append((nr,nc))
            q.append((nr,nc))

    # 3. find the exits pos and exit phase
    exit_phase = - 1
    er, ec = -1, -1
    pr, pc = -1, -1
    found_0 = False
    for r, c in path:
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if not(0 <= nr < n and 0 <= nc < n):
                continue
            if arr_2d[nr][nc] == 0:
                found_0 = True
                exit_phase = i
                pr, pc = r, c
                er, ec = nr, nc
                break
        if found_0:
            break

    # 4. phase
    c_3d = -1
    if exit_phase == 0: # 동
        c_3d = max_r - pr
    elif exit_phase == 1: # 서
        c_3d = pr - min_r
    elif exit_phase == 2: # 남
        c_3d = pc - min_c
    elif exit_phase == 3: # 북
        c_3d = max_c- pc

    return exit_phase, c_3d, er, ec

def step2(exit_phase, c_3d):
    # 1. find the start point
    sr, sc = -1, -1
    found = False
    for r in range(m):
        for c in range(m):
            if arr_3d[4][r][c] == 2:
                sr, sc = r, c
                found = True
                break
        if found:
            break
    # 2. make a v and bfs
    tp, tr, tc = exit_phase, m - 1, c_3d

    side_move = {
        (4,0): (lambda r,c: 0, lambda r, c: m - 1 - r, 0),
        (4,1): (lambda r,c: 0, lambda r, c: r, 1),
        (4,2): (lambda r, c: 0, lambda r, c: c, 2),
        (4,3): (lambda r, c: 0, lambda r, c: m - 1 - c, 3),

        (0, 0): (lambda r, c: r, lambda r, c: 0, 3),
        (0, 1): (lambda r, c: r, lambda r, c: m - 1, 2),
        (0, 3): (lambda r, c: 0, lambda r, c: m - 1 - c, 4),

        (1, 0): (lambda r, c: r, lambda r, c: 0, 2),
        (1, 1): (lambda r, c: r, lambda r, c: m - 1, 3),
        (1, 3): (lambda r, c: c, lambda r, c: 0, 4),

        (2, 0): (lambda r, c: r, lambda r, c: 0, 0),
        (2, 1): (lambda r, c: r, lambda r, c: m - 1, 1),
        (2, 3): (lambda r, c: m - 1, lambda r, c: c, 4),

        (3, 0): (lambda r, c: r, lambda r, c: 0, 1),
        (3, 1): (lambda r, c: r, lambda r, c: m - 1, 0),
        (3, 3): (lambda r, c: 0, lambda r, c: m - 1 - c, 4)
    }
    phase =[[[(m**2)*5]*m for _ in range(m)] for _ in range(5)]
    phase[4][sr][sc] = 0

    q = deque([(sr,sc,4,0)])
    answer = 0
    while q:
        cr, cc, cp, turn = q.popleft()

        if (cr,cc,cp) == (tr,tc,tp):
            answer = turn
            break

        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            nxt_turn, np = turn + 1, cp

            # 격자 밖
            if not(0 <= nr < m and 0 <= nc < m):
                if np in [0,1,2,3] and i == 2:
                    continue
                func_r, func_c, np = side_move[(np,i)]
                nr, nc = func_r(cr,cc), func_c(cr,cc)

            if phase[np][nr][nc] <= nxt_turn or arr_3d[np][nr][nc] == 1: # 이미 방문
                continue

            phase[np][nr][nc] = nxt_turn
            q.append((nr,nc,np,nxt_turn))

    return answer

def step3(orders, turn):
    # 1. 초기화
    array = [[0]*n for _ in range(n)]
    for order in orders:
        ri, ci, d, v = order
        array[ri][ci] = 1
    # 2.
    t = 1
    while t <= n**2:
        new_array = [row[:] for row in array]
        for id in range(len(orders)):
            ri, ci, d, v = orders[id]
            if t // v > 0 and t % v == 0:
                nr, nc = ri + dr[d], ci + dc[d]

                if not(0 <= nr < n and 0 <= nc < n) or array[nr][nc] > turn:
                    continue
                if arr_2d[nr][nc] != 0:
                    continue

                new_array[nr][nc] = t
                orders[id] = [nr, nc, d, v]
        t += 1
        array = new_array

    # 3. bfs
    if array[er][ec] <= turn and array[er][ec] != 0:
        return -1, array
    else:
        sr, sc = er, ec  # 2d 시작점
        array[sr][sc] = turn

        q = deque([(sr, sc, turn)])

        while q:
            cr, cc, ct = q.popleft()
            if arr_2d[cr][cc] == 4:
                return ct, array

            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]
                nt = ct + 1

                if not(0 <= nr < n  and 0 <= nc < n):
                    continue
                if arr_2d[nr][nc] in [1,3] or 0 < array[nr][nc] <= nt:
                    continue

                array[nr][nc] = nt
                q.append((nr,nc,nt))
        return -1, array

# 1. init
T = 1
for ts in range(1, T + 1):
    n, m, f = map(int,input().split())
    arr_2d = [list(map(int,input().split())) for _ in range(n)] # 1. 2d
    # 0: 동, 1: 서 2: 남, 3: 북, 4: 윗면
    arr_3d = [[list(map(int,input().split())) for _ in range(m)] for _ in range(5)]  # 2. 3d
    orders = [list(map(int,input().split())) for _ in range(f)] # 3. f
    # 동 서 남 북
    dr = [0, 0, 1, -1]
    dc = [1, -1, 0, 0]
    # 2. execute
    # step1. find the exit phase and pos
    exit_phase, c_3d, er, ec  = step1()

    # step2. 3d -> 2d
    turn = step2(exit_phase, c_3d)
    turn += 1

    # step3. 이상현상
    answer, array = step3(orders, turn)
    print(answer)
