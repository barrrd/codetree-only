N = int(input())
t = []
w = []

for _ in range(N):
    time, pos = input().split()
    t.append(int(time))
    w.append(pos)

# Please write your code here.
from collections import deque

# 1. init
get_pos = {"A": 3, "B": 2, "C": 1, "D": 0}

lst = [deque() for _ in range(4)]  # 1.
answer = {i: -1 for i in range(N)} # 2.
time_in = {tmp: [] for _, tmp in enumerate(t)}  # 3. time: index
for i, tmp in enumerate(t):
    time_in[tmp].append(i)


# 2. execute
times = sorted(time_in.keys())
pointer = 0
time = min(time_in.keys())
pop_cnt = 0
while pop_cnt < N :
    # 0. update a poiner
    if not any(lst):
        if pointer >= len(times):
            break
        time = times[pointer]
    
    if pointer < len(times) and times[pointer] == time:
        pointer += 1

    # 1. put the car
    if time in time_in:
        in_tmp = time_in[time]
        for idx in in_tmp:
            type = get_pos[w[idx]]
            lst[type].append(idx)
    
    # 2. out
    is_possible = False
    who_out = [False]*4
    for i in range(4):
        nxt_idx = (i + 1) % 4
        if lst[i] :
            if not lst[nxt_idx]:
                who_out[i] = True
                is_possible = True

    for i in range(4):
        if who_out[i]:
            p = lst[i].popleft()
            answer[p] = time
            pop_cnt += 1

    if not is_possible:
        if any(lst):
            break

    # 3. update a time

    time += 1

# 3. answer
for v in answer.values():
    print(v)



