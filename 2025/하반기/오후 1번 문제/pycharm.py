from collections import deque
def step1():
    global marr, mpos
    for mid in range(1, k + 1):
        # 1. find ths sp
        mr, mc = mpos[mid]
        marr[mr][mc] = 0

        if arr[mr][mc] > 0:
            marr[mr][mc] = mid
            continue

        candidate = []

        v = [[False]*n for _ in range(n)]
        v[mr][mc] = True
        q = deque([(0, mr, mc)])

        best_sp = float("inf")
        found = False
        while q:
            sp, sr, sc = q.popleft()
            if found and best_sp <= sp:
                break
            for i in range(4):
                nr, nc = sr + dr[i], sc + dc[i]

                if not(0 <= nr < n and 0 <= nc < n) or v[nr][nc] or marr[nr][nc] > 0: continue
                if arr[nr][nc] == -1: continue

                q.append((sp + 1, nr, nc))
                v[nr][nc] = True

                if arr[nr][nc] > 0:
                    found = True
                    best_sp = sp + 1
                    candidate.append((sp + 1, nr, nc))

        if candidate:
            candidate.sort(key = lambda x: (x[0], x[1], x[2]))
            fr, fc = candidate[0][1:]
            marr[fr][fc] = mid
            mpos[mid] = [fr,fc]
        else: # 먼지가 없어서 이동 못한 경우
            marr[mr][mc] = mid

def step2():
    global arr
    for mid in range(1, k + 1):
        # 1. 4곳의 먼지 양
        mr, mc = mpos[mid]
        center = arr[mr][mc]
        dusts = [0 for _ in range(4)]
        for i in range(4):
            nr, nc = mr + dr[i], mc + dc[i]
            if not(0 <= nr < n and 0 <= nc < n) or arr[nr][nc] < 0: continue
            dusts[i] = min(arr[nr][nc], 20)

        # 2. choose a dir
        b_total = -1
        dir = -1
        for i in range(4):
            tmp = sum(dusts) - dusts[(i+2) % 4]
            if tmp > b_total:
                dir = i
                b_total = tmp
        b_total += center

        # 3. clean the dust
        arr[mr][mc] -= 20
        if arr[mr][mc] < 0:
            arr[mr][mc] = 0
        for i in range(4):
            nr, nc = mr + dr[i], mc + dc[i]
            if not (0 <= nr < n and 0 <= nc < n) or arr[nr][nc] < 0:
                continue
            if (dir + 2) % 4 == i:
                continue
            arr[nr][nc] -= 20
            if arr[nr][nc] < 0:
                arr[nr][nc] = 0

def step3():
    global arr
    for r in range(n):
        for c in range(n):
            if arr[r][c] > 0:
                arr[r][c] += 5

def step4():
    global arr
    new_arr = [row[:] for row in arr]
    for r in range(n):
        for c in range(n):
            if arr[r][c] == 0:
                # 1. total dust
                total = 0
                for i in range(4):
                    nr, nc = r + dr[i], c + dc[i]
                    if not(0 <= nr < n and 0 <= nc < n) or arr[nr][nc] < 0:
                        continue
                    total += arr[nr][nc]
                # 2. diffusion
                new_arr[r][c] += total // 10
    arr = new_arr


# 1. init
T = 1
for ts in range(1, T + 1):
    # 우 하 좌 상
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    n, k, l = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(n)] # 1.
    marr = [[0]*n for _ in range(n)]  # 2.
    mpos = {} # 3.
    for mid in range(1, k + 1):
        ri, ci = map(int,input().split())
        ri, ci = ri - 1, ci - 1
        marr[ri][ci] = mid
        mpos[mid] = [ri, ci]
    for turn in range(1, l + 1):
        # step1: move a 청소기
        step1()
        # step2. vacuum
        step2()
        # step3. accumulation dust
        step3()
        # step4. diffusion
        step4()
        # step5. total dust
        answer = 0
        for r in range(n):
            for c in range(n):
                if arr[r][c] > 0:
                    answer += arr[r][c]
        print(answer)


