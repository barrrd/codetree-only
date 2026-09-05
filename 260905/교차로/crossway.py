N = int(input())
t = []
w = []

for _ in range(N):
    time, pos = input().split()
    t.append(int(time))
    w.append(pos)

# Please write your code here.
from collections import deque

def solution(N, t, w):
    answer = [-1] * N 
    dct_change = {"A":0, "B": 1, "C": 2, "D": 3}
    orders = deque( (t[i], w[i], i) for i in range(N))

    cur_time = 0
    lst = [deque() for _ in range(4)]
    
    while orders or any(lst):
        # 1. 투입 
        while orders and orders[0][0] <= cur_time:
            arrive_time, lane, num = orders.popleft()
            lane = dct_change[lane]
            lst[lane].append(num)
        
        # 2. 
        to_go = []
        for i in range(4):
            if not lst[i]:
                continue

            nr = (i - 1) % 4

            if lst[nr]:
                continue
            to_go.append(i)
        
        if not to_go and any(lst):
            break
        
        # 3. 이제 제거
        for t_lane in to_go:
            id = lst[t_lane].popleft()
            answer[id] = cur_time
        
        # 4. 시간 진행
        if not any(lst) and orders:
            cur_time = orders[0][0]   
        else:
            cur_time += 1

    return answer

# 
for r in solution(N, t, w):
    print(r)