from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def step1(turn):
    global tarr, tdct, answer, count
    for id in sorted(tdct):
        sr, sc = tdct[id]

        found = False
        parent = [[None]*N for _ in range(N)]
        parent[sr][sc] = (sr,sc)

        q = deque([(sr, sc)])
        # 1. make a parent
        while q:
            cr, cc = q.popleft()
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = cr + dr, cc + dc

                if not in_range(nr,nc): # 범위 밖
                    continue
                if tarr[nr][nc] > 0: # 거북
                    continue
                if arr[nr][nc] > 0: # 산호 + 화석
                    continue
                if parent[nr][nc] is not None: # 우 하 좌 상
                    continue

                parent[nr][nc] = (cr, cc)

                if (nr, nc) == (N - 1, N - 1):
                    found = True
                    break
                else:
                    q.append((nr, nc))

            if found:
                break

        # 2. move a tutle: update a tarr, tdct, answer, count
        if found:
            # parent[pr][pc] == [sr, sc] 일떄 stop
            pr, pc = N - 1, N - 1
            while (sr, sc) != parent[pr][pc]:
                pr, pc = parent[pr][pc]

            tarr[sr][sc] = 0
            # case1. 안식처 도착
            if [N - 1, N - 1] == [pr, pc]:
                del tdct[id]
                answer[id] = turn
                count += 1
            # case2. Not 안식처
            else:
                tarr[pr][pc] = id
                tdct[id] = [pr, pc]

def step2():
    global vdct
    for id in vdct:
        vdct[id][2] += 10

def step3():
    global arr, tarr, tdct, varr, answer, count
    # 1. 열기 전파
    # find a initial erupted: 초기 분출
    q = deque([])
    for id in vdct:
        r, c, cur, p = vdct[id]
        if cur >= p: # 열기 분출
            q.append(id)

    # 열기 전파
    erupted = set()
    while q:
        id = q.popleft()
        # if id not in erupted:
        erupted.add(abs(id))

        r, c, cur, p = vdct[id]
        varr[r][c] += p

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            cr, cc, power = r, c, p
            while True:
                nr, nc = cr + dr, cc + dc
                power //= 2

                if not in_range(nr,nc):
                    break
                if arr[nr][nc] == 1:
                    break
                if power == 0:
                    break

                varr[nr][nc] += power
                cr, cc = nr, nc

                if arr[nr][nc] < 0:
                    if abs(arr[nr][nc]) not in erupted:
                        nid = abs(arr[nr][nc])
                        nxt_r, nxt_c, nxt_p , nxt_e = vdct[nid]
                        if varr[nr][nc] + nxt_p >= nxt_e:
                            q.append(abs(arr[nr][nc]))
    # 3. 화석화
    for id in sorted(tdct):
        r, c = tdct[id]
        if varr[r][c] >= 20:
            tarr[r][c] = 0
            del tdct[id]
            count += 1
            arr[r][c] = 2

    # 4.
    varr = [[0]*N for _ in range(N)]
    for id in sorted(vdct):
        if id in erupted:
            vdct[id][2] = 0

# 1. init
T = 1
for ts in range(1, T + 1):

    N, M, K = map(int, input().split())
    # 1: 산호, 음수: 화산 id, 2: 화석
    arr  = [list(map(int, input().split())) for _ in range(N)]

    tarr = [[0]*N for _ in range(N)]
    tdct = {}
    for id in range(1, M + 1):
        r, c = map(int,input().split())
        tdct[id] = [r, c]
        tarr[r][c] = id

    vdct = {}
    varr = [[0]*N for _ in range(N)]
    for id in range(1, K + 1):
        r, c, e_max = map(int,input().split())
        vdct[id] = [r, c, 0, e_max]
        arr[r][c] = -id

    answer = {id: - 1 for id in tdct}
    count = 0
    # 2. execute
    for turn in range(1, 101):
        # break 조건
        if count == M:
            break
        # step1. 거북이 이동
        step1(turn)

        # step2. 화산 압력 증가
        step2()

        # step3. 화산 분출 + 연쇄 반으 + 초기화
        step3()

    for id in answer:
        print(answer[id])