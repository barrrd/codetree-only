# n: 구멍 수 <= 10^9
# k: 최대 패치 수(종류) <= 10^9
# want to 최소  길이
n, k = map(int, input().split())
positions = list(map(int, input().split()))


min_l = 1
max_l = positions[-1] - positions[0] + 1
answer = max_l

# 1. binary search
while min_l <= max_l:
    mid_l = (min_l + max_l) // 2
    fin_point = 0
    cnt = 0
    for p in positions:
        if fin_point < p:
            fin_point = p + mid_l - 1
            cnt += 1
    # 2. update a min_l, max_l 
    if cnt <= k:
        max_l = mid_l - 1
        answer = mid_l
    else:
        min_l = mid_l + 1
print(answer)



