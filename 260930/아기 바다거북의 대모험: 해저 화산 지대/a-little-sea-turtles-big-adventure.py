from collections import deque

def in_range(r,c):
    return 0 <= r < N and  0 <= c < N

def step1(turn):
    global tarr, tdct, answer, count
    # 1. 이동가능한지 여부 및 후보자
    cands = []
    for id in sorted(tdct):
        r, c = tdct[id]
        parent = [[None]*N for _ in range(N)]
        parent[r][c] = (r,c)

        found = False
        q = deque([(r,c)])
        while q:
            sr, sc = q.popleft()
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = sr + dr, sc + dc

                if not in_range(nr,nc):
                    continue
                if parent[nr][nc] is not None:
                    continue
                if arr[nr][nc] > 0  or tarr[nr][nc] > 0:
                    continue

                parent[nr][nc] = (sr, sc)

                ## N- 1, N - 1도착
                if (nr,nc) == (N - 1, N - 1):
                    found = True
                    break
                else:
                    q.append((nr,nc))
            if found:
                break

        # 2. 이동
        if found:
            pr, pc = N - 1, N - 1
            while parent[pr][pc] != (r, c):
                pr, pc = parent[pr][pc]

            ## CASE1. EXIT에 도착
            if (pr, pc) == (N - 1, N - 1):
                del tdct[id]
                tarr[r][c] = 0
                answer[id] = turn
                count += 1
            ## Case2. not exit
            else:
                tarr[r][c] = 0
                tarr[pr][pc] = id
                tdct[id] = (pr, pc)

def step2():
    global vdct
    for id in sorted(vdct):
        r,c, p, e = vdct[id]
        vdct[id] = (r, c, p + 10, e)


def step3():
    global tarr, tdct, varr, vdct, answer, count
    # 0. 후보자
    q = deque()
    for id in sorted(vdct):
        if vdct[id][2] >= vdct[id][3]:
            q.append(id)

    # 1. 열기 전파
    erupted = set()
    while q:
        id = q.popleft()
        erupted.add(id)
        r, c, cur, p = vdct[id]
        varr[r][c] += p

        for dr, dc in [(1,0), (-1,0), (0, 1), (0, - 1)]:
            power = p
            sr, sc = r, c
            while True:
                nr, nc = sr + dr, sc + dc
                power //= 2

                if not in_range(nr,nc):
                    break
                if arr[nr][nc] == 1:
                    break
                if power == 0:
                    break

                varr[nr][nc] += power
                sr, sc = nr, nc

                # 2. 연쇄 반응
                if arr[nr][nc] <0:
                    if abs(arr[nr][nc]) not in erupted:
                        nid = abs(arr[nr][nc])
                        n_r, n_c, n_p, n_e = vdct[nid]
                        if n_p + varr[nr][nc] >= n_e:
                            q.append(nid)

    # 3. 화석화
    for tid in sorted(tdct):
        r, c = tdct[tid]

        if varr[r][c] >= 20:
            arr[r][c] = 2
            del tdct[tid]
            tarr[r][c] = 0
            count += 1

    # 4. 초기화
    varr = [[0]*N for _ in range(N)]
    for id in sorted(vdct):
        if id not in erupted:
            continue
        r, c, cur, e = vdct[id]
        vdct[id] = (r,c,0,e)

# 1.init
T = 1
for ts in range(1, T + 1):

    N, M, K = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    tarr= [[0]*N  for _ in range(N)]
    tdct = {}
    for id in range(1, M + 1):
        r, c = map(int, input().split())
        tdct[id] = (r, c)
        tarr[r][c] = id
    varr = [[0]*N for _ in range(N)]
    vdct = {}
    for id in range(1, K + 1):
        r, c, p = map(int, input().split())
        vdct[id] = (r,c,0,p)
        arr[r][c] = -id

    answer = {id: -1 for id in sorted(tdct)}
    count = 0

    # 2. exe
    for turn in range(1, 101):
        if count == M:
            break
        # step1. 바다거북 이동
        step1(turn)

        # step2. 화산 압력
        step2()

        # step3. 화산 분출 및 연쇄 반응
        step3()

    for id in answer:
        print(answer[id])


