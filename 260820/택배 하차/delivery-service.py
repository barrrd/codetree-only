from collections import deque

def down(cr, cc, h, w, num):
    is_possible = True
    if cr + h > N:
        is_possible = False
        return is_possible

    for r in range(cr, cr + h):
        for c in range(cc, cc+ w):
            if arr[r][c] != 0:
                is_possible = False
                break
        if not is_possible:
            break

    return is_possible


def step1(num, sc, w, h):
    global arr, dct

    # 1. sr 찾기
    sr = 0
    while True:
        if down(sr + 1, sc, h, w, num):
            sr += 1
        else:
            break

    # 2. update
    dct[num] = [sr, sc, h, w]
    for r in range(sr, sr + h):
        for c in range(sc, sc + w):
            arr[r][c] = num

def gravity():
    global arr, dct
    orders = sorted(dct.keys(),key = lambda x: -(dct[x][0] + dct[x][2]))

    for id in orders:
        sr, sc, h, w = dct[id]

        # 1. 잠시 지움
        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                arr[r][c] = 0

        # 2. down
        while down(sr + 1, sc, h, w, id):
            sr += 1

        # 3. update
        dct[id][0] = sr

        for r in range(sr, sr+ h):
            for c in range(sc, sc + w):
                arr[r][c] = id

def step2(flag):
    global arr
    # 1. find the cand
    for id in sorted(dct.keys()):
        is_possible = True
        sr, sc, h, w = dct[id]

        if flag == "left":
            check_lst = range(0, sc)
        elif flag == "right":
            check_lst = range(sc + w , N)

        for r in range(sr, sr + h):
            for c in check_lst:
                if arr[r][c] != 0:
                    is_possible = False
                    break
            if not is_possible:
                break

        # 2. 가능하면 제거
        if is_possible:
            for r in range(sr, sr + h):
                for c in range(sc, sc+ w):
                    arr[r][c] = 0


            # 3. update
            del dct[id]

            # 4. gravity
            gravity()

            return is_possible, id

    return is_possible, None

# 1. init
T = 1
for ts in range(1, T + 1):

    N, M = map(int, input().split())
    arr = [[0]*N for _ in range(N)]
    dct = {}

    # 2. execute
    for _ in range(M):
        num, h, w, start_c = map(int, input().split())
        start_c -= 1

        # step1. 택배 투입
        step1(num, start_c, w, h)

    # step2~3: left, right
    count = 0
    while count < M:
        pos2, ans2 = step2("left")
        if pos2:
            count += 1

            print(ans2)


        pos3, ans3 = step2("right")
        if pos3:
            count += 1
            print(ans3)

