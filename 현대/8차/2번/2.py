n, m = map(int, input().split())
t = []
c = []

for _ in range(n):
    type_t, value = input().split()
    t.append(type_t)
    c.append(int(value))

# Please write your code here.
coins = list(zip(c,t))
coins.sort()

INF = float("inf")
dp = [INF]*(m+1)
dp[0] = 0

for val, co in coins:
    if co == "A":
        for i in range(val, m + 1):
            dp[i] = min(dp[i], dp[i - val] + 1)
    elif co == "B":
        for i in range(m, val - 1, -1):

            dp[i] = min(dp[i], dp[i- val] + 1)


if dp[m] == INF:
    print(-1)
else:
    print(dp[m])
