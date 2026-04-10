N = int(input())
colors = [list(map(int, input().split())) for _ in range(3 * N)]

# Please write your code here.
from collections import deque
def bfs(sr,sc,colors,v):
    
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0 ,0, -1, 1]

    repre = colors[sr][sc]
    q = deque([(sr,sc)])
    v[sr][sc] = True
    ans = [(sr,sc)]
    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not(2*N <= nr < 3*N and 0 <= nc < N) or colors[nr][nc] != repre:
                continue
            if v[nr][nc] :
                continue
            q.append((nr,nc))
            v[nr][nc] = True
            ans.append((nr,nc))
    
    return ans


def dfs(depth, colors, total):
    global answer

    # 1. depth == 3
    if depth == 3:
        answer = max(answer, total)
        return

    # 2. bfs
    v = [[False]*N for _ in range(3*N)]
    found = False
    for cr in range(2*N, 3*N):
        for cc in range(N):
            if v[cr][cc]:
                continue
            
            point = bfs(cr,cc,colors,v)

            if len(point) > 1:
                found = True
                # 3. update a temp total
                min_r = min(r for r,c in point)
                max_r = max(r for r,c in point)
                min_c = min(c for r,c in point)
                max_c = max(c for r,c in point)
                area = (max_r - min_r + 1) * (max_c - min_c + 1)

                tmp = area + len(point)

                # 4. remove the area
                new_colors = [row[:] for row in colors]
                for rr, rc in point:
                    new_colors[rr][rc] = 0
                
                # 5. gravity
                for c in range(N):
                    temp = []
                    for r in range(3*N):
                        if new_colors[r][c] != 0:
                            temp.append(new_colors[r][c])
                    
                    idx = 3*N - 1
                    for i in range(len(temp)- 1, -1, -1):
                        new_colors[idx][c] = temp[i]
                        idx -= 1

                    while idx >= 0:
                        new_colors[idx][c] = 0
                        idx -= 1
                
                # 6. dfs
                dfs(depth + 1, new_colors, total + tmp)
    if not found:
        answer = max(answer, total)

                     
# 1. init

answer = 0
dfs(0, colors, 0)
print(answer)

