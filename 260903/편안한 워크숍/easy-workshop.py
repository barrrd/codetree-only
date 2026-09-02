N, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.
# min max(h)
def solution(N, K, grid):
    answer = -1
    def in_range(r,c):
        return 0 <= r < N and 0 <= c < N

    # 1.dp
    cells = []

    for r in range(N):
        for c in range(N):
            cells.append((grid[r][c], r, c))


    cells.sort()

    # 2.binary search
    h_min = 0
    h_max = 10**8
    while h_min <= h_max:
        mid = (h_max + h_min)//2
        possible = False
        dp = [[1]*N for _ in range(N)]

        for h, r, c in cells:
            for dr, dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc

                if not in_range(nr, nc):
                    continue

                nh = grid[nr][nc]

                if  0 < nh - h  <= mid:
                    dp[nr][nc] = max(dp[nr][nc], dp[r][c] + 1)

                    if dp[nr][nc] >= K:
                        possible = True
                
                if possible:
                    break
            if possible:
                break


        if possible:
            answer = mid
            h_max = mid - 1
        else:
            h_min = mid + 1
        

    return answer

print(solution(N, K, grid))