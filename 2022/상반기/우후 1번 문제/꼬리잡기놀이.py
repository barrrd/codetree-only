# up right down, left
dr = [-1, 0, 1, 0] 
dc = [0, 1, 0, -1]
def bfs(r, c, visited):
    visited.add((r,c))
    q = deque([(r,c)])
    result = [(r,c)]
    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not (0 <= nr < n and 0 <= nc < n): 
                continue
            if arr[nr][nc] == 0:
                continue
            if (nr,nc) in visited:
                continue
            visited.add((nr,nc))
            q.append((nr,nc))
            result.append((nr,nc))
    return result
            
# 1. init
from collections import deque
n, m, k = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(n)]

path_lists = []
visited = set()
for r in range(n):
    for c in range(n):
        if arr[r][c] == 0: continue
        if (r, c) in visited: continue

        path = bfs(r, c, visited)
        path_set = set(path)

        cur = path[0]
        temp = [cur]
        vis = {cur}

        while len(temp) < len(path):
            cr, cc = cur
            nxt = None
            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]
                if (nr, nc) in vis: continue
                if (nr, nc) in path_set:
                    nxt = (nr, nc)
                    break
            if nxt is None: break
            vis.add(nxt)
            temp.append(nxt)
            cur = nxt
        path_lists.append(temp)

team_members = []
team_indices = []
dirs = [] # 1: 정방향(+1 이동), -1: 역방향(-1 이동)

for path in path_lists:
    L = len(path)
    
    # 1. 머리(1
    head_idx = -1
    for i in range(L):
        r, c = path[i]
        if arr[r][c] == 1:
            head_idx = i
            break
            
    # 2. 경로의 방향 확인
    next_idx = (head_idx + 1) % L
    r_next, c_next = path[next_idx]
    
    if arr[r_next][c_next] == 2:
        path.reverse()
        head_idx = L - 1 - head_idx 
        
    dirs.append(1) 
    
    # 3. 팀원 추출: 머리 -> 몸통 -> 꼬리 순서로 담음
    curr = head_idx
    team_pos = []
    t_indices = []
    
    while True:
        r, c = path[curr]
        team_pos.append((r, c))
        t_indices.append(curr)
        if arr[r][c] == 3: 
            break
        curr = (curr - 1 + L) % L 
        
    team_members.append(team_pos)
    team_indices.append(t_indices)

team_sets = [set(mem) for mem in team_members]

# 2. execute
# print(arr[1][5])
total_score = 0
for round in range(k):
##############################
# step1. head move
##############################
    # 1. head move
    for t in range(m):
        # dirs[t]가 1이면 cw, -1이면 ccw
        move_dir = dirs[t]
        L = len(path_lists[t])
        
        new_team_pos = []
        for i in range(len(team_indices[t])):
            # 인덱스 업데이트
            team_indices[t][i] = (team_indices[t][i] + move_dir + L) % L
            new_team_pos.append(path_lists[t][team_indices[t][i]])
            
        team_members[t] = new_team_pos
        team_sets[t] = set(new_team_pos)

##############################
# step2. round
##############################
    turn = (round // n) % 4  # 0: 우, 1: 상, 2: 좌, 3: 하
    offset = round % n 
    trajectory = []
    if turn == 0:   # 왼 -> 오 (offset행)
        for c in range(n): trajectory.append((offset, c))
    elif turn == 1: # 아래 -> 위 (offset열)
        for r in range(n-1, -1, -1): trajectory.append((r, offset))
    elif turn == 2: # 오 -> 왼 (n-1-offset 행)
        for c in range(n-1, -1, -1): trajectory.append((n-1-offset, c))
    else:           # 위 -> 아래 (n-1-offset 열)
        for r in range(n): trajectory.append((r, n-1-offset))   
##############################
# step3. get a point
##############################
    hit_team_idx = -1
    for r, c in trajectory:
        for t_idx in range(m):
            if (r, c) in team_sets[t_idx]:
                hit_team_idx = t_idx
                # team_members는 무조건 [머리, 몸통, ..., 꼬리] 순서임
                hit_idx = team_members[t_idx].index((r, c))
                order = hit_idx + 1 # 머리가 인덱스 0이므로 +1 하면 순서
                total_score += (order ** 2)

                # 방향 반전
                team_members[t_idx].reverse()
                team_indices[t_idx].reverse()
                team_sets[t_idx] = set(team_members[t_idx]) 
                dirs[t_idx] *= -1 # 1은 -1로, -1은 1로 스위칭
                break
        if hit_team_idx != -1:
            break
print(total_score)
#     if round == 0:
#          break

