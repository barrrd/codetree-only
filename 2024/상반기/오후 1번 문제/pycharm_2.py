from collections import deque
def can_down(cr, cc):
    possible = True
    lst = [(0,0), (-1,0), (0, 1), (1, 0), (0, -1)]
    for dr, dc in lst:
        nr, nc = cr + dr, cc + dc
        if not (0 <= nr < n + 3 and 0 <= nc < m) or arr[nr][nc] != 0:
            possible = False
            break
    return possible

def can_west(cr, cc):
    possible = True
    lst = [(-1,-1), (0,-2), (1, -1), (1, -2), (2, -1)]
    for dr, dc in lst:
        nr, nc = cr + dr, cc + dc
        if not (0 <= nr < n + 3 and 0 <= nc < m) or arr[nr][nc] != 0:
            possible = False
            break
    return possible

def can_east(cr, cc):
    possible = True
    lst = [(-1,1), (0,2), (1, 1), (2, 1), (1, 2)]
    for dr, dc in lst:
        nr, nc = cr + dr, cc + dc
        if not (0 <= nr < n + 3 and 0 <= nc < m) or arr[nr][nc] != 0:
            possible = False
            break
    return possible

def step1(id, sc, sd):
    global arr
    # 1. find the sr
    sr = 1
    while True:
        if can_down(sr + 1, sc):
            sr += 1
        elif can_west(sr , sc ):
            sr, sc = sr + 1, sc - 1
            sd = (sd - 1) % 4
        elif can_east(sr , sc ):
            sr, sc = sr + 1, sc + 1
            sd = (sd + 1) % 4
        else:
            break
    if 1 <= sr < 4:
        arr = [[0] * m for _ in range(n + 3)]
        return True, sr, sc
    else:
        arr[sr][sc] = id
        for i in range(4):
            nr, nc = sr + dr[i], sc + dc[i]
            if sd == i:
                arr[nr][nc] = - id
            else:
                arr[nr][nc] = id
        return False, sr, sc

def step2(id, sr, sc):
    global answer
    best_max = sr
    v = [[False]*m for _ in range(n + 3)]
    v[sr][sc] = True
    q = deque([(sr,sc, id)])
    while q:
        cr, cc, cid = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]

            if not(0 <= nr < n + 3 and 0 <= nc < m) or v[nr][nc]:
                continue
            if arr[nr][nc] == 0:
                continue

            # 1. 다른 id 이동 가능
            if arr[cr][cc] < 0 and abs(arr[nr][nc]) != cid:
                q.append((nr, nc, abs(arr[nr][nc])))
                v[nr][nc] = True
                best_max = max(nr, best_max)

            # 2. 같은 id 이동
            elif abs(arr[nr][nc]) == cid:
                q.append((nr, nc, abs(arr[nr][nc])))
                v[nr][nc] = True
                best_max = max(nr, best_max)

    # 3. update a answer
    answer += best_max - 2

# 1. init
T = int(input())
for ts in range(1, T + 1):
    n, m, k = map(int,input().split())
    arr = [[0]*m for _  in range(n + 3)]
    answer = 0

    # 북 동 남 서
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    # 2. execute
    for id in range(1, k + 1):
        sc, sd = map(int,input().split())
        sc -= 1
        # step1. put the block in arr and evalulate to is possible
        is_empty, center_r, center_c = step1(id, sc, sd)

        # step2. answer
        if not is_empty:
            step2(id, center_r, center_c)
    print(answer)
