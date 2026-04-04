from collections import deque

n, m, k = map(int, input().split())

edges = []
for _ in range(m):
    x, y = map(int, input().split())
    edges.append((x - 1, y - 1))

start_points = list(map(lambda x: int(x) - 1, input().split()))

# Please write your code here.
# 1. init
adj = [[] for _ in range(n)]
for x, y in edges:
    adj[x].append(y)

# 2.
ans = [0]*n 
vis = [0]*n 
for cid in start_points:
    dist = [-1]*n
    q = deque([cid])
    dist[cid] = 0
    while q:
        id = q.popleft()
        for nxt in adj[id]:
            if dist[nxt] == -1 :
                dist[nxt] = dist[id] + 1
                q.append(nxt)
    # print(dist)
    # 3. update a ans and vis
    for idx, i in enumerate(dist):
        if i < 0:
            continue
        ans[idx] = max(ans[idx], dist[idx])
        vis[idx] += 1  

# 4. answer
answer = float("inf")
found = False
for idx, cnt in enumerate(ans):
    if vis[idx] != k:
        continue
    answer = min(answer, cnt)
    found = True

print(answer if found else -1)
