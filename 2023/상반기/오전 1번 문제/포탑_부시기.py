from collections import deque
def bfs(att, tar):
    sr, sc = att[2], att[3]
    tr, tc = tar[2], tar[3]
    q = deque([(sr, sc, [])])
    v = {(sr,sc)}
    while q:
        r, c, path = q.popleft()
        for i in range(4):
            nr, nc = (r + dr[i]) % n, (c + dc[i]) % m
            if (nr, nc) == (tr, tc):
                return path
            if broken[nr][nc]: continue
            if (nr,nc) in v: continue
            temp = path[:]
            temp.append((nr,nc))
            v.add((nr,nc))
            q.append([nr, nc, temp])
    return None
            
# 1. init
n, m, k  = map(int,input().split())
arr = [ list(map(int,input().split())) for _ in range(n)]
broken = [[False] * m for _ in range(n)]
for r in range(n):
    for c in range(m):
        if arr[r][c] == 0:
            broken[r][c] = True
        arr[r][c] = [arr[r][c], -1]
        
#     우 하 좌 상
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]
# 
ddr = [0, -1, -1, -1, 0, 1, 1, 1]
ddc = [-1, -1, 0, 1, 1, 1, 0, -1]
# 2. execute
    #######################################
    # step
    #######################################
for turn in range(k):
    #######################################
    # step1.choose a attacker
    #######################################
    candidates = []
    for r in range(n):
        for c in range(m):
            if broken[r][c]: continue
            candidates.append([*arr[r][c], r, c])
    # print(candidates)
    if len(candidates) <= 1:
        break
    sorted_cand = sorted(candidates, key= lambda data: (data[0], -data[1], -(data[2] + data[3]), -data[3]))
    attacker = sorted_cand[0]
    sr, sc = attacker[2], attacker[3]
    power = attacker[0] + n + m
    arr[sr][sc][0] = power
    arr[sr][sc][1] = turn
    # print(power)
    # print(attacker)
    # print(arr)
    #######################################
    # step2~3. attack
    #######################################
    # 1. choose a target
    without_attacker = sorted_cand[1:]
    target = without_attacker[-1]
    tr, tc = target[2], target[3]
    # print(target)
    paths = bfs(attacker,target)
    # print(paths)

    arr[tr][tc][0] -= power
    # arr[tr][tc][1] = turn
    if arr[tr][tc][0] <= 0:
        broken[tr][tc] = True
    if paths is not None:
        for ar, ac in paths:
            arr[ar][ac][0] -= power//2
            # arr[ar][ac][1] = turn
            if arr[ar][ac][0] <= 0:
                broken[ar][ac] = True
    else:
        cannon_paths = []
        for i in range(8):
            nr, nc = (tr + ddr[i]) % n, (tc + ddc[i]) % m
            if (nr, nc) == (sr, sc): continue
            if broken[nr][nc]: continue
            arr[nr][nc][0] -= power//2
            cannon_paths.append((nr,nc))
            # arr[nr][nc][1] = turn
            if arr[nr][nc][0] <= 0:
                broken[nr][nc] = True
    # print(arr)
    # print(broken)
    #######################################
    # step4. update a arr
    #######################################
    for r in range(n):
        for c in range(m):
            if broken[r][c]: continue
            if (r,c) == (sr, sc): continue
            if (r,c) == (tr, tc): continue
            if paths is not None:
                if (r,c) in paths: continue
            else:
                if (r,c) in cannon_paths: continue
            arr[r][c][0] += 1
    # print(f"turn:{turn}, arr= {arr}")
    # print()
                          
 # 3. final
answer = 0
for r in range(n):
    for c in range(m):
        answer = max(answer,arr[r][c][0])
print(answer)
