from collections import deque
def cw90(sr,sc):
    new_arr = [row[:] for row in arr]
    length = 3
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1.
            orr, occ = r - sr, c - sc
            # 2.
            rr, rc = occ, length - 1 - orr
            # 3.
            new_arr[sr + rr][sc + rc] = arr[r][c]
    return new_arr

def cw180(sr,sc):
    new_arr = [row[:] for row in arr]
    length = 3
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1.
            orr, occ = r - sr, c - sc
            # 2. # 0, 1 > 2, 1
            rr, rc = length - 1 - orr, length - 1 - occ
            # 3.
            new_arr[sr + rr][sc + rc] = arr[r][c]
    return new_arr
def cw270(sr,sc):
    new_arr = [row[:] for row in arr]
    length = 3
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            # 1.
            orr, occ = r - sr, c - sc
            # 2. # 0, 1 > 1, 0
            rr, rc = length - 1 - occ, orr
            # 3.
            new_arr[sr + rr][sc + rc] = arr[r][c]
    return new_arr
def step1(clear,tmp):
    v = [[False]*5 for _ in range(5)]
    if clear == 0:
        answer = 0
        for r in range(5):
            for c  in range(5):
                if v[r][c]: continue
                axis = tmp[r][c]
                cnt = 1
                v[r][c] = True
                q = deque([(r,c)])
                while q:
                    cr, cc = q.popleft()
                    for i in range(4):
                        nr, nc = cr + dr[i], cc + dc[i]
                        if not(0 <= nr < 5 and 0 <= nc < 5) or v[nr][nc]: continue
                        if tmp[nr][nc] == axis:
                            v[nr][nc] = True
                            q.append((nr,nc))
                            cnt += 1
                if cnt < 3: continue
                answer += cnt
        return answer
    elif clear == 1:
        for r in range(5):
            for c  in range(5):
                if v[r][c]: continue
                axis = tmp[r][c]
                cnt = 1
                v[r][c] = True
                q = deque([(r,c)])
                path = [(r,c)]
                while q:
                    cr, cc = q.popleft()
                    for i in range(4):
                        nr, nc = cr + dr[i], cc + dc[i]
                        if not(0 <= nr < 5 and 0 <= nc < 5) or v[nr][nc]: continue
                        if tmp[nr][nc] == axis:
                            v[nr][nc] = True
                            q.append((nr,nc))
                            cnt += 1
                            path.append((nr,nc))
                if cnt < 3: continue
                for rrr, ccc in path:
                    tmp[rrr][ccc] = 0
        return tmp

# 1.init
# T = int(input())
# for ts in range(1, T + 1):
k, m = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(5)]
orders = deque(map(int,input().split()))
# 상하좌우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# 2.execute
answer = []
for turn in range(1, k + 1):
    ans = 0
    # step1. 탐사 진행
    best_ans1 = 0
    candidates = []
    for r in range(0,3):
            for c in range(0,3):
                for id,tp in enumerate([cw90(r,c), cw180(r,c), cw270(r,c)], start = 1):
                     ans1 = step1(0,tp)
                     if best_ans1 < ans1:
                         best_ans1 = ans1
                         candidates = [(ans1, id, c, r)]
                     elif best_ans1 == ans1:
                         candidates.append((ans1, id, c, r))
    if best_ans1 == 0:
        ans = 0
        break
    else:
        step1_ans = sorted(candidates, key = lambda x: (-x[0],x[1], x[2], x[3]))[0]

        if step1_ans[1] == 1:
            arr = cw90(step1_ans[3], step1_ans[2])
        if step1_ans[1] == 2:
            arr = cw180(step1_ans[3], step1_ans[2])
        if step1_ans[1] == 3:
            arr = cw270(step1_ans[3], step1_ans[2])
        # step2. clearn the arr
        ## 1.
        while step1(0, arr):
            ans += step1(0, arr)
            arr = step1(1, arr)
            candidates2 = []

            ## 2.
            for r in range(5):
                for c  in range(5):
                    if arr[r][c] == 0:
                        candidates2.append((r,c))
            candidates2.sort(key=lambda x: (x[1], -x[0]))
            for nr, nc in candidates2:
                number = orders.popleft()
                arr[nr][nc] = number

        # step3.
        answer.append(ans)
print(*answer)







