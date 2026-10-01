from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def step1():
    global barr
    for r in range(N):
        for c in range(N):
            barr[r][c] += 1

def step2():
    # 1. 순서
    orders = []
    v = [[False]*N for _ in range(N)]

    for r in range(N):
        for c in range(N):
            if v[r][c]:
                continue

            ref = farr[r][c]
            v[r][c] = True
            cands = [(barr[r][c], r, c)]

            q = deque([(r, c)])
            while q:
                sr, sc = q.popleft()
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = sr + dr, sc + dc

                    if not in_range(nr,nc):
                        continue

                    if v[nr][nc]:
                        continue

                    nxt = farr[nr][nc]
                    if nxt != ref:
                        continue

                    v[nr][nc] = True
                    cands.append((barr[nr][nc], nr, nc))
                    q.append((nr,nc))

            # 2. 신앙심 이동
            cands.sort(key = lambda x: (-x[0], x[1], x[2]))
            target = cands[0]
            b, tr, tc = target
            for i, (_, rr, rc) in enumerate(cands):
                if i == 0:
                    continue
                barr[rr][rc] -= 1
                barr[tr][tc] += 1

            orders.append((farr[tr][tc], barr[tr][tc], tr, tc))

    return orders

def step3(order):
    # 1. 순서
    orders = []
    for f, b, r, c in order:
        if f in [4, 2, 1]:
            orders.append((1, b, r, c))
        elif f in [3, 6, 5]:
            orders.append((2, b, r, c))
        else:
            orders.append((3, b, r, c))
    orders.sort(key = lambda x: (x[0], -x[1], x[2], x[3]))

    # 2. 전파
    defense = set()
    for _, B, r, c in orders:
        if (r,c) in defense:
            continue
        barr[r][c] = 1
        x = B - 1

        dir = B % 4
        dir_lst = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = dir_lst[dir]
        sr, sc = r, c
        ref = farr[r][c]

        while True and x > 0:
            nr, nc = sr + dr, sc + dc

            if not in_range(nr,nc):
                break

            y = barr[nr][nc]
            nxt = farr[nr][nc]

            if nxt == ref:
                sr, sc = nr, nc
                continue

            # Case1. 강한 전파
            if x > y:
                x -= (y + 1)
                farr[nr][nc] = ref
                barr[nr][nc] += 1
                defense.add((nr, nc))
                sr, sc = nr, nc
                continue
            # Case2. 약한 전파
            elif x <= y:
                farr[nr][nc] |= ref
                barr[nr][nc] += x
                x = 0
                defense.add((nr, nc))

# 1. init
Test =1
for ts in range(1, Test + 1):
    N, T = map(int, input().split())
    change_dct = {"T":4, "C": 2, "M": 1}

    farr = [[0]*N for _ in range(N)]
    for r in range(N):
        for c, char in enumerate(input()):
            cha = change_dct[char]
            farr[r][c] = cha

    barr = [list(map(int, input().split())) for _ in range(N)]
    # 2. execution
    for turn in range(1, T + 1):

        # 아침
        step1()

        # 점심
        orders = step2()

        # 저녁
        step3(orders)

        # answer
        answer = {7: 0, 6: 0, 5: 0, 3: 0, 1:0, 2:0, 4:0}
        for r in range(N):
            for c in range(N):
                f = farr[r][c]
                answer[f] += barr[r][c]
        ans = []
        for i in answer:
            ans.append(answer[i])
        print(*ans)

