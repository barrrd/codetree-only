N, M = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(M)]
S, T = map(int, input().split())

# Please write your code here.
from collections import deque

def solution(N, M, edges, S, T):
    answer = 0
    # for e in edges:
    #     print(e)

    # 1. init
    graph = [[] for _ in range(N + 1)]
    r_graph = [[] for _ in range(N + 1)]
    for start, end in edges:
        graph[start].append(end)
        r_graph[end].append(start)
    
    # 1. S > T
    forward = set([S])
    reverse = set([T])
    
    # 1-1. S -> X
    from_S = {S}
    q = deque([S])

    while q:
        cur = q.popleft()

        # T에 도착하면 출근 종료
        if cur == T:
            continue

        for nxt in graph[cur]:
            if nxt in from_S:
                continue

            from_S.add(nxt)
            q.append(nxt)

    # 1-2. X -> T
    to_T = {T}
    q = deque([T])

    while q:
        cur = q.popleft()

        # if cur == S:
        #     continue

        for nxt in r_graph[cur]:
            if nxt in to_T:
                continue

            to_T.add(nxt)
            q.append(nxt)

    # 출근길에 포함 가능한 노드
    st = from_S & to_T

    # 2-1. T -> X
    from_T = {T}
    q = deque([T])

    while q:
        cur = q.popleft()

        # S에 도착하면 퇴근 종료
        if cur == S:
            continue

        for nxt in graph[cur]:
            if nxt in from_T:
                continue

            from_T.add(nxt)
            q.append(nxt)

    # 2-2. X -> S
    to_S = {S}
    q = deque([S])

    while q:
        cur = q.popleft()

        # 역방향에서 T까지 왔으면 그 뒤로는 볼 필요 없음
        # if cur == T:
        #     continue

        for nxt in r_graph[cur]:
            if nxt in to_S:
                continue

            to_S.add(nxt)
            q.append(nxt)

    # 퇴근길에 포함 가능한 노드
    ts = from_T & to_S

    # 출근 + 퇴근 모두 포함 가능한 노드
    common = st & ts

    # S, T 제외
    answer = len(common) - 2

    
    return answer

# 
print(solution(N, M, edges, S, T))