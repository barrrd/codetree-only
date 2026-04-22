H, K, R = map(int, input().split())

tasks = [list(map(int, input().split())) for _ in range(1 << H)]

# Please write your code here.
from collections import deque
tree = [[deque(), deque()] for _ in range(2**(H+1))]

answer = 0
for day in range(1, R + 1):
    # 1. root
    if day % 2 == 1: # odd: left
        if tree[1][0]:
            answer += tree[1][0].popleft()
    elif day % 2 == 0: # even
        if tree[1][1]:
            answer += tree[1][1].popleft()

    # 2. mid: range(2, 2**H)
    for child in range(2, 2**H):
        parent = child // 2
        job = None
        if day % 2 == 1:
            if tree[child][0]:
                job = tree[child][0].popleft()
        else:
            if tree[child][1]:
                job = tree[child][1].popleft()
        
        if job:
            if child % 2 == 0:
                tree[parent][0].append(job)
            else:
                tree[parent][1].append(job)


    # 3. leaf
    for child in range(2**H, 2**(H+1)):
        parent = child // 2
        idx = child - 2**H
        if tasks[idx]:
            job = tasks[idx].pop(0)

            if child % 2 == 0: # left
                tree[parent][0].append(job)
            else: # right
                tree[parent][1].append(job)

print(answer)
