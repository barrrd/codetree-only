N, B = map(int, input().split())
a = list(map(int, input().split()))

# Please write your code here.
def solution(N, B, a):
    target = 0

    # 1. binary search
    a.sort()
    min_t = a[0]
    max_t = 10**18
    # print(min_t, max_t)
    while min_t <= max_t:
        target = (max_t + min_t) // 2
        cur_d = 0
        possible = True
        for c in a:
            if c >= target:
                continue
            d = target - c

            cur_d += d**2

            if cur_d > B:
                possible = False
                max_t = target - 1
                break
        
        if cur_d <= B:
            answer = target
            min_t = target + 1


    return answer

# 
print(solution(N, B, a))