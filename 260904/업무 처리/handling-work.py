from collections import deque
H, K, R = map(int, input().split())

tasks = [deque(map(int, input().split())) for _ in range(1 << H)]

# Please write your code here.
def solution(H, K, R, tasks):
    answer = 0

    tree = [[deque(), deque()] for _ in range(2**(H + 1) - 1)]
    leaf_start = 2**(H ) - 1

    for day in range(1, R + 1):

        # 1.root
        if day % 2 == 1: # left
            if tree[0][0]:
                answer += tree[0][0].popleft()
        else: # right
            if tree[0][1]:
                answer += tree[0][1].popleft()
        
        # 2. mid
        for id in range(1, leaf_start):
            parent = (id - 1) // 2
            task = None
            
            # 홀수
            if day % 2 == 1:
                if tree[id][0]:
                    task = tree[id][0].popleft()
            # 짝수
            else:
                if tree[id][1]:
                    task = tree[id][1].popleft()
            
            if task:
                tree[parent][(id - 1) % 2].append(task)
            
        # 3.leaf
        for id in range(leaf_start, len(tree)):
            idx = id - leaf_start

            if not tasks[idx]:
                continue

            task = tasks[idx].popleft()

            parent = (id - 1) // 2

            if id % 2 == 1:       # left child
                tree[parent][0].append(task)
            else:                 # right child
                tree[parent][1].append(task)
    
    
    return answer


# answer
print(solution(H, K, R, tasks))