from collections import deque
from collections import Counter
def cw(arr,sr,sc):
    tmp1 = [row[:] for row in arr]
    tmp2 = [row[:] for row in arr]
    tmp3 = [row[:] for row in arr]
    tmps = []
    # 1.
    for r in range(sr, sr + 3):
        for c in range(sc, sc +3):
            ## 1. relateive
            orr, occ = r - sr, c - sc
            ## 2. gap
            rr1, rc1 = occ, 3 - 1 - orr # (0,1) > (1,2)
            rr2, rc2 = 3 - 1 - orr, 3 - 1- occ# (1,2) > (1,0)
            rr3, rc3 = 3 - 1 - occ, orr# (1,2)> (0,1)
            ##3. assign
            tmp1[sr + rr1][sc + rc1] = arr[r][c]
            tmp2[sr + rr2][sc + rc2] = arr[r][c]
            tmp3[sr + rr3][sc + rc3] = arr[r][c]
    tmps.append(tmp1)
    tmps.append(tmp2)
    tmps.append(tmp3)

    return tmps

def bfs(tmp):
    q = deque()
    v = [[False]*5 for _ in range(5)]
    answer = 0
    for r in range(5):
        for c in range(5):
            if v[r][c]: continue
            ref = tmp[r][c]
            if ref == 0: continue
            ref_cnt = 1
            v[r][c] = True
            q.append((r,c))
            while q:
                cr,  cc = q.popleft()
                for i in range(4):
                    nr, nc = cr + dr[i], cc + dc[i]
                    if not( 0 <= nr < 5 and 0 <= nc < 5): continue
                    if v[nr][nc]: continue
                    if ref == tmp[nr][nc]:
                        v[nr][nc] = True
                        ref_cnt += 1
                        q.append((nr,nc))
            if ref_cnt >= 3:
                answer += ref_cnt
    return answer

def delete_bfs(arr):
    global ans
    q = deque()
    v = [[False]*5 for _ in range(5)]
    answer = 0
    for r in range(5):
        for c in range(5):
            if v[r][c]: continue
            ref = arr[r][c]
            if ref == 0: continue
            ref_cnt = 1
            v[r][c] = True
            paths = [(r,c)]
            q.append((r,c))
            while q:
                cr,  cc = q.popleft()
                for i in range(4):
                    nr, nc = cr + dr[i], cc + dc[i]
                    if not( 0 <= nr < 5 and 0 <= nc < 5): continue
                    if v[nr][nc]: continue
                    if ref == arr[nr][nc]:
                        v[nr][nc] = True
                        ref_cnt += 1
                        paths.append((nr,nc))
                        q.append((nr,nc))
            if ref_cnt >= 3:
                for pr,pc in paths:
                    arr[pr][pc] = 0
                    ans += 1
    
#######################################################3
# 1. init
k, m = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(5)] 
walls= deque(map(int, input().split()))
# 상하좌우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

final = []
# 2. execute
for turn in range(1, k+1):
    ## arr check : 없으면 break 그리고 ans = 0
    ans = 0
    ########################################
    # step1. 탐사
    ########################################
    best = 0
    best_paths = []
    for check_r in range(0,3):
        for check_c in range(0,3):
            tmps = cw(arr, check_r, check_c)
            for idx, tmp in enumerate(tmps):
                # print(tmp)
                temp = bfs(tmp)
                if best <= temp:
                    best = temp
                    best_paths.append((best, idx, check_c, check_r))
    if best == 0:
        ans = 0
        break
    else:
    ########################################
    # step2. 유물 
    ########################################
        # 1. ans
        pick = sorted(best_paths, key = lambda x: (-(x[0]), x[1], x[2], x[3]))[0]
        t_ans, cw_id,  start_c, start_r = pick
        tmps = cw(arr, start_r, start_c)
        arr = tmps[cw_id][:]
        # 2. delete
        delete_bfs(arr)
        # 3. put the walls num
        candidates = []
        for r in range(5):
            for c in range(5):
                if arr[r][c] == 0:
                    candidates.append((r,c))
        orders = sorted(candidates, key = lambda x: (x[1], -x[0]))
        for (ur, uc) in orders:
            nxt = walls.popleft()
            arr[ur][uc] = nxt
    ########################################
    # step3. 유물 연쇄 획득 
    ########################################
        flag = True
        while flag:
            prev = ans
            delete_bfs(arr)
            candidates = []
            for r in range(5):
                for c in range(5):
                    if arr[r][c] == 0:
                        candidates.append((r,c))
            orders = sorted(candidates, key = lambda x: (x[1], -x[0]))
            for (ur, uc) in orders:
                nxt = walls.popleft()
                arr[ur][uc] = nxt
            if prev == ans:
                flag = False
            elif prev < ans:
                prev = ans
        final.append(ans)
print(*final)

