N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]

# Please write your code here.
def solution(N, M, grid):
    answer = -float("inf")
    cand = set()

    def in_range(r,c):
        return 0 <= r < N and 0 <= c < M

    def dfs(num, v):
        nonlocal cand
        if num == 5:
            cand.add(frozenset(v))
            return
        
        for r, c in list(v):
            for dr, dc in [(1,0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc

                if not in_range(nr,nc):
                    continue
                if (nr,nc) in v:
                    continue

                v.add((nr,nc))
                dfs(num + 1, v)
                v.remove((nr, nc))
                

    # 1. 두개 공통
    for r in range(N):
        for c in range(M):
            v = {(r, c)}
            dfs(1, v)
    
    cand = list(cand)
    for i in range(len(cand)):
        for j in range(i, len(cand)):
            if len(cand[i] & cand[j]) != 2:
                continue
            
            score = 0
            for r, c in cand[i]:
                score += grid[r][c]
            for r,c in cand[j]:
                score += grid[r][c]
            
            answer = max(answer, score)



    return answer


# exe
print(solution(N, M, grid))