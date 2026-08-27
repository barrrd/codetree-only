from collections import deque
def is_range(r,c):
    return 0 <= r < N and 0 <= c < N

def can_down(sr, sc, h, w):
    is_possible = True
    for r in range(sr, sr + h):
        for c in range(sc, sc + w):
            if not is_range(r,c) or arr[r][c] != 0:
                is_possible = False
                break

        if not is_possible:
            break

    return is_possible

def step1(id, r, c, h, w):
    global arr, dct

    while can_down(r + 1, c, h, w):
        r += 1

    dct[id] = (r,c,h,w)
    for sr in range(r, r+ h):
        for sc in range(c, c+ w):
            arr[sr][sc] = id

def possible(r, h, check_lst):
    is_possible = True
    for sr in range(r, r + h):
        for sc in check_lst:
            if arr[sr][sc] !=0:
                is_possible = False
                break
        if not is_possible:
            break

    return is_possible

def update(id):
    global arr, dct
    r,c,h,w = dct[id]
    # 1. arr 제거
    for sr in range(r, r + h):
        for sc in range(c, c+ w):
            arr[sr][sc] = 0

    # 2. down
    print(id)
    del dct[id]

    # 3.
    orders = sorted(dct.keys(), key = lambda x: -(dct[x][0] + dct[x][2]))
    for order in orders:
        r, c, h, w = dct[order]

        ## 1. arr 제거
        for sr in range(r, r + h):
            for sc in range(c, c + w):
                arr[sr][sc] = 0

        ## 2. down
        while can_down(r + 1, c, h, w):
            r += 1

        ## 3. update
        for sr in range(r, r + h):
            for sc in range(c, c + w):
                arr[sr][sc] = order

        dct[order] = (r, c, h, w)


def left_right(flag):
    global arr, dct, count

    for id in sorted(dct):
        r, c, h, w = dct[id]
        if flag == "left":
            check_lst = range(0, c)
        else:
            check_lst = range(c + w, N)

        if possible(r,h,check_lst):
            update(id)
            return True

    return False




# 1. init
T = 1
for ts in range(1, T + 1):
    # ###############################
    # if ts == 2:
    #     break
    # ##############################
    N, M = map(int, input().split())

    arr = [[0]*N for _ in range(N)]


    # 2. execution
    # step1. 택배 투입
    dct = {}
    for _ in range(M):
        k, h, w, c = map(int, input().split())
        c -= 1
        step1(k,0,c,h,w)

    # step2~3
    count = 0
    while count < M:
        if left_right("left"):
            count += 1

        if left_right("right"):
            count += 1

        