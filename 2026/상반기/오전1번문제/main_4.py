from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def step1(turn):
    global arr, tarr, tdct, count, answer
    # 1. 거북이 이동
    for tid in sorted(tdct):
        sr, sc = tdct[tid]

        found = False
        parent = [[None]*N for _ in range(N)]
        parent[sr][sc] = (sr,sc)

        q = deque([(sr, sc)])
        while q:
            r, c = q.popleft()
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc

                if not in_range(nr, nc):
                    continue
                if tarr[nr][nc] > 0:
                     continue
                if arr[nr][nc] > 0:
                     continue
                if parent[nr][nc]:
                    continue

                parent[nr][nc] = (r,c)

                if (nr,nc) == (N- 1, N - 1):
                    found = True
                    break
                else:
                    q.append((nr,nc))

            if found:
                break

        # 2. found시
        if found:
            pr, pc = N - 1, N - 1
            while (sr, sc) != parent[pr][pc]:
                pr, pc = parent[pr][pc]

            tarr[sr][sc] = 0
            # case1. pr, pc == N - 1, N - 1
            if (pr, pc) == (N - 1, N - 1):
                count += 1
                del tdct[tid]
                answer[tid] = turn
            # case2. not 도착
            else:
                tdct[tid] = [pr, pc]
                tarr[pr][pc] = tid

def step2():
    global vdct
    for id in sorted(vdct):
        vdct[id][2] += 10

def step3():
    global varr, vdct, arr, tarr, tdct, count, answer

    # 0. 후보자
    q = deque([])
    for id in vdct:
        r, c, cur, p = vdct[id]
        if cur >= p:  # 열기 분출
            q.append(id)

    # 1. 열기 전파
    erupted = set()
    while q:
        id = q.popleft()
        erupted.add(abs(id))

        r, c, cur, p = vdct[id]
        varr[r][c] += p

        for dr, dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:

            cr, cc, power = r, c, p
            while True:
                nr, nc = cr + dr, cc + dc
                power //=  2

                if not in_range(nr, nc):
                    break
                if arr[nr][nc] == 1:
                    break
                if power == 0:
                    break

                varr[nr][nc] += power
                cr, cc = nr, nc

                # 2. 연쇄 반응
                if arr[nr][nc] < 0: # 화산
                    if abs(arr[nr][nc]) not in erupted:
                        nid = abs(arr[nr][nc])
                        nxt_r, nxt_c, nxt_p , nxt_e = vdct[nid]
                        if varr[nr][nc] + nxt_p >= nxt_e:
                            q.append(abs(arr[nr][nc]))

    # 3. 화석화
    for tid in sorted(tdct):
        r, c = tdct[tid]

        if varr[r][c] >= 20:
            arr[r][c] = 2
            tarr[r][c] = 0
            del tdct[tid]
            count += 1

    # 4. 초기화
    varr = [[0]*N for _ in range(N)]
    for id in sorted(vdct):
        if id in erupted:
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
        tdct[id] = [r,c]
        tarr[r][c] = id

    varr = [[0]*N for _ in range(N)]
    vdct = {}
    for id in range(1, K + 1):
        r, c, e_max = map(int, input().split())
        vdct[id] = [r, c, 0, e_max]
        arr[r][c] = -id

    # 2.execution
    count = 0
    answer = {id: - 1 for id in tdct}
    for turn in range(1, 101):
        if count == M:
            break

        # step1
        step1(turn)

        # step2.
        step2()

        # step3.
        step3()

    for id in sorted(answer):
        print(answer[id])
