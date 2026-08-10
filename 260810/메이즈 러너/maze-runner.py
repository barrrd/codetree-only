from collections import deque
# def distance():

def step1():
    global arr, loc, left, ans
    new_loc = [[0]*n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if loc[r][c] > 0:
                curr_dist = abs(r - tr) + abs(c - tc)
                found = False
                for d in range(4):
                    nr, nc = r + dr[d], c + dc[d]
                    if not(0 <= nr < n and 0 <= nc < n ) or arr[nr][nc] > 0:
                        continue

                    nxt_dist = abs(nr - tr) + abs(nc - tc)
                    if curr_dist > nxt_dist:
                        found = True
                        if (nr, nc) == (tr, tc):
                            left -= loc[r][c]
                        else:
                            new_loc[nr][nc] += loc[r][c]

                        ans += loc[r][c]
                        break

                if not found:
                    new_loc[r][c] += loc[r][c]
    loc = new_loc

def square():
    for length in range(2, n + 1):
        for r in range(0, n - length + 1):
            for c in range(0, n - length + 1):
                p_f, e_f = False, False
                for sr in range(r, r + length):
                    for sc in range(c, c + length):
                        if arr[sr][sc] == -1:
                            e_f = True
                        if loc[sr][sc] > 0:
                            p_f = True
                if p_f and e_f:
                    return length, r, c


def step2():
    global arr, loc, left, ans, tr, tc
    # 1. square
    arr[tr][tc] = -1
    length, sr, sc = square()

    # 2. 내구도
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            if arr[r][c] > 0:
                arr[r][c] -= 1

    # 3. rotate
    new_loc = [row[:] for row in loc]
    new_arr = [row[:] for row in arr]
    new_tr, new_tc = -1, -1
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1.
            orr, occ = r - sr, c - sc
            # 2. 1, 3 > 3, 2
            rr, cc = occ, length - 1 - orr
            # 3.
            if (r,c) == (tr, tc):
                new_tr, new_tc = sr + rr, sc + cc
            new_arr[rr + sr ][cc + sc] = arr[r][c]
            new_loc[rr + sr ][cc + sc] = loc[r][c]

    loc = new_loc
    arr = new_arr
    tr, tc = new_tr , new_tc


# 1.init
T = 1
# 상 하 좌 우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
for ts in range(1, T + 1):
    n, m, k = map(int, input().split())
    arr = [list(map(int,input().split())) for _ in range(n)]
    loc = [[0]*n for _ in range(n)]
    ## 참가자
    for _ in range(m):
        rrr, ccc = map(int,input().split())
        loc[rrr - 1][ccc - 1] += 1
    ## 출구
    tr, tc = map(int,input().split())
    tr, tc  = tr - 1, tc - 1

    # 2. execute
    ans = 0
    left = m
    for turn in range(1, k + 1):
        if left == 0:
            break
        # step1. move
        step1()
        if left == 0:
            break

        step2()
        # if turn == 1:
        #     break

    print(ans)
    print(tr+ 1, tc+ 1)