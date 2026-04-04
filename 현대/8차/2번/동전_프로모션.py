n, m = map(int, input().split())
t = []
c = []

for _ in range(n):
    type_t, value = input().split()
    t.append(type_t)
    c.append(int(value))

# Please write your code here.
# 1. make a dp
dp = [float("inf")]*(m + 1)
dp[0] = 0 

coins = list(zip(c,t))
coins.sort(key = lambda kv: kv[0])

# 2.execute
for value, type in coins:
    if type == "A":
        for i in range(value, m + 1):
            dp[i] = min(dp[i - value] + 1, dp[i] )
    elif type == "B":
        for i in range(m, value - 1, -1):
            dp[i] = min(dp[i - value] + 1, dp[i])

# 3. answer
if dp[m] == float("inf"):
    print(-1)
else:
    print(dp[m])
