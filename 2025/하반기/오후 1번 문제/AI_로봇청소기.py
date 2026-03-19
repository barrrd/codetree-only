from collections import deque
def step1():
    global arr, pos, carr
    for key in sorted(pos.keys()):
        value = pos[key]
        sr, sc = value
        if arr[sr][sc] > 0:
            continue
        v = [[False]*n for _ in range(n)]
        carr[sr][sc] = 0
        v[sr][sc] = True

        q = deque([(sr, sc , 0)])
        candidates = []
        best = float("inf")
        er, ec = sr, sc
        while q:
            cr, cc, cnt = q.popleft()
            if cnt > best:
                break
            for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                nr, nc = cr + dr, cc + dc
                if not(0 <= nr < n and 0 <= nc < n) or v[nr][nc] or arr[nr][nc] == -1: continue
                if carr[nr][nc] != 0: continue
                v[nr][nc] = True
                if arr[nr][nc] > 0: 
                    best = cnt + 1
                    candidates.append((best,nr,nc))
                elif arr[nr][nc] == 0:
                    q.append((nr, nc, cnt + 1))
        if candidates:
            candidates.sort() 
            er, ec = candidates[0][1:]
        else:
            er, ec = sr, sc 
            
        pos[key] = [er, ec]
        carr[er][ec] = key


def step2():
    global arr, carr, pos
    for key, value in pos.items():
        # 1. chooce a best dir
        sr, sc = value
        curr_dust = 0
        if arr[sr][sc] < 20:
            curr_dust = arr[sr][sc]
        elif arr[sr][sc] >= 20:
            curr_dust = 20
        best = - 1
        dir = - 1
        for i in range(4):
            nr0, nc0 = sr + dr[(i-1)% 4], sc + dc[(i-1)% 4]
            nr1, nc1 = sr + dr[i], sc + dc[i]
            nr2, nc2 = sr + dr[(i+1)% 4], sc + dc[(i+1)% 4]
            tmp = curr_dust
            for nr, nc in [(nr0,nc0), (nr1,nc1), (nr2,nc2)]:
                if not(0 <= nr < n and 0 <= nc < n) or arr[nr][nc] == -1: continue
                if arr[nr][nc] < 20:
                    tmp += arr[nr][nc]
                elif arr[nr][nc] >= 20:
                    tmp += 20
            if best < tmp:
                best = tmp
                dir = i
        # 2. clean the dust
        if dir != -1:
            if arr[sr][sc] <= 20:
                arr[sr][sc] = 0
            elif arr[sr][sc] >= 20:
                arr[sr][sc] -= 20
            nr0, nc0 = sr + dr[(dir-1)% 4], sc + dc[(dir-1)% 4]
            nr1, nc1 = sr + dr[dir], sc + dc[dir]
            nr2, nc2 = sr + dr[(dir+1)% 4], sc + dc[(dir+1)% 4]
            for nr, nc in [(nr0, nc0), (nr1, nc1), (nr2, nc2)]:
                if not(0 <= nr < n and 0 <= nc < n) or arr[nr][nc] == -1: continue
                if arr[nr][nc] < 20:
                    arr[nr][nc] = 0
                elif arr[nr][nc] >= 20:
                    arr[nr][nc] -= 20
def step3():
    global arr
    for r in range(n):
        for c in range(n):
            if arr[r][c] > 0:
                arr[r][c] += 5

def step4():
    global arr
    # 1. copy
    new_arr = [row[:] for row in arr]

    # 2. execute
    for r in range(n):
        for c in range(n):
            if arr[r][c] == 0:
                diff = 0
                for i in range(4):
                    nr, nc = r + dr[i], c + dc[i]
                    if not(0 <= nr < n and 0 <= nc < n) or arr[nr][nc] in (-1, 0): continue
                    diff += arr[nr][nc]
                new_arr[r][c] = diff // 10

    arr = new_arr


# 1. init
n, k, l = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(n)]
carr = [[0] * n for _ in range(n)]
pos = {}
for i in range(1,k+1):
    ri, ci = map(int,input().split())
    ri -= 1
    ci -= 1
    pos[i] = [ri,ci]
    carr[ri][ci] = i    

# 오 아 왼 위
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

# 2. execute
for T in range(1, l + 1):
    ##################################
    # step1. 청소기 이동
    ##################################
    step1()
    ##################################
    # step2. 청소
    ##################################
    step2()
    #################################
    # step3. 먼지 축척
    ##################################
    step3()
    ##################################
    # step4. 먼지 확산
    ##################################
    step4()

    ans = 0
    for r in range(n):
        for c in range(n):
            if arr[r][c] != -1:
                ans += arr[r][c]
    print(ans)

