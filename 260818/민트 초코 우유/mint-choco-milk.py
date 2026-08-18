from collections import deque

def morning():
    global barr
    for r in range(N):
        for c in range(N):
            barr[r][c] += 1

def lunch():
    global farr, barr
    v = [[False]*N for _ in range(N)]
    leaders = []

    # 1. find the leader and group
    for r in range(N):
        for c in range(N):
            if v[r][c]:
                continue

            v[r][c] = True
            t_leader = farr[r][c]
            t_lst = [(r,c)]

            q = deque([(r,c)])
            while q:
                cr, cc = q.popleft()
                for dr, dc in [(0,1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = cr + dr, cc + dc

                    if not(0 <= nr < N and 0 <= nc < N):
                        continue
                    if v[nr][nc]:
                        continue
                    if farr[nr][nc] != t_leader:
                        continue

                    v[nr][nc] = True
                    q.append((nr,nc))
                    t_lst.append((nr,nc))

            # 2. leader, teams
            t_lst.sort(key = lambda x: (-barr[x[0]][x[1]],x[0], x[1]))
            leader = t_lst[0]
            leaders.append(leader)

            if len(t_lst) > 1:
                teams = t_lst[1:]
                lr, lc = leader

                for tr, tc in teams:
                    barr[tr][tc] -= 1
                    barr[lr][lc] += 1

    return leaders

def dinner(leaders):
    global barr, farr
    # 1. 순서 정함
    """
    민트, 초코, 우유: 4, 2, 1
    초코우유, 민트우유, 민트초코: 3, 5, 6
    민트초코우유 : 7
    """
    tmp_dct = {
        4: 1, 2: 1, 1: 1,
        3: 2, 5: 2, 6: 2,
        7: 3
    }
    orders = []

    for lr, lc in leaders:
        f = farr[lr][lc]
        orders.append((tmp_dct[f],barr[lr][lc], lr, lc))

    orders.sort(key = lambda x: (x[0], -x[1], x[2], x[3]))

    # 2. 전파
    # 위, 아래, 왼, 오
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    defense = set()
    for order in orders:
        _, b, r, c = order

        if (r,c) in defense:
            continue

        dir = b % 4

        x = b - 1
        barr[r][c] = 1
        cr, cc = r, c

        food = farr[cr][cc]

        while x > 0:
            nr, nc = cr + dr[dir], cc + dc[dir]

            # 1. 격자 밖: fin
            if not(0 <= nr < N and 0 <= nc <N):
                break

            # 2.1 같은 신앙
            if farr[nr][nc] == food:
                # 3.update
                cr, cc = nr, nc
                continue

            # 2.2 다른 신앙
            else:
                y = barr[nr][nc]

                # case1. 강한전파
                if x > y:
                    farr[nr][nc] = food
                    barr[nr][nc] += 1
                    x -= (y+1)
                    defense.add((nr,nc))

                # case2. 약한 전파
                else:
                    farr[nr][nc] |= food
                    barr[nr][nc] += x
                    x = 0
                    defense.add((nr,nc))
                # 3.update
                cr, cc = nr, nc

# 1.init
change_dct = {
   "T": 4,
   "C": 2,
    "M": 1
}

Test = 1
for ts in range(1, Test + 1):

    N, T = map(int,input().split())
    farr = [[0]*N for _ in range(N)]
    for r in range(N):
        for c, tmp in enumerate(input()):
            farr[r][c] = change_dct[tmp]
    barr = [list(map(int, input().split())) for _ in range(N)]

    # 2. execute
    for turn in range(1, T + 1):
        # step1. 아침: 신앙심 += 1
        morning()

        # step2. 점심:
        leaders = lunch()

        # step3. 저녁
        dinner(leaders)

        # print
        answer = [0]*7
        answer_dct = {
            7: 0,
            6: 1, 5: 2, 3: 3,
            4: 6, 2: 5, 1: 4
        }
        for r in range(N):
            for c in range(N):
                food = answer_dct[farr[r][c]]

                answer[food] += barr[r][c]
        print(*answer)
