N, M = map(int, input().split())

grid = [list(map(int, input().split())) for _ in range(N)]

points = []
for _ in range(M):
    x, y = map(int, input().split())
    points.append((x - 1, y - 1))

# Please write your code here.
def solution(N, M, grid, points):
    answer = 0
    
    def in_range(r,c):
        return 0 <= r < N and 0 <= c < N

    def dfs(sr, sc, idx):
        nonlocal answer
        if idx == M - 1:
            answer += 1
            return
        
        for dr, dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = sr + dr, sc + dc
            if not in_range(nr,nc):
                continue
            if v[nr][nc]:
                continue
            if grid[nr][nc] == 1:
                continue
            
            v[nr][nc] = True
            if (nr, nc) == points[idx + 1]:
                dfs(nr, nc, idx + 1)
                v[nr][nc] = False
            else:
                dfs(nr,nc,idx)
                v[nr][nc] = False
            

    sr, sc = points[0]
    v = [[False]*N for _ in range(N)]
    v[sr][sc] = True
    dfs(sr,sc,0)


    return answer

##############
print(solution(N, M, grid, points))
