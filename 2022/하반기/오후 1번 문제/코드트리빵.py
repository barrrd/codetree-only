from collections import deque
def move(i,blocked):
    global players
    sr, sc = players[i]
    tr, tc = arrive[i]
    
    # 1. target으로 부터 시작 점 까지 거리
    dist = [[-1]*n for _ in range(n)]
    dist[tr][tc] = 0
    q = deque([(tr,tc)])
    while q:
        cr, cc = q.popleft()
        d = dist[cr][cc]
        for id in range(4):
            nr, nc = cr + dr[id], cc+ dc[id]
            if not (0 <= nr < n and 0 <= nc < n): continue
            if blocked[nr][nc]: continue
            if dist[nr][nc] != -1: continue
            dist[nr][nc] = d + 1
            q.append((nr,nc))
    # 2. move one
    best_r, best_c = sr, sc
    best_d = float('inf')
    for id in range(4):
        nr, nc = sr + dr[id], sc + dc[id]
        if not(0 <= nr < n and 0 <= nc < n): continue
        if blocked[nr][nc]: continue
        if dist[nr][nc] == -1: continue
        if dist[nr][nc] < best_d:
            best_d = dist[nr][nc]
            best_r, best_c = nr, nc
    players[i] = [best_r, best_c]
    if players[i] == arrive[i]:
        return (arrive[i][0], arrive[i][1])
    return None

def bfs(sr,sc,blocked):
    dist = [[-1]*n for _ in range(n)]
    q = deque([(sr,sc)])
    dist[sr][sc] = 0

    candidates = []
    best = None
    while q:
        r, c = q.popleft()
        d = dist[r][c]
        if best is not None and d > best:
            break
        if arr[r][c] == 1 and not blocked[r][c]:
            if best is None:
                best = d
            candidates.append((r, c))
            continue

        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            if not (0 <= nr < n and 0 <= nc < n): continue
            if blocked[nr][nc]: continue
            if dist[nr][nc] != -1: continue
            q.append((nr,nc))
            dist[nr][nc] = d + 1
    candidates.sort()
    return candidates[0]


# 1. init
n, m = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(n)]
arrive = []
for _ in range(m):
    r, c = map(int,input().split())
    r -= 1
    c -= 1
    arrive.append([r,c])
players = [[-1,-1] for _ in range(m)]
dr = [-1, 0, 0 ,1]
dc = [0, -1, 1, 0]
done = [False] * m 
# print(arrive)
# print(players)

# 2. execute
turn = -1
blocked = [[False]*n for _ in range(n)]
while True:
    turn += 1
    ############################
    # step1. go to basecamp
    ############################
    temp = []
    for i in range(len(players)):
        if players[i] == [-1,-1]:
            break
        if done[i]:
            continue
        cell = move(i, blocked)
        if cell is not None:
            done[i] = True         
            temp.append(cell) 
    ############################
    # step2. go to basecamp
    ############################  
    for cell in temp:
        if cell is None:
            continue
        r2, c2 = cell
        blocked[r2][c2] = True

    ############################
    # step3. go to basecamp
    ############################
    if turn < m:
        er, ec = arrive[turn]
        br, bc = bfs(er,ec,blocked)
        blocked[br][bc] = True
        players[turn] = [br, bc]
        # print(br,bc)
    
    if all(done):
        print(turn + 1)   
        break
