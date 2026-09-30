from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c< N

def step1():
    global rdct, rarr
    # 1. 후보자
    for id in sorted(rdct):
        r, c = rdct[id]
        if arr[r][c] > 0:
            continue
        cands = []
        best = float("inf")
        v = [[False]*N for _ in range(N)]
        v[r][c] = True
        q = deque([(r,c,0)])
        while q:
            sr, sc, sdist = q.popleft()
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = sr + dr, sc + dc

                if not in_range(nr,nc):
                    continue
                if v[nr][nc]:
                    continue
                if arr[nr][nc] == -1 or rarr[nr][nc] > 0:
                    continue

                v[nr][nc] = True

                # Case1. not 먼지
                if arr[nr][nc] == 0:
                    q.append((nr,nc, sdist + 1))
                # Case2. 먼지
                else:
                    if best > sdist + 1:
                        best = sdist + 1
                        cands = [(nr,nc, best)]
                    elif best == sdist + 1:
                        cands.append((nr, nc, best))
        
        if not cands:
            continue
        cands.sort(key = lambda x: (x[0], x[1]))
        target = cands[0]

        # 2. 이동 및 업데이트
        
        tr, tc, _ = target
        rarr[r][c] = 0
        rarr[tr][tc] = id
        rdct[id] = (tr, tc)

def step2():
    global arr
    # 1. 방향 찾기
    for id in sorted(rdct):
        r, c = rdct[id]
        cands = []
        best = 0
        for i in range(4):
            tmp = min(arr[r][c],20)
            for j, (dr, dc) in enumerate ([(0, -1), (-1, 0), (0, 1), (1, 0)]):
                if i == j:
                    continue

                nr, nc = r + dr, c + dc
                if not in_range(nr,nc):
                    continue
                if arr[nr][nc] == -1:
                    continue
                tmp += min(arr[nr][nc], 20)

            if best < tmp:
                cands = [(i, tmp)]
                best = tmp
            elif best == tmp:
                cands.append((i,tmp))

        cands.sort(key = lambda x: (x[0]))
        target = cands[0]

        # 2. clean
        e_num, _ = target
        if arr[r][c] <= 20:
            arr[r][c] = 0
        else:
            arr[r][c] -= 20
        for j, (dr, dc) in enumerate([(0, -1), (-1, 0), (0, 1), (1, 0)]):
            if e_num == j:
                continue
            nr, nc = r + dr, c + dc
            if not in_range(nr, nc):
                continue
            if arr[nr][nc] == - 1:
                continue

            if arr[nr][nc] <= 20:
                arr[nr][nc] = 0
            else:
                arr[nr][nc] -= 20

def step3():
    global arr
    for r in range(N):
        for c in range(N):
            if arr[r][c] > 0 :
                 arr[r][c] += 5


def step4():
    global arr
    new_arr = [row[:] for row in arr]
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                tmp = 0
                for dr, dc in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if not in_range(nr,nc):
                        continue
                    if arr[nr][nc] < 0:
                        continue
                    tmp += arr[nr][nc]

                tmp //= 10
                new_arr[r][c] += tmp

    arr = new_arr



# 1.init
T = 1
for ts in range(1, T + 1):
    N, K, L = map(int,input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]
    rdct = {}
    rarr = [[0]*N for _ in range(N)]
    for id in range(1, K + 1):
        r, c = map(int, input().split())
        r, c = r - 1, c - 1
        rdct[id] = (r, c)
        rarr[r][c] = id
    # 2. execution
    for turn in range(1, L + 1):
        # step1: 청소기 이동
        step1()

        # step2. 청소
        step2()

        # step3. 축적
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