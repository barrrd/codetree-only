from collections import deque
def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def step1(turn):
    global tarr, tdct, count, answer
    # 1. bfs
    for id in sorted(tdct.keys()):
        found = False
        r, c = tdct[id]

        q = deque([(r,c)])
        parent = [[None] * N for _ in range(N)]

        while q:
            cr, cc = q.popleft()
            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                nr, nc = cr + dr, cc + dc

                if not(in_range(nr, nc)):
                    continue
                if arr[nr][nc] != 0:
                    continue
                if tarr[nr][nc] != 0:
                    continue
                if parent[nr][nc] is not None:
                    continue

                parent[nr][nc] = (cr, cc)

                if (nr, nc) == (N - 1, N - 1):
                    found = True
                    break

                q.append((nr, nc))

            if found:
                break

        # 2. 경로
        sr, sc = r, c
        if parent[N - 1][N - 1] is not None:
            tr, tc = N - 1, N - 1
            while parent[tr][tc] != (sr, sc):
                tr, tc = parent[tr][tc]

            tarr[sr][sc] = 0
            # case1. 다음 경로가 N - 1, N - 1
            if (tr, tc) == (N-1, N-1):
                del tdct[id]
                count += 1
                answer[id] = turn
            # case2.
            else:
                tarr[tr][tc] = id
                tdct[id] = (tr, tc)

def step2():
    global vdct
    for id in sorted(vdct.keys()):
        vdct[id][2] += 10

def step3(turn):
    global varr, vpos, vdct, tarr, tdct, count, answer
    # 1. 열기 전파
    q = deque()
    erupted = set()
    for id in sorted(vdct.keys()):
        cr, cc, cpower, emax = vdct[id]
        if cpower >= emax:
            q.append(id)

    # 2. 전파 + 연쇄
    while q:
        id = q.popleft()
        if id in erupted:
            continue

        erupted.add(id)

        r, c, cpower, emax = vdct[id]
        varr[r][c] += emax

        # 열기 이동
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            power = emax
            cr, cc = r, c

            while True:
                nr, nc = cr + dr, cc + dc
                power //= 2

                if not(in_range(nr, nc)):
                    break
                if arr[nr][nc] == 1:
                    break
                if power == 0:
                    break

                varr[nr][nc] += power

                if vpos[nr][nc] > 0:
                    nid = vpos[nr][nc]
                    if nid not in erupted:
                        if vdct[nid][2] + varr[nr][nc] >= vdct[nid][3]:
                            q.append(nid)

                cr, cc = nr, nc
    # 3. 화석
    for id in sorted(tdct.keys()):
        r, c = tdct[id]
        if varr[r][c] >= 20:
            arr[r][c] = 2
            tarr[r][c] = 0
            del tdct[id]
            count += 1

    # 4.초기화
    varr = [[0]*N for _ in range(N)]
    for id in erupted:
        vdct[id][2] = 0




# 1. init
T = 1
for ts in range(1, T + 1):
    N, M, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    tarr = [[0]*N for _ in range(N)]
    tdct = {}
    for id in range(1, M + 1):
        r, c = map(int,input().split())
        tarr[r][c] = id
        tdct[id] = (r, c)

    varr = [[0]*N for _ in range(N)]
    vpos = [[0] * N for _ in range(N)]
    vdct = {}
    for id in range(1, K + 1):
        r, c, e_max = map(int, input().split())
        vdct[id] = [r, c, 0,e_max]
        vpos[r][c] = id

    answer = {id: -1 for id in range(1, M + 1)}
    count = 0

    # 2. execute
    for turn in range(1, 101):
        if count == M:
            break
        # step1.
        step1(turn)

        # step2.
        step2()

        # step3.
        step3(turn)

    for id in answer:
        print(answer[id])
