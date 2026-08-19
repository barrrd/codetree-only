from collections import deque

def step1():
    global arr, varr, dct
    # 1. 이동
    for id in sorted(dct.keys()):
        sr, sc = dct[id]

        if arr[sr][sc] > 0:
            continue

        cand = []

        q = deque([(0, sr, sc)])
        v = [[False]*N for _ in range(N)]
        v[sr][sc] = True

        # 2. bfs
        while q:
            dist, cr, cc = q.popleft()
            dist += 1
            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]

                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if v[nr][nc]:
                    continue
                if varr[nr][nc] != 0 or arr[nr][nc] == -1:
                    continue

                v[nr][nc] = True
                # case1. 먼지 존재
                if arr[nr][nc] != 0:
                    cand.append((dist, nr, nc))
                # case2. 먼지 노존재
                elif arr[nr][nc] == 0:
                    q.append((dist, nr, nc))

        # 3. cand
        if cand:
            cand.sort(key = lambda x: (x[0], x[1], x[2]))
            tr, tc = cand[0][1:]
            varr[sr][sc] = 0
            varr[tr][tc] = id
            dct[id] = (tr, tc)
        else:
            tr, tc = sr, sc

def step2():
    global arr
    # 1. dir 찾기
    for id in dct.keys():
        sr, sc = dct[id]
        best = 0
        dir = 0

        for i in range(4):
            tmp = 0
            for idx in range(4):
                nr, nc = sr + dr[idx], sc + dc[idx]
                if i == idx :
                    continue
                if not(0 <= nr < N and 0 <= nc < N):
                    continue
                if arr[nr][nc] == -1:
                    continue

                tmp += min(20, arr[nr][nc])

            if tmp > best:
                best = tmp
                dir = i

        # 2. update
        arr[sr][sc] -= min(20, arr[sr][sc])
        for i in range(4):
            nr, nc = sr + dr[i], sc + dc[i]
            if i == dir:
                continue
            if not (0 <= nr < N and 0 <= nc < N):
                continue
            if arr[nr][nc] == -1:
                continue
            arr[nr][nc] -= min(20, arr[nr][nc])

def step3():
    global arr
    for r in range(N):
        for c in range(N):
            if arr[r][c] == -1 or arr[r][c] == 0:
                continue
            arr[r][c] += 5

def step4():
    global arr
    new_arr = [row[:] for row in arr]
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                power = 0
                for i in range(4):
                    nr, nc = r + dr[i], c + dc[i]

                    if not (0 <= nr < N and 0 <= nc < N):
                        continue
                    if arr[nr][nc] == -1:
                        continue
                    power += arr[nr][nc]

                power = power // 10
                new_arr[r][c] += power

    arr = new_arr


# 왼, 위, 오, 아
dr = [0, -1, 0, 1]
dc = [-1, 0, 1, 0]
# 1. init
T = int(input())
for ts in range(1, T + 1):
    N, K, L = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(N)]

    dct = {}
    varr = [[0]*N for _ in range(N)]
    for id in range(1, K + 1):
        r, c = map(int, input().split())
        dct[id] = (r - 1, c - 1)
        varr[r-1][c-1] = id

    # 2.execute
    for turn in range(1, L + 1):
        # step1. 청소기 이동
        step1()

        # step2. 청소
        step2()

        # step3. 먼지 축척
        step3()

        # step4. 먼지 확산
        step4()

        # 출력
        answer = 0
        for r in range(N):
            for c in range(N):
                if arr[r][c] > 0:
                    answer += arr[r][c]
        print(answer)



