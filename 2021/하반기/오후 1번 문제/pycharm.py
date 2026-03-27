def step1():
    eggs = []
    for r in range(n):
        for c in range(n):
            for d in range(8):
                if mpos[r][c][d] > 0:
                    eggs.append((r, c, d, mpos[r][c][d]))
    return eggs

def step2(turn):
    global arr, mpos
    new_arr = [[0]*n for _ in range(n)]
    new_mpos =  [list([0]*8 for _ in range(4))for _ in range(n)]
    # monster : 상 > ccw
    dr = [-1, -1, 0, 1, 1, 1, 0, -1]
    dc = [0, -1, -1, -1, 0, 1, 1, 1]
    for r in range(n):
        for c in range(n):
            for d in range(8):
                cnt = mpos[r][c][d]
                if cnt == 0:
                    continue
                moved = False
                for i in range(8):
                    ndir = (d + i) % 8
                    nr, nc = r + dr[ndir], c + dc[ndir]
                    if not(0 <= nr < n and 0 <= nc < n) or (nr,nc) == (pr,pc):
                        continue
                    if dead[nr][nc] <= turn:
                        moved = True
                        break
                if moved:
                    new_mpos[nr][nc][ndir] += cnt
                    new_arr[nr][nc] += cnt
                else:
                    new_mpos[r][c][d] += cnt
                    new_arr[r][c] += cnt
    arr = new_arr
    mpos = new_mpos


def product(lst, k):
    result = []
    path = []
    def backtracking():
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(len(lst)):
            path.append(lst[i])
            backtracking()
            path.pop()
    backtracking()
    return result



def step3(turn):
    global arr, pr, pc, dead, mpos
    # packman: 상 좌 하 우
    dr = [-1, 0, 1, 0]
    dc = [0, -1, 0, 1]
    # 1. make a product
    plst = product([0,1,2,3],3)

    # 2. choose a best path
    best_catch = -1
    path = []
    for lst in plst:
        cr, cc = pr, pc
        tmp_catch = 0
        v = set()
        v.add((pr,pc))
        moved = True
        for l in lst:
            nr, nc = cr + dr[l], cc + dc[l]
            if not(0 <= nr < n and 0 <= nc < n):
                moved = False
                break
            if (nr, nc) not in v :
                tmp_catch += arr[nr][nc]
                v.add((nr, nc))
            cr, cc = nr, nc
        if moved:
            if best_catch < tmp_catch:
                best_catch = tmp_catch
                path = lst
    # 3. update (arr and mpos) and make a dead
    for ls in path:
        pr, pc = pr + dr[ls], pc + dc[ls]
        if arr[pr][pc] > 0:
            mpos[pr][pc] = [0]*8
            arr[pr][pc] = 0
            dead[pr][pc] = turn + 3 # 죽은 표시


def step4(eggs):
    global arr, mpos
    # 1. packman 있으면 문제임,,,
    for r, c, d, cnt in eggs:
        mpos[r][c][d] += cnt
        arr[r][c] += cnt

# 1. init
T = 1
for ts in range(1, T + 1):
    # monster : 상 > ccw
    dr = [-1, -1, 0, 1, 1, 1, 0, -1]
    dc = [0, -1, -1, -1, 0, 1, 1, 1]
    # packman: 상 좌 하 우
    dr = [-1, 0, 1, 0]
    dc = [0, -1, 0, 1]
    m, t = map(int,input().split())
    n = 4
    pr, pc = map(int,input().split())
    pr, pc = pr - 1, pc -1 # 1.
    mpos = [list([0]*8 for _ in range(4))for _ in range(n)] # 2.
    arr = [[0]*n for _ in range(n)] #3. pack: -1, monser: 수 dead: - turn
    dead = [[0]*n for _ in range(n)]
    for mid in range(1, m + 1):
        r, c, d = map(int,input().split())
        r, c, d = r - 1, c - 1, d - 1
        mpos[r][c][d] += 1
        arr[r][c] += 1

    # 2. execute
    for turn in range(1, t + 1):
        # step1. make a eggs
        eggs = step1()
        # step1. monster move
        step2(turn)
        # step3. packman move
        step3(turn)
        # step4. hatch the eggs
        step4(eggs)
    # step5.
    answer = 0
    for r in range(n):
        for c in range(n):
            answer += sum(mpos[r][c])
    print(answer)
