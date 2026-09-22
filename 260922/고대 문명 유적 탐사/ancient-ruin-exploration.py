from collections import deque
def in_range(r,c):
    return 0 <= r < 5 and 0 <= c < 5

def rotate(angle, sr, sc):
    new_arr = [row[:] for row in arr]
    # 1.
    length = 3
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            ## 1.
            rr, cc = r - sr, c - sc
            ## 2.
            if angle == 90:
                orr, occ = cc, length -1 -  rr
            elif angle == 180:
                orr, occ = length -1 - rr, length -1 - cc
            elif angle == 270:
                orr, occ = length -1 - cc, rr
            # 3.
            new_arr[sr + orr][sc + occ] = arr[r][c]

    return new_arr

def bfs(narr):
    count = 0
    cand = []
    v = [[False]*5 for _ in range(5)]
    for r in range(5):
        for c in range(5):
            if v[r][c]:
                continue

            tmp = 1
            tval = narr[r][c]
            v[r][c] = True
            tcand = [(r,c)]
            q = deque([(tval,r,c)])
            while q:
                va, sr, sc = q.popleft()
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = sr + dr, sc + dc

                    if not in_range(nr, nc):
                        continue
                    if v[nr][nc]:
                        continue
                    if va != narr[nr][nc]:
                        continue

                    tmp += 1
                    v[nr][nc] = True
                    q.append((va, nr,nc))
                    tcand.append((nr,nc))

            if tmp >= 3:
                count += tmp
                cand.extend(tcand)

    return count, cand



def step1():
    global arr, answer
    # 1. 회전 중 가장 많이 후보자
    candidates = []
    best = 0
    for r in range(0,3):
        for c in range(0,3):
            for angle in [90, 180, 270]:
                # 1. new_arr
                narr = rotate(angle, r, c)
                # 2. bfs
                score, removes = bfs(narr)
                # 3.
                if score > best:
                    best = score
                    candidates = [(best, angle, r + 1, c + 1)]
                elif score == best:
                    candidates.append((score, angle, r + 1, c + 1))
    if best == 0:
        return False, []

    candidates.sort(key = lambda x: (-x[0], x[1], x[3], x[2]))
    score, angle, mr, mc = candidates[0]
    mr, mc = mr - 1, mc - 1

    # 2.
    new_arr = rotate(angle, mr, mc)
    score, removes = bfs(new_arr)
    answer.append(score)
    arr = [row[:] for row in new_arr]
    for rr, rc in removes:
        arr[rr][rc] = 0

    return True, removes

def step2(pos):
    global arr, orders, answer

    while True:
        # 1. put the 유물
        for pr, pc in pos:
            t = orders.pop()
            arr[pr][pc] = t

        # 2. 다시 검사
        score, pos = bfs(arr)
        if score > 0:
            answer.append(score)
            pos.sort(key = lambda x: (x[1], -x[0]))
        else:
            break

# 1. init
T = 1
for ts in range(1, T + 1):
    K, M = map(int, input().split()) # 1.
    arr = [list(map(int, input().split())) for _ in range(5)] # 2.
    orders = list(map(int, input().split())) # 3.
    orders.reverse()
    result = [] # 4.

    # 2. exe
    for turn in range(1, K + 1):
        answer = []  # 5.
        # step1. 탐사 가능 여부
        possible, pos = step1()

        # step2.
        if possible:
            pos.sort(key = lambda x: (x[1], -x[0]))
            step2(pos)
        else:
            break

        result.append(sum(answer))
    print(*result)


