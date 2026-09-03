from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def morning():
    global barr
    for r in range(N):
        for c in range(N):
            barr[r][c] += 1

def lunch():
    global barr
    # 1. make a group
    groups = []
    v = [[False]*N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if v[r][c]:
                continue
            f = farr[r][c]
            group = [(barr[r][c], r, c)]

            q = deque([(r,c)])
            v[r][c] = True
            while q:
                cr, cc = q.popleft()

                for dr,dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = cr + dr, cc + dc

                    if not in_range(nr, nc):
                        continue
                    if v[nr][nc]:
                        continue
                    if farr[nr][nc] != f:
                        continue

                    group.append((barr[nr][nc], nr,nc))
                    v[nr][nc] = True
                    q.append((nr,nc))

            # 2. choose a leader
            group.sort(key = lambda x: (-x[0], x[1], x[2]))

            # 3. update
            leader = group[0]
            lr, lc = leader[1:]
            member = []
            for gb, gr, gc in group[1:]:
                member.append((gr, gc))
                barr[gr][gc] -= 1
                barr[lr][lc] += 1

            tmp = [f,(barr[lr][lc], lr, lc)] + member
            groups.append(tmp)

    return groups

def dinner(groups):
    global farr, barr
    # 1. 순서
    order_dct = {
        4: 1, 2: 1, 1: 1,
        3: 2, 5: 2, 6: 2,
        7: 3
    }

    groups.sort(key = lambda x: (order_dct[x[0]], -x[1][0], x[1][1], x[1][2]))

    # 2. 시작
    pass_pos = set()
    for group in groups:
        f = group[0]

        b, lr, lc = group[1]

        if (lr,lc) in pass_pos:
            continue

        barr[lr][lc] = 1
        x = b - 1

        dir = b % 4
        drdc =  [(-1, 0), (1, 0), (0, -1), (0, 1)] # 상, 하, 좌, 우
        dr, dc = drdc[dir]

        nr, nc = lr + dr, lc + dc
        while in_range(nr,nc) and x > 0:
            nf = farr[nr][nc]
            # case1. 같은 경우
            if nf == f:
                nr, nc = nr + dr, nc + dc
                continue

            # case2. 다른 경우
            else:
                y = barr[nr][nc]
                pass_pos.add((nr,nc))
                ## case2.1 x > y : 강한 전파
                if x > y:
                    farr[nr][nc] = f

                    x  -= y + 1
                    barr[nr][nc] += 1
                ## cass2.2 x <= y : 약한 전파
                else:
                    farr[nr][nc] |= f

                    barr[nr][nc] += x
                    x = 0

                nr, nc = nr + dr, nc + dc

# 1. init
change_dct = {"T": 4, "C": 2, "M": 1}
Test = 1
for ts in range(1,Test + 1):

    N, T = map(int, input().split())

    farr = [[0] * N for _ in range(N)]
    for r in range(N):
        for c, tmp in enumerate(input()):
            t = change_dct[tmp]
            farr[r][c] = t
    barr = [list(map(int, input().split())) for _ in range(N)]


    # 2.exe
    for turn in range(1, T + 1):
        answer = {7: 0, 6: 0, 5: 0, 3: 0, 1: 0, 2: 0, 4: 0}
        # step1. 아침
        morning()

        # step2. 점심
        # print(f"{turn}!!")
        groups = lunch()
        # print()

        # step3. 저녁
        dinner(groups)

        # step4. answer
        for r in range(N):
            for c in range(N):
                f = farr[r][c]

                answer[f] += barr[r][c]

        fin = []
        for id in answer:
            fin.append(answer[id])
        print(*fin)

