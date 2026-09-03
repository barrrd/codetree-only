N, T = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.
def solution(N, T, grid):
    answer = 0
    
    def in_range(r,c):
        return 0 <= r < N and 0 <= c < N

    # 1.fdp
    fdp = [[0]*N for _ in range(N)]

    fdp[0][0] = grid[0][0]
    for r in range(N):
        for c in range(N):
            if (r,c) == (0,0):
                continue
            tmp = -float("inf")
            for dr, dc in [(-1, 0), (0, -1)]:
                prev_r, prev_c = r + dr, c + dc

                if not in_range(prev_r,prev_c):
                    continue
                
                tmp = max(tmp, fdp[prev_r][prev_c])
            
            fdp[r][c] = grid[r][c] + tmp
    

    # 2. bdp
    bdp = [[0]*N for _ in range(N)]
    bdp[N-1][N-1] = grid[N-1][N-1] 

    for r in range(N - 1, -1, -1):
        for c in range(N - 1, -1, -1):
            if (r,c) == (N-1, N-1):
                continue
            tmp = -float("inf")

            for dr, dc in [(1,0), (0,1)]:
                nr, nc = r + dr, c + dc

                if not in_range(nr, nc):
                    continue
                
                tmp = max(tmp, bdp[nr][nc])
            
            bdp[r][c] = tmp + grid[r][c]


    # dp[r][c] = max(dp[r-1][c], dp[r][c-1]) + grid[r][c] 

    # 3.mdp
    mdp = [[0]*N for _ in range(N)]
    for t in range(1, T + 1):
        new_dp = [[-float("inf")]*N for _ in range(N)]

        for r in range(N):
            for c in range(N):
                for dr, dc in [(1, 0), (0, 1)]:
                    nr, nc = r + dr, c + dc

                    if not in_range(nr,nc):
                        continue
                    if mdp[nr][nc] == -float("inf"):
                        continue
                    
                    new_dp[r][c] = max(new_dp[r][c], mdp[nr][nc] + grid[nr][nc])
        
        mdp  = new_dp



    answer = fdp[N - 1][N - 1]
    
    for r in range(N):
        for c in range(N):
            if mdp[r][c] == -float("inf"):
                continue
            answer = max(answer, fdp[r][c] + bdp[r][c] + mdp[r][c])
    return answer 


# answer
print(solution(N, T, grid))

