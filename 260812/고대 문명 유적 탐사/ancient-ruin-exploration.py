from collections import deque
def rotate(degree, sr, sc):
    global arr
    length = 3
    new_arr = [row[:] for row in arr]
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1. relative
            r1, c1 = r - sr, c - sc

            # 2. rotate
            # case1. 90도 (0,0) > (0,2)
            if degree == 90:
                r2, c2 = c1, length - 1 - r1
            elif degree == 180:
                r2, c2 = length - 1 - r1, length - 1 - c1
            elif degree == 270:
                r2, c2 = length - 1 - c1, r1

            # 3. real
            r3, c3 = r2 + sr, c2 + sc

            # 4. new_arr
            new_arr[r3][c3] = arr[r][c]

    return new_arr

def bfs(new_arr):
    count = 0
    lst = []
    v = [[False]*5 for _ in range(5)]
    for r in range(5):
        for c in range(5):
            if v[r][c]:
                continue

            value = new_arr[r][c]

            q = deque([(r,c)])
            v[r][c] = True

            g_count = 1
            g_lst = [(r,c)]
            while q:
                cr, cc = q.popleft()
                for dr, dc in [(-1,0), (1,0), (0,1), (0,-1)]:
                    nr, nc = cr + dr, cc + dc

                    if not(0 <= nr < 5 and 0 <= nc < 5):
                        continue
                    if v[nr][nc]:
                        continue
                    if new_arr[nr][nc] != value:
                        continue
                    q.append((nr,nc))
                    v[nr][nc] = True
                    g_count += 1
                    g_lst.append((nr,nc))

            if g_count >= 3:
                count += g_count
                lst.extend(g_lst)

    return count, lst


def step1():
    global arr
    # 1. find the start point
    cand = []
    best = 0
    for r in range(0,2 + 1):
        for c in range(0, 2 + 1):
            for degree in [90, 180, 270]:
                ## 1. make a new arr
                new_arr = rotate(degree, r, c)
                ## 2. bfs
                count, lst = bfs(new_arr)
                if count > best:
                    best = count
                    cand = [(count, degree, r, c, lst)]
                elif count == best:
                    cand.append((count, degree, r, c, lst))
    # 탐사 불가
    if best == 0:
        return True,[], 0

    #2. 탐사 가능
    cand.sort(key = lambda x: (-(x[0]), x[1], x[3], x[2]))
    select = cand[0]
    remove_lst = cand[0][-1]

    # 3. update a arr
    arr  = rotate(select[1], select[2], select[3])
    for rr, rc in remove_lst:
        arr[rr][rc] = 0

    remove_lst.sort(key = lambda  x: (x[1], -x[0]))
    return False, remove_lst, best

def step2(empty_lst, ans):
    global arr, orders
    # 1. put the 유뮬
    for idx in range(len(empty_lst)):
        order = orders.pop()

        pr, pc = empty_lst[idx]
        arr[pr][pc] = order

    # 2. 3개 이상이면 계속
    while True:
        count, remove_lst = bfs(arr)
        if count == 0:
            break

        ans += count

        for rr, rc in remove_lst:
            arr[rr][rc] = 0

        remove_lst.sort(key=lambda x: (x[1], -x[0]))

        for idx in range(len(remove_lst)):
            order = orders.pop()

            pr, pc = remove_lst[idx]
            arr[pr][pc] = order

    return ans

# 1. init
T = 1
for ts in range(1, T + 1):
    k, m = map(int, input().split())
    arr = [list(map(int,input().split())) for _ in range(5)]
    orders = list((map(int, input().split())))
    orders.reverse()

    # 2. execute
    answer = []
    for turn in range(k):
        # step0. 유뮬 획들 할 수 없는 경우
        # step1. 탐사
        is_fin, empty_lst, ans = step1()

        # 탐사 더 이상 불가
        if is_fin:
            break
        # 탐사 후
        else:
            # step2.
            answer.append(step2(empty_lst, ans))
    print(*answer)

