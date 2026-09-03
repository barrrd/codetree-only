N, M, K = map(int, input().split())

edges = []
for _ in range(M):
    x, y = map(int, input().split())
    edges.append((x - 1, y - 1))
    # edges.append((x , y))

start_points = list(map(lambda x: int(x) - 1, input().split()))


# Please write your code here.
from collections import deque

def solution(N, M, K, edges, start_points):
    answer = float("inf")

    # 1. init
    graph = {}
    for s, e in edges:
        graph.setdefault(s, [])
        graph[s].append(e)
    
    # 2.exe
    dist = [[-1]*N for _ in range(K)]  
    poss = [[False]*N for _ in range(K)] 
    for idx, start in enumerate(start_points):

        q = deque([start])

        dist[idx][start] = 0
        poss[idx][start] = True    

        while q:
            cid =  q.popleft()
 
            # for nid in graph[cid]:
            for nid in graph.get(cid, []):
                if dist[idx][nid] != -1:
                    continue

                dist[idx][nid] = dist[idx][cid] + 1
                poss[idx][nid] = True    

                q.append(nid)
                
    
    # 3. answer
    for id in range(N):
        possible = True
        max_h = 0

        for start in range(K):
            if not poss[start][id]:
                possible = False
                break

            max_h = max(dist[start][id], max_h)
        
        if not possible:
            continue
        
        answer = min(answer, max_h)
        
    
    if answer == float("inf"):
        answer = -1

    return answer

print(solution(N, M, K, edges,start_points))