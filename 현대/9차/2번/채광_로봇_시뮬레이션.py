from collections import deque
def step1(forward):
    global arr
    for r in range(n):
        for c in range(n):
            if r == 0 and c == 0:
                continue
            if r > 0: # from up
                forward[r][c] = max(forward[r][c], forward[r - 1][c] + grid[r][c])
            if c > 0: # from right
                forward[r][c] = max(forward[r][c], forward[r][c - 1] + grid[r][c])

def step2(backward):
    for r in range(n- 1, - 1, - 1):
        for c in range(n - 1, - 1, - 1):
            if r == n - 1 and c == n - 1:
                continue
            if r < n - 1: # go down
                backward[r][c] = max(backward[r][c], grid[r][c] + backward[r + 1][c])
            if c <  n - 1: # go right
                backward[r][c] = max(backward[r][c], grid[r][c] + backward[r][c + 1])


def step3():
    # 1. 시작: r, c
    prev = [[0]*n for _ in range(n)]
    for _  in range(t):
        curr = [[-float("inf")]*n for _ in range(n)]

        for r in range(n-1, -1, -1):
            for c in range(n-1, -1, -1):
                
                if r < n - 1 and prev[r+1][c] != float("inf"): # go down
                    curr[r][c] = max(curr[r][c], prev[r+1][c] + grid[r+1][c])
                if c < n - 1 and prev[r][c+1] != float("inf"): # go right
                    curr[r][c] = max(curr[r][c], prev[r][c+1] + grid[r][c+1])
        
        prev = curr

    return prev

n, t = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# Please write your code here.
# right or down [(0, 1), (1, 0)]
# 1. init
forward = [[-float("inf")]*n for _ in range(n)]
backward = [[-float("inf")]*n for _ in range(n)]

forward[0][0] = grid[0][0]
backward[n - 1][ n - 1] = grid[n - 1][n - 1]
tr, tc = n - 1, n - 1

# 2. execute
# step1. make a dp that forward
step1(forward)

# step2. maka dp that backward
step2(backward)

# stpe3. make dp that extra that is time machine
# (r,c)에서 출발해서 정확히 k초 동안 더 이동할 때 얻을 수 있는 최대 추가 이득
extra = step3()

# step4. answer
answer = [[-float("inf")]*n for _ in range(n)]
# 1. not 시간 여행
best = forward[n-1][n-1]

for r in range(n):
    for c in range(n):
        answer[r][c] = max(answer[r][c], forward[r][c] + extra[r][c] + backward[r][c])
        best = max(best, answer[r][c])

print(best)
