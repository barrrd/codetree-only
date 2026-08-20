from collections import deque

def step1(turn):
    global tutle, tarr, answer, count
    for id in sorted(tutle.keys()):
        sr, sc = tutle[id]

        # 1. BFS
        parent = [[None] * N for _ in range(N)]
        q = deque([(sr, sc)])
        found = False

        while q:
            cr, cc = q.popleft()
            # 우하좌상
            for dr,dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = cr + dr, cc + dc

                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if arr[nr][nc] !=0 :
                    continue
                if tarr[nr][nc]:
                    continue
                if parent[nr][nc] is not None:
                    continue

                parent[nr][nc] = (cr, cc)

                if (N-1, N - 1) == (nr, nc):
                    found = True
                    break

                q.append((nr, nc))

            if found:
                break
        # 2. nxt
        nr, nc = sr, sc
        if parent[N - 1][N - 1] is not None:
            tr, tc = N - 1, N - 1

            while parent[tr][tc] != (sr,sc):
                tr, tc = parent[tr][tc]

            nr, nc = tr, tc

        tarr[sr][sc] = 0

        if (nr,nc) == (N - 1, N - 1):
            del tutle[id]
            answer[id] = turn
            count += 1
        else:
            tarr[nr][nc] = id
            tutle[id] = (nr,nc)

def step2():
    global var
    for id in var.keys():
        var[id][2] += 10

def step3():
    global arr, tarr, tutle, var, varr, answer, count
    # 1. 열기 전파
    ## 1. pressure > p 인 마그마 q
    q = deque()
    erupted = set()
    for id in sorted(var.keys()):
        sr, sc, pressure, max_p = var[id]
        if pressure >= max_p:
            q.append(id)

    ## 2.전파 + 연쇄
    while q:
        id = q.popleft()
        if id in erupted:
            continue

        erupted.add(id)

        sr, sc, pressure, max_p = var[id]
        varr[sr][sc] += max_p

        for dr,dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            cur_pre = max_p
            cr, cc = sr, sc
            while True:
                nr, nc = cr + dr, cc + dc
                cur_pre //=  2

                if not(0 <= nr < N and 0 <= nc < N):
                    break
                if arr[nr][nc] == 1 or cur_pre == 0:
                    break

                varr[nr][nc] += cur_pre

                if volcano_pos[nr][nc] > 0:
                    nxt = volcano_pos[nr][nc]
                    if nxt not in erupted:
                        if varr[nr][nc] + var[nxt][2] >= var[nxt][3]:
                            q.append(volcano_pos[nr][nc])

                cr, cc = nr, nc

    ## 3. 화석화
    for id in list(tutle.keys()):
        sr, sc = tutle[id]
        if varr[sr][sc] >= 20:
            arr[sr][sc] = 2

            tarr[sr][sc] = 0
            del tutle[id]

            count += 1
            answer[id] = -1

    ## 4. 초기화
    varr = [[0]*N for _ in range(N)]
    for id in erupted:
      var[id][2] = 0

# 1.init
T = 1
for ts in range(1, T + 1):
    N, M, K = map(int,input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    tutle = {}
    tarr = [[0]*N for _ in range(N)]
    for id in range(1, M + 1):
        r, c = map(int,input().split())
        tutle[id] = (r,c)
        tarr[r][c] = id

    var = {}
    varr = [[0]*N for _ in range(N)]
    volcano_pos = [[0]*N for _ in range(N)]
    for id in range(1, K + 1):
        r, c, max_p = map(int,input().split())
        var[id] = [r, c, 0, max_p]
        volcano_pos[r][c] = id

    answer = {id: -1 for id in range(1, M + 1)}
    count = 0
    # 2. execute
    for turn in range(1, 101):
        if count == M:
            break
        # step1. 이동
        step1(turn)

        # step2. 화산 압력 증가
        step2()

        # step3.
        step3()

    for id in answer.keys():
        print(answer[id])
