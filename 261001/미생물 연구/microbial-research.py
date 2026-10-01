from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N


def step1(turn, sr, sc, er, ec):
    global arr
    # 1. 미생물 투입
    cand = set()
    for r in range(sr, er):
        for c in range(sc, ec):
            if arr[r][c] != 0:
                cand.add((arr[r][c]))
            arr[r][c] = turn

    # 2. 두 개로 나누는지
    if cand:
        for id in cand:
            tmp = 0
            sr, sc = -1, -1
            for r in range(N):
                for c in range(N):
                    if arr[r][c] == id:
                        tmp += 1
                        sr, sc = r, c
            # 3. 이제 두개인지
            if tmp == 0:
                continue

            check = 1
            v = set()
            v.add((sr,sc))
            q = deque([(sr,sc)])
            while q:
                r, c = q.popleft()
                for dr, dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = r + dr, c + dc
                    if not in_range(nr, nc):
                        continue
                    if (nr,nc) in v:
                        continue
                    if arr[nr][nc] != id:
                        continue

                    v.add((nr, nc))
                    q.append((nr,nc))
                    check += 1

            # 4. 제거
            if tmp != check:
                for r in range(N):
                    for c in range(N):
                        if arr[r][c] == id:
                            arr[r][c] = 0

def step2():
    global arr
    # 1. 순서: 면적 > turn >
    orders = {}
    dct = {}
    for r in range(N):
        for c in range(N):
            flag = arr[r][c]
            if flag == 0:
                continue
            orders.setdefault(flag, [0, flag])
            dct.setdefault(flag, [])
            orders[flag][0] += 1
            dct[flag].append((r,c))
    order = sorted(orders, key = lambda x: (-orders[x][0], orders[x][1]))

    # 2. 이동
    new_arr = [[0]*N for _ in range(N)]
    for id in order:

        # 1. min r, c
        min_r, min_c = N, N
        for r, c in dct[id]:
            min_r, min_c = min(min_r, r), min(min_c, c)
        # 2. 상대좌표: (0,0)
        shape = []
        for r, c in dct[id]:
            shape.append((r - min_r, c - min_c))

        # 3. 시작 점
        sr, sc = -1, -1
        for dr in range(N):
            for dc in range(N):
                poss = True
                for r, c in shape:
                    nr, nc = r + dr, c + dc

                    if not in_range(nr,nc):
                        poss = False
                        break
                    if new_arr[nr][nc] != 0:
                        poss = False
                        break
                if poss:
                    sr, sc = dr, dc
                    break
            if poss:
                break

        # 4. 업데이트
        if poss:
            for dr, dc in shape:
                nr, nc = sr + dr, sc + dc
                new_arr[nr][nc] = id


    # 5.
    arr = new_arr

def step3():
    # 1. dct
    dct = {}
    for r in range(N):
        for c in range(N):
            flag = arr[r][c]
            if flag == 0:
                continue

            dct.setdefault(flag, 0)
            dct[flag] += 1

    # 2. 인접
    v = [[False]*N for _ in range(N)]
    pairs = set()
    for r in range(N):
        for c in range(N):
            ref = arr[r][c]

            if ref == 0:
                continue


            q = deque([(r, c)])
            while q:
                sr, sc = q.popleft()
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = sr + dr, sc + dc

                    if not in_range(nr,nc):
                        continue
                    if arr[nr][nc] == 0:
                        continue
                    if v[nr][nc]:
                        continue

                    if arr[nr][nc] == ref:
                        q.append((nr,nc))
                        v[nr][nc] = True
                    else:
                        nxt = arr[nr][nc]

                        txt = tuple(sorted([ref, nxt]))
                        pairs.add(txt)

    # 3. answer
    answer = 0
    for r1, r2 in pairs:
        answer += dct[r1] * dct[r2]
    print(answer)


# 1. init
T = 1
for ts in range(1, T + 1):
    N, Q = map(int, input().split())
    arr = [[0]*N for _ in range(N)]

    # 2. execution
    for turn in range(1, Q + 1):
        sr, sc, er, ec = map(int,input().split())
        # step1: 미생물 투입
        step1(turn, sr, sc, er, ec)

        # step2: 용기 이동
        step2()

        # step3. 실험 결과 이동
        step3()

