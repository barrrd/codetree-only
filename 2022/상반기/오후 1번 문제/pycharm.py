from collections import deque

def make_path(hr, hc):
    path = deque()
    path.append((hr,hc))
    # find the body and tail
    sr, sc = hr, hc
    v = set()
    v.add((sr,sc))
    # 1. body
    while True:
        moved = False
        for i in range(4):
            nr, nc = sr + dr[i], sc + dc[i]
            if not(0 <= nr < n and 0 <= nc < n) or (nr,nc) in v: continue

            if arr[nr][nc] == 2:
                v.add((nr,nc))
                path.append((nr, nc))
                sr, sc = nr, nc
                moved = True
                break
        if moved:
            continue
        # 2. tail
        for i in range(4):
            nr, nc = sr + dr[i], sc + dc[i]
            if not (0 <= nr < n and 0 <= nc < n) or (nr, nc) in v: continue
            if arr[nr][nc] == 3:
                path.append((nr, nc))
                return path

def update(is_4, path):
    global arr, team
    if is_4: # 모든게 연결 x
        for i, (r, c) in enumerate(path):
            if i == 0:
                arr[r][c] = 1
            elif i == len(path) - 1:
                arr[r][c] = 4
            elif i == len(path) - 2:
                arr[r][c] = 3
            else:
                arr[r][c] = 2
        path.pop()
    else: # 모두 연결
        for i, (r,c) in enumerate(path):
            if i == 0:
                arr[r][c] = 1
            elif i == len(path) - 1:
                arr[r][c] = 3
            else:
                arr[r][c] = 2
def step1():
    global arr, team
    # 1. find the nxt head
    for tid in range(1, m + 1):
        path = team[tid]  # head body tail
        hr, hc = path[0]
        is_4 = False
        for i in range(4):
            nr, nc = hr + dr[i], hc + dc[i]
            if not (0 <= nr < n and 0 <= nc < n): continue
            if arr[nr][nc] == 4:
                nxr, nxc = nr, nc
                is_4 = True
                break
        # 2. move a tid and update team
        if is_4:
            # arr[tr][tc] = 4
            path.appendleft((nxr, nxc))
            team[tid] = path
        else:
            path.rotate(1)
            # team[tid] = deque(temp_path)
            # 4. update arr and tid
        update(is_4, path)

def order(turn):
    case = ((turn -1 )// n) % 4
    case_in = (turn - 1) % n
    if case == 0:
        return [(case_in, c) for c in range(n)]
    elif case == 1:
        return [(r, case_in) for r in range(n-1,- 1, -1)]
    elif case == 2:
        return [( (n - 1) - case_in, c) for c in range(n-1, -1, -1)]
    elif case == 3:
        return [(r, (n - 1) -  case_in) for r in range(n)]

def step2(turn, orders):
    global arr, answer, team
    # 1. fin the tid
    candidate = []
    for rr, rc in orders:
        for tid in range(1, m + 1):
            if (rr, rc) in team[tid]:
                candidate = [tid, 1 + team[tid].index((rr,rc))]
                break
        if candidate:
            break
    # 2. update the answer and arr and team
    if candidate:
        ## 1. answer
        tid, k = candidate
        answer += k**2

        ## 2. team
        path = team[tid]
        path.reverse()

        # 3. arr
        hr, hc = path[0]
        tr, tc = path[-1]

        arr[hr][hc] = 1
        arr[tr][tc] = 3

        # ## 3. team
        # team[tid] = path


# 1. init
T = 1
for ts in range(1, T + 1):
        # break
    n, m, k = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(n)]
    answer = 0
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    team = {}
    tid = 1
    for r in range(n):
        for c in range(n):
            if arr[r][c] == 1:
                team[tid] = make_path(r,c)
                tid += 1

    for turn in range(1, k + 1):
        step1()
        orders = order(turn)
        step2(turn, orders)

    print(answer)
