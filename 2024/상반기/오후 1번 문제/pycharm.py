from collections import deque
def can_down(r, c):
    if arr[r][c] != 0:
        return False
    for i in range(4):
        nr, nc = r + dr[i], c + dc[i]
        if not(0 <= nr < R + 3 and 0 <= nc < C) or arr[nr][nc] != 0:
            return False
    return True

def can_west(r, c):
    check_lst = [(r - 1,c - 1), (r,c - 2), (r + 1,c - 1), (r + 1,c - 2), (r + 2,c - 1)]
    for nr, nc in check_lst:
        if not(0 <= nr < R + 3 and 0 <= nc < C) or arr[nr][nc] != 0:
            return False
    return True

def can_east(r,c):
    check_lst = [(r - 1,c + 1), (r,c + 2), (r + 1,c + 1), (r + 1,c + 2), (r + 2,c + 1)]
    for nr, nc in check_lst:
        if not(0 <= nr < R + 3 and 0 <= nc < C) or arr[nr][nc] != 0:
            return False
    return True

def bfs(r, c):
    v = [[False]*C for _ in range(R + 3)]
    v[r][c] = True
    q = deque([(r,c)])
    max_r = 0
    while q:
        cr, cc = q.popleft()
        max_r = max(max_r, cr)
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not (0 <= nr < R + 3 and 0 <= nc < C) or arr[nr][nc] == 0 or v[nr][nc]: continue
            if abs(arr[cr][cc]) == abs(arr[nr][nc]):
                q.append((nr,nc))
                v[nr][nc] = True
            elif arr[cr][cc] < 0:
                q.append((nr,nc))
                v[nr][nc] = True
    return max_r - 2

# 1.init
# T = int(input())
T = 1
# 북 동 남 서
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
for ts in range(1, T + 1):
    R, C, K = map(int,input().split())
    orders = [list(map(int,input().split())) for _ in range(K)]
    for idx in range(len(orders)):
        orders[idx][0] -= 1
    # row: 0,1,2 에 하나라도 잇으면 문제
    arr = [[0]*C for _ in range(R + 3)]
    pos = {}
    answer = 0
    #########################################
    # step1. down or west or east
    #########################################
    for num, order in enumerate(orders, start = 1):
        sc, edir = order
        sr = 1
        while True:
            if can_down(sr + 1,sc):
                sr += 1
            elif can_west(sr, sc):
                sr += 1
                sc -= 1
                edir = (edir - 1) % 4
            elif can_east(sr, sc):
                sr += 1
                sc += 1
                edir = (edir + 1) % 4
            else:
                break
        if sr >= 4:
            arr[sr][sc] = num
            er, ec = sr + dr[edir], sc + dc[edir]
            for i in range(4):
                nr, nc = sr + dr[i], sc + dc[i]
                if (er, ec) == (nr,nc):
                    arr[nr][nc] = -num
                else:
                    arr[nr][nc] = num
            #########################################
            # step2. final row
            #########################################
            ans2 = bfs(sr, sc)
            answer += ans2
        else:
            arr = [[0]*C for _ in range(R + 3)]
        # for row in arr:
        #     print(row)
        # print()
    print(answer)
    # if ts == 1:
    #     break
