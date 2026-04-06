from collections import deque
def distance(r1,c1, r2, c2):
    return abs(r1- r2) + abs(c1-c2)

def step1():
    global parr, er, ec, answer, left_number
    # 1. 동시에 move
    new_parr = [[0]*n for _ in range(n)]
    for sr in range(n):
        for sc in range(n):
            if parr[sr][sc] == 0:
                continue
            number = parr[sr][sc]
            curr_d = distance(sr, sc, er, ec)
            found = False
            for i in range(4):
                nr, nc = sr + dr[i], sc + dc[i]
                if not(0 <= nr < n  and 0 <= nc < n) or arr[nr][nc] > 0:
                    continue
                nxt_d = distance(nr, nc, er, ec)

                if nxt_d < curr_d:
                    found= True
                    answer += 1 * number
                    if nxt_d == 0: # 출구 도착
                        left_number -= number
                    else: # 츨구 도착 x
                        new_parr[nr][nc] += number
                    break

            if not found: # not move
                new_parr[sr][sc] += number

    parr = new_parr

def find_square():
    for length in range(2, n + 1):
        for r in range(0, n - length + 1):
            for c in range(0, n - length + 1):
                p_f, e_f = False, False
                for sr in range(r, r + length):
                    for sc in range(c, c + length):
                        if arr[sr][sc] == -1:
                            e_f = True
                        if parr[sr][sc] > 0:
                            p_f = True
                if p_f and e_f:
                    return length, r, c
    return None

def step2():
    global arr, parr,  er, ec
    # 1. find the square
    length, sr, sc = find_square()

    # 2. rotate the square
    ## 1. 내구도 감소
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            if arr[r][c] > 0:
                arr[r][c] -= 1

    ## 2. update ar parr, arr
    new_parr = [row[:] for row in parr]
    new_arr = [row[:] for row in arr]
    new_er, new_ec = -1, -1
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1.
            orr, occ = r - sr, c - sc
            # 2. 1, 3 > 3, 2
            rr, cc = occ, length - 1 - orr
            # 3.
            if (r,c) == (er, ec):
                new_er, new_ec = sr + rr, sc + cc
            new_arr[rr + sr ][cc + sc] = arr[r][c]
            new_parr[rr + sr ][cc + sc] = parr[r][c]

    parr = new_parr
    arr = new_arr
    er, ec = new_er, new_ec

# 1. init
T = 1
# 상 하 좌 우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
for ts in range(1, T + 1):
    n, m, k = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(n)]  #1.
    parr = [[0]*n for _ in range(n)] # 2
    for pid in range(1, m + 1):
        r, c = map(int,input().split())
        r, c = r - 1, c - 1
        parr[r][c] += 1

    for _ in range(1):
        er, ec = map(int,input().split())
        er, ec = er - 1, ec - 1 # 3
        arr[er][ec] = -1

    answer = 0
    left_number = m
    # 2. execute
    for turn in range(1, k + 1):
        step1()
        if left_number == 0:
            break
        step2()
    print(answer)
    print(er + 1, ec + 1)


