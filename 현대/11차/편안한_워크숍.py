N, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.
def dfs(r,c,limit,dp):

    if dp[r][c] != -1:
        return dp[r][c]

    dp[r][c] = 1

    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0 ,0, -1, 1]
    for i in range(4):
        nr, nc = r + dr[i], c + dc[i]
        
        if not(0 <= nr < N and 0 <= nc < N):
            continue

        diff = grid[nr][nc] - grid[r][c]

        if diff <= 0 or diff > limit:
                continue
        
        dp[r][c] = max(dp[r][c], 1 + dfs(nr,nc,limit,dp))
    
    return dp[r][c]


def can(limit):
    dp = [[-1] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if  dfs(r,c,limit,dp) >= K:
                return True
    return False
               
# 1. make a dp that is dfs
lo = 1
hi = 10**8
ans = -1

while lo <= hi:
    mid = (lo +hi)//2

    if can(mid):
        hi = mid - 1
        ans = mid
    else:
        lo = mid + 1 
print(ans)
