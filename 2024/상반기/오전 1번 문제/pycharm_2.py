from collections import deque
def cw_90(sr,sc,length):
    array = [row[:] for row in arr]
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1. make a relative coordinate
            orr, occ = r - sr, c - sc
            # 2. cw 0,1 > 1, 2
            rr, cc = occ, length - 1 - orr
            # 3. absolute coord
            array[sr + rr][sc + cc] = arr[r][c]
    return array

def cw_180(sr,sc,length):
    array = [row[:] for row in arr]
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1. make a relative coordinate
            orr, occ = r - sr, c - sc
            # 2. cw 0,1 > 3, 2
            rr, cc = length - 1 - orr, length - 1 - occ
            # 3. absolute coord
            array[sr + rr][sc + cc] = arr[r][c]
    return array

def cw_270(sr,sc,length):
    array = [row[:] for row in arr]
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1. make a relative coordinate
            orr, occ = r - sr, c - sc
            # 2. cw 0,1 > 1, 0
            rr, cc = length - 1 - occ, orr
            # 3. absolute coord
            array[sr + rr][sc + cc] = arr[r][c]
    return array

def step1():
    global arr
    array = [row[:] for row in arr]
    candidates = []
    for sr in range(3):
        for sc in range(3):
            tmp_cw90 =  cw_90(sr,sc,3)
            tmp_cw180 = cw_180(sr,sc,3)
            tmp_cw270 = cw_270(sr,sc,3)

            candidates.append((0, sr, sc, tmp_cw90))
            candidates.append((1, sr, sc, tmp_cw180))
            candidates.append((2, sr, sc, tmp_cw270))

    return candidates

def bfs(array):
    # 1. find the same id
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    ans = 0
    v = [[False]*5 for _ in range(5)]
    for r in range(5):
        for c in range(5):
            if v[r][c] or array[r][c] == 0: continue
            q = deque([(r,c)])
            v[r][c] = True
            id = array[r][c]

            cnt = 1
            remove_lst = [(r,c)]
            while q:
                cr, cc = q.popleft()
                for i in range(4):
                    nr, nc = cr + dr[i], cc + dc[i]
                    if not(0 <= nr < 5 and 0 <= nc < 5) or v[nr][nc] or array[nr][nc] != id:
                        continue

                    q.append((nr,nc))
                    v[nr][nc] = True
                    cnt += 1
                    remove_lst.append((nr,nc))

            # 2. find the id that is same or more than 3
            if cnt >= 3:
                ans += cnt
                for rr, rc in remove_lst:
                    array[rr][rc] = 0
    return ans

def step2(candidates):
    global arr, tmp_answer
    # 1. find the best candidates
    best_max = 0
    new_candidates = []
    for cw, sr, sc, array in candidates:
        cnt = bfs(array)
        if cnt > best_max:
            best_max = cnt
            new_candidates = [(best_max,cw,sr,sc,array)]
        elif cnt == best_max:
            new_candidates.append((best_max,cw,sr,sc,array))

    if best_max == 0:
        return True
    else:
        new_candidates.sort(key = lambda x: (-x[0], x[1], x[3], x[2]))
        tmp_answer += new_candidates[0][0]
        arr = new_candidates[0][-1]
        return False

def step3(orders):
    global arr, tmp_answer
    # 1. find the zero candidates
    candidates = []
    for r in range(5):
        for c in range(5):
            if arr[r][c] == 0:
                candidates.append((r,c))
    candidates.sort(key = lambda x: (x[1], -x[0]))

    # 2. put the orders in zero pos
    for zr, zc in candidates:
        arr[zr][zc] = orders.pop()

    # 3. 연쇄
    while True:
        gained = bfs(arr)
        if gained >= 3:
            tmp_answer += gained
            # 1. find the zero candidates
            candidates = []
            for r in range(5):
                for c in range(5):
                    if arr[r][c] == 0:
                        candidates.append((r, c))
            candidates.sort(key=lambda x: (x[1], -x[0]))

            # 2. put the orders in zero pos
            for zr, zc in candidates:
                arr[zr][zc] = orders.pop()
        else:
            break

# 1.init
T = 1
for ts in range(1, T + 1):
    k, m = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(5)]
    orders = list(map(int,input().split()))
    orders.reverse()

    # 2. execute
    answer = []
    for turn in range(1, k + 1):
        tmp_answer = 0
        # step1. make a candidates
        candidates = step1()

        # step2. choose a candidate and scoring
        is_finish = step2(candidates)
        if is_finish:
            break

        # step3. put the orders
        step3(orders)
        answer.append(tmp_answer)

    print(*answer)




