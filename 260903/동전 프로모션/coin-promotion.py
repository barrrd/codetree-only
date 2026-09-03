N, M = map(int, input().split())
T = []
C = []

for _ in range(N):
    type_t, value = input().split()
    T.append(type_t)
    C.append(int(value))


# Please write your code here.
def solution(N, M, T, C):
    answer = 0
    INF = float("inf")

    # 1. dp상태 + 초기화
    """
    dp[x]: x일때의 최소 수
    dp의 초기화: INF
    """
    dp = [INF]* (M + 1)
    dp[0] = 0

    for typ, coin in zip(T, C):


        # 2. 이전 dp + 점화식
        """
        for id in s
        dp[5] = min(dp[5 - id] + 1, dp[5])
        """
        
        # 1. 오름차순: 중복 가능
        if typ == "A":
            for x in range(coin, M + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
        
        # 2 내림차순: 중복 불가
        if typ == "B":
            for x in range(M, coin - 1, -1):
                dp[x] = min(dp[x], dp[x - coin] + 1)
        
    answer = dp[M]

    if answer == INF:
        answer = -1

    return answer

print(solution(N, M, T, C))