N, M = map(int, input().split())
sequences = [input() for _ in range(N)]

# Please write your code here.
# 1. make a bit mask
# a: 1, c: 2: g: 4, t:8, .: 15
base_to_bit = {'a': 1, 'c': 2, 'g': 4, 't': 8, '.': 15}
bit_mask = []
for seque in sequences:
    row = [base_to_bit[s] for s in seque]
    bit_mask.append(row)

# 2. dp

# valid[mask] = mask에 해당하는 sequence들을
# 초염기서열 1개로 동시에 커버할 수 있는가?
# valid = [False] * (1 << N)
valid = [False] * (2**N)
valid[0] = True


for mask in range(1, 2**N):

    possible = True
    
    # M칸 있는지 확인
    for col in range(M): # 
        curr = 15  # 1111, 처음엔 a/c/g/t 모두 가능
        # N개 파악
        for i in range(N):
            if mask & (2**i):
                curr &= bit_mask[i][col]
                if curr == 0:
                    possible = False
                    break
        if not possible:
            break

    valid[mask] = possible

INF = N + 1
dp = [INF] * (1 << N)
dp[0] = 0

for mask in range(1, 1 << N):
    # 이 집합 자체를 한 번에 커버 가능하면 1
    if valid[mask]:
        dp[mask] = 1
        continue

    # mask를 sub와 mask^sub로 분할
    sub = mask
    while sub:
        dp[mask] = min(dp[mask], dp[sub] + dp[mask ^ sub])
        sub = (sub - 1) & mask

print(dp[(1 << N) - 1])
print(dp)
