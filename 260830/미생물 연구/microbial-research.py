from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def count_square(cand):
    # 1. 시작점 찾기
    sr, sc = -1, -1
    found = False
    for r in range(N):
        for c in range(N):
            if arr[r][c] == cand:
                found = True
                sr, sc = r, c
                break
        if found:
            break

    # 2. 4방향으로 이동
    count = 1
    v = [[False]*N for _ in range(N)]
    v[sr][sc] = True
    q = deque([(sr, sc)])

    while q:
        cr, cc = q.popleft()
        for dr, dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = cr + dr, cc+ dc

            if not in_range(nr, nc):
                continue
            if v[nr][nc]:
                continue
            if arr[nr][nc] != cand:
                continue

            q.append((nr, nc))
            v[nr][nc] = True
            count += 1

    return count

def remove(cand, count):
    global arr
    tmp = 0
    for r in range(N):
        for c in range(N):
            if arr[r][c] == cand:
                arr[r][c] = 0
                tmp += 1

            if tmp == count:
                break

        if tmp == count:
            break


def more_two(cand):
    global arr
    # 1. 후보자 투입
    for ca in cand:
        count = 0
        for r in range(N):
            for c in range(N):
                if arr[r][c] == ca:
                    count += 1

        # 2. 하나로 시작해서 < count 이면 remove
        if count_square(ca) < count:
            remove(ca, count)

def step1(sr, sc, er, ec, turn):
    global arr
    cand = set()
    for r in range(sr, er):
        for c in range(sc, ec):
            if arr[r][c] != 0:
                cand.add(arr[r][c])
            arr[r][c] = turn

    if cand:
        more_two(cand)

def step2():
    global arr

    new_arr = [[0]*N for _ in range(N)]
    # 1. dct로 정리
    dct = {}
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                continue

            id = arr[r][c]
            dct.setdefault(id, {
                "square": 0,
                "lst": []
            })

            dct[id]["square"] += 1
            dct[id]["lst"].append((r,c))

    # 2. 순서
    orders = []
    for id in dct.keys():
        orders.append((dct[id]["square"], id))

    orders.sort(key = lambda x: (-x[0], x[1]))

    # 3. update
    for order in orders:
        id = order[-1]
        tlst = dct[id]["lst"]

        # 4. max, min
        min_r = min(r for r, c in tlst)
        min_c = min(c for r, c in tlst)

        shape = []
        for r, c in tlst:
            shape.append((r - min_r, c - min_c))

        # 5. find the sr,sc
        sr, sc = -1, -1

        for r in range(N):
            for c in range(N):
                possible = True
                for dr,dc in shape:
                    nr, nc = r + dr, c + dc

                    if not in_range(nr, nc):
                        possible = False
                        break
                    if new_arr[nr][nc] != 0:
                        possible = False
                        break

                if possible:
                    sr, sc = r, c
                    break

            if possible:
                break

        if (sr, sc) != (-1, -1):
            for dr, dc in shape:
                r, c = sr + dr, sc + dc

                new_arr[r][c] = id

    # 6.
    arr = new_arr

def step3():
    # 1. maka a pairs
    pairs = set()
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                continue

            cur = arr[r][c]

            for dr,dc in [(1,0), (0,1)]:
                nr, nc = r + dr, c + dc

                if not in_range(nr, nc):
                    continue
                if arr[nr][nc] == 0:
                    continue

                nxt = arr[nr][nc]

                if cur != nxt:
                    a, b = sorted((cur, nxt))
                    pairs.add((a,b))
    # 2.answer
    answer = 0
    for a, b in pairs:
        tmp = 1
        tmp *= count_square(a) * count_square(b)
        answer += tmp

    print(answer)


# 1. init
T = 1
for ts in range(1, T + 1):

    N, Q = map(int,input().split())
    arr = [[0]*N for _ in range(N)]
    # 2. execution
    for turn in range(1, Q + 1):
        sr, sc, er, ec = map(int,input().split())

        # step1. 투입 that more_two > count_square, remove
        step1(sr,sc, er, ec, turn)

        # step2. 용기 이동
        step2()

        # step3. 실험 결과 기록
        step3()