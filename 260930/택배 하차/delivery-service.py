from collections import deque

def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def can_down(r, c, h, w):
    if not in_range(r + h - 1 , c + w - 1):
        return False

    poss = True
    for sr in range(r, r + h):
        for sc in range(c, c + w):
            if arr[sr][sc] != 0:
                poss = False
                break
        if not poss:
            break

    return  poss


def step1(k, h, w, c):
    global arr, dct
    # 1. choose a row
    r = 0
    while True:
        if can_down(r + 1, c, h, w):
            r += 1
        else:
            break
    # 2. update
    dct[k] = [r,c,h,w]
    for sr in range(r, r + h):
        for sc in range(c, c + w):
            arr[sr][sc] = k


def possible(r, h, check_c):
    poss = True
    for sr in range(r, r + h):
        for sc in check_c:
            if arr[sr][sc] != 0:
                return False

    return poss

def update(id):
    global arr, dct
    # 1. remove at arr
    r, c, h, w = dct[id]
    for sr in range(r, r + h):
        for sc in range(c, c + w):
            arr[sr][sc] = 0

    print(id)
    del dct[id]

    # 2. down
    orders = sorted(dct, key = lambda x: (-dct[x][0]))
    for id in orders:
        r, c, h, w = dct[id]
        ## 1. 제거
        for sr in range(r, r + h):
            for sc in range(c, c + w):
                arr[sr][sc] = 0
        ## 2. find the row
        while can_down(r + 1, c, h, w):
                r += 1
        ## 3. update
        dct[id] = [r,c,h,w]
        for sr in range(r, r + h):
            for sc in range(c, c + w):
                arr[sr][sc] = id


def left_right(flag):
    global arr, dct
    # 1. 범위
    for id in sorted(dct):
        r, c, h, w= dct[id]
        if flag == "left":
            check_range = range(0, c)
        elif flag =="right":
            check_range = range(c+w, N)

        # 2. 가능한지
        if possible(r, h, check_range):
            update(id)
            return True

    return False

# 1.init
T = 1
for ts in range(1, T + 1):
    N, M = map(int, input().split())
    arr = [[0]*N for _ in range(N)]

    # 2. execution
    dct = {}
    # step1. 택배 투입
    for _ in range(M):
        k, h, w, c = map(int,input().split())
        step1(k, h, w, c - 1)

    # step2. 택배 하차
    count = 0
    while count < M:
        if left_right("left"):
            count += 1
        if left_right("right"):
            count += 1