n, q = map(int, input().split())
efficiency = list(map(int, input().split()))
m = [int(input()) for _ in range(q)]

# Please write your code here.
# 1. init
efficiency.sort()
index_dct = {e: i for i, e in enumerate(efficiency, 1) }


# 2. execute
for mid in m:
    if mid in index_dct.keys():
        # 1. lox * high cnt
        mid_index = index_dct[mid]

        low_cnt = mid_index - 1

        high_cnt = len(efficiency) - mid_index

        answer = low_cnt * high_cnt
        print(answer) 
    else:
        print(0)
