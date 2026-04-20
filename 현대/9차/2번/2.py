n, t = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# Please write your code here.

from collections import deque
def step1(forward):
    forward[0][0] = grid[0][0]

    check_lst = [(-1,0), (0, -1)]
    for r in range(n):
        for c in range(n):
            if (r,c) == (0,0):
                continue
            for dr, dc in check_lst:
                pr, pc = r + dr, c + dc

                if not(0 <= pr < n and 0 <= pc < n):
                    continue

                forward[r][c] = max(forward[r][c], grid[r][c] + forward[pr][pc])

def step2(backward):
    backward[-1][-1] = grid[-1][-1]
            
    for r in range(n- 1, -1, -1):
        for c in range(n-1 ,-1, -1):
            if r == n -1 and c == n - 1:
                continue
            if r < n - 1:
                backward[r][c] = max(backward[r][c], backward[r + 1][c] + grid[r][c])
            if c < n - 1:
                backward[r][c] = max(backward[r][c], backward[r][c + 1] + grid[r][c])

def step3():
    prev = [row[:] for row in grid]
    for _ in range(t):
        curr = [[INF]*n for _ in range(n)]
        
        for r in range(n-1, -1, -1):
            for c in range(n-1, -1, -1):
                if r == n-1 and c == n-1:
                    continue
                if r < n - 1:
                    curr[r][c] = max(curr[r][c], grid[r][c] + prev[r+1][c])
                if c < n - 1:
                    curr[r][c] = max(curr[r][c], grid[r][c] + prev[r][c + 1])
        prev = curr
                
    return prev


INF = -float("inf")
forward  = [[INF]*n  for _ in range(n)]
backward = [[INF]*n  for _ in range(n)]

# step1: make a forward dp
step1(forward)

# step2. make a backrward dp
step2(backward)

# step3. make a extra dp that is period t
extra = step3()

# find the best 
answer = [[INF]*n for _ in range(n)]
best = forward[n-1][n-1]

for r in range(n):
    for c in range(n):
        answer[r][c] = max(answer[r][c], forward[r][c] + extra[r][c] + backward[r][c] - grid[r][c])
        best = max(answer[r][c], best)

print(best)

