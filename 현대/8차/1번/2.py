n, m, k = map(int, input().split())

edges = []
for _ in range(m):
    x, y = map(int, input().split())
    edges.append((x - 1, y - 1))

start_points = list(map(lambda x: int(x) - 1, input().split()))

# Please write your code here.
from collections import deque

# 1. make a adj list 
adj = [[] for _ in range(n)]
for x, y in edges:
    adj[x].append(y)

# 2. make a 
ans = [0]*n 
vis = [0]*n 
for cid in start_points:
    dist = [-1]*n
    dist[cid] = 0
    q = deque([cid])
    while q:
        id = q.popleft()
        for nid in adj[id]:
            if dist[nid] == -1:
                dist[nid] = dist[id] + 1
                q.append(nid)

    # 3. update a ans and vis
    for idx, dis in enumerate(dist):
        if dis == -1:
            continue
        ans[idx] = max(ans[idx], dist[idx])
        vis[idx] += 1 

# 4.
answer = float("inf")
found = False
for idx, cnt in enumerate(ans):
    if vis[idx] != k:
        continue
    answer = min(answer, cnt)
    found = True

print(answer if found else -1)
