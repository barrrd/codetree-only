N, M = map(int, input().split())
sequences = [input() for _ in range(N)]

# Please write your code here.
# 1. make a bit mask
base_to_bit = {"a": 1, "c":2, "g": 4, "t": 8, ".": 15}
bit_mask = []
for seque in sequences:
    row = [base_to_bit[s] for s in seque]
    bit_mask.append(row)

# 2. make a valid that is 조합들 > 7: 1,2,3 이 들어 잇는거
"""
부분집합(mask)에 들어 있는 좋은 염기서열들을, 초염기서열 1개로 한 번에 커버할 수 있는가?"
"""
valid = [False] * (2**N)
valid[0] = True

for mask in range(1, 2**N):
    possible = True
    for col in range(M):
        curr = 15
        for i in range(N):
            if mask & (2**i):
                curr &= bit_mask[i][col]
                if curr == 0:
                    possible = False
                    break
        if not possible:
            break
    
    valid[mask] = possible

# 3. dp
"""
mask에 포함된 좋은 염기서열들을 전부 커버하기 위한
최소 초염기서열 개수
"""
INF = N + 1
dp = [INF]*(2**N)
dp[0] = 0

for mask in range(1, 2**N):
    ## 1. 부분 집합으로 cover 가능
    if valid[mask]:
        dp[mask] = 1
        continue
    
    ## 2. 부분집합을 커버 불가
    sub = mask
    while sub:
        dp[mask] = min(dp[mask], dp[sub] + dp[sub ^ mask])
        sub = (sub - 1) & mask

print(dp[(1 << N) - 1])
