n, m = map(int, input().split())

grid = [list(map(int, input().split())) for _ in range(n)]

points = []
for _ in range(m):
    x, y = map(int, input().split())
    points.append((x - 1, y - 1))

# Please write your code here.

# 상 하 좌 우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

ans = 0

def dfs(cr, cc, nxt):
    global ans
    # 1.arrive at target 
    if (cr, cc) == points[nxt]:
        if nxt == len(points) - 1:
            ans += 1
            return
        else:
            dfs(cr, cc , nxt + 1 )
    # 2. not arrive at target
    for i in range(4):
        nr, nc = cr + dr[i], cc + dc[i]
        if not(0 <= nr < n and  0 <= nc < n) or grid[nr][nc] == 1 or v[nr][nc]:
            continue
        v[nr][nc] = True
        dfs(nr, nc , nxt)
        v[nr][nc] = False




sr, sc = points[0]
v = [[False]*n for _ in range(n)]
v[sr][sc] = True
dfs(sr, sc, 1)
print(ans)




