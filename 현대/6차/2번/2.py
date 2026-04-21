n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]
S, T = map(int, input().split())

# Please write your code here.
from collections import deque
def bfs(s,lst,target = - 1):
    v = set()
    v.add(s)
    q = deque([s])
    while q:
        cur = q.popleft()

        if cur == target:
            continue

        for nxt in lst[cur]:
            if nxt in v:
                continue
            v.add(nxt)
            q.append(nxt)
    
    return v

adj = [[] for id in range(n + 1)]
adj_rev = [[] for id in range(n + 1)]
for start, end in edges:
    adj[start].append(end)
    adj_rev[end].append(start)


s_to_x = bfs(S,adj,T)
x_to_t = bfs(T,adj_rev)

t_to_x = bfs(T,adj,S)
x_to_s = bfs(S,adj_rev)

inter = s_to_x & x_to_t & t_to_x & x_to_s
ans = len(inter)

if S in inter:
    ans -= 1
if T in inter:
    ans -= 1
print(ans)
