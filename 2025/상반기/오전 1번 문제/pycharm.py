from collections import deque
from unittest.util import three_way_cmp


def step1():
    global barr
    for r in range(n):
        for c in range(n):
            barr[r][c] += 1

def step2():
    # 1. make a group
    group = {}
    repre = []

    v = [[False]*n for _ in range(n)]
    id = 1
    for r in range(n):
        for c in range(n):
            if v[r][c]: continue

            group[id] = {
                "rep": [],
                "shape": [],
                "type": arr[r][c]
            }
            path = [(r, c)]
            best = barr[r][c]
            candidates = [(r, c)]

            v[r][c] = True
            q = deque([(r,c)])
            while q:
                cr, cc = q.popleft()
                for i in range(4):
                    nr, nc = cr + dr[i], cc + dc[i]

                    if not (0 <= nr < n and 0 <= nc < n) or v[nr][nc]:
                        continue

                    if arr[r][c] != arr[nr][nc]:
                        continue

                    v[nr][nc] = True
                    q.append((nr,nc))
                    path.append((nr,nc))

                    # 2. representation
                    if best < barr[nr][nc]:
                        best = barr[nr][nc]
                        candidates = [(nr, nc)]
                    elif best == barr[nr][nc]:
                        candidates.append((nr, nc))


            candidates.sort(key = lambda x: (x[0], x[1]))
            group[id]["shape"] = path
            group[id]["rep"] = candidates[0]
            repre.append(group[id]["rep"])

            rr, rc = group[id]["rep"]
            for pr, pc in path:
                if (pr,pc) == group[id]["rep"]:
                    continue
                barr[pr][pc] -= 1
                barr[rr][rc] += 1
            id += 1

    return group, repre

def step3(group, repre):
    global arr, barr, answer
    # 1. make a order
    three = []
    two = []
    one = []
    for id in group.keys():
        type = group[id]["type"]
        rep_r, rep_c = group[id]["rep"]

        # 3개 중
        if type == 7: # 3
            three.append((barr[rep_r][rep_c], rep_r, rep_c, id))
        elif type in [1, 2, 4]:  # 2
            one.append((barr[rep_r][rep_c], rep_r, rep_c, id))
        else: # 2개
            two.append((barr[rep_r][rep_c], rep_r, rep_c, id))

    three.sort(key = lambda x: (-x[0], x[1], x[2]))
    two.sort(key=lambda x: (-x[0], x[1], x[2]))
    one.sort(key=lambda x: (-x[0], x[1], x[2]))
    tmp = one + two + three

    order = []
    for _, _, _, id in tmp:
        order.append(id)

    defense_rep = []
    # 2. make a faith and dir
    for id in order:
        type = group[id]["type"]
        shape = group[id]["shape"]
        rep_r, rep_c = group[id]["rep"]

        if (rep_r, rep_c) in defense_rep:
            continue

        dir = barr[rep_r][rep_c] % 4
        x = barr[rep_r][rep_c] -1
        barr[rep_r][rep_c] -= x
        sr, sc = rep_r, rep_c

        # 3. propagation
        while True:
            nr, nc = sr + dr[dir], sc + dc[dir]

            if not (0 <= nr < n and 0 <= nc < n):
                break
            ntype = arr[nr][nc]
            y = barr[nr][nc]

            if type == ntype:
                sr, sc = nr, nc
                continue

            # 강한 전파
            if x > y:
                arr[nr][nc] = type
                barr[nr][nc] += 1
                x -= (y + 1)

            # 약한 전파
            else:
                arr[nr][nc] = arr[nr][nc] | type
                barr[nr][nc] += x
                x = 0

            if (nr, nc) in repre:
                defense_rep.append((nr, nc))

            if x == 0:
                break

            sr, sc = nr, nc

# 1. init
Test = 1
for ts in range(1,Test + 1):
    # T(민트): 4, C(초코):2, M(우유):1
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    n, t = map(int, input().split())
    arr = [list(input()) for _ in range(n)] # 1.
    for r in range(n):
        for c in range(n):
            if arr[r][c] == "T":
                arr[r][c] = 4
            elif arr[r][c] == "C":
                arr[r][c] = 2
            else:
                arr[r][c] = 1
    barr = [list(map(int, input().split())) for _ in range(n)] # 2.

    # 2. execute
    for turn in range(1, t + 1):
        # step1: update a barr(신앙심) += 1
        step1()

        # step2. make a group and representation
        group, repre = step2()

        # step3. make a order and faith and propagation
        step3(group, repre)

        # step4. print answer
        answer = {7: 0, 6: 0, 5: 0, 3: 0 ,1: 0, 2: 0, 4: 0}
        for r in range(n):
            for c in range(n):
                answer[arr[r][c]] += barr[r][c]

        ans = [v for v in answer.values()]
        print(*ans)



