H, K, R = map(int, input().split())

tasks = [list(map(int, input().split())) for _ in range(1 << H)]

# Please write your code here.
from collections import deque


tree = [[deque(), deque()] for _ in range(2**(H +1))] # 0: 제거, 1: 부서장 , 2: LEFT, 3: RIGHT

answer = 0
for turn in range(1, R + 1):
    # 1. 부서장
    if turn % 2 == 0: # 짝수: right
        if tree[1][1]:
            answer += tree[1][1].popleft()
    else: # 홀 수: left
        if tree[1][0]:
            answer += tree[1][0].popleft()
    
    # 2. 중간
    
    for child in range(2, 2**H):
        parent = child // 2
        job = None
        if turn % 2 == 0:
            if tree[child][1]:
                job = tree[child][1].popleft()
        else:
            if tree[child][0]:
                job = tree[child][0].popleft()

        if job:
            if child % 2 == 0:
                tree[parent][0].append(job)
            else:
                tree[parent][1].append(job)
    
    # 3. leaf
    for child in range(2**H, 2**(H + 1)):
        parent = child // 2

        idx = child - 2**H
        if tasks[idx]:
            job = tasks[idx].pop(0)

            if child % 2 == 0:
                tree[parent][0].append(job)
            else:
                tree[parent][1].append(job)

print(answer)
