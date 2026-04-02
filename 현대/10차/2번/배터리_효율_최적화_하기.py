from collections import deque
def combinations(arr, l):
    result = []

    def backtracking(start, path):
        if len(path) == l:
            result.append(path[:])
            return 
        for i in range(start, len(arr)):
            path.append(arr[i])
            backtracking(i + 1, path)
            path.pop()

    backtracking(0, [])

    return result

def step1():
    arr = []
    for r in range(n):
        for c in range(m):
            arr.append((r,c))
    
    return combinations(arr, 5)

def step2(res1, number):
    tmp_res2 = []
    for res in res1:
        sr, sc = res[0]
        nodes = set(res)
        q = deque([(sr,sc)])
        count = 1
        v = {(sr,sc)}
        while q:
            cr, cc = q.popleft()
            for i in range(4):
                nr, nc = cr + dr[i], cc + dc[i]

                if not(0 <= nr < n and 0 <= nc < m):
                    continue
                if (nr,nc) in nodes and (nr,nc) not in v:
                    q.append((nr,nc))
                    v.add((nr,nc))
                    count += 1
            
        if count == number:
            tmp_res2.append(res)
    
    if tmp_res2:
        return True, tmp_res2
    else:
        return False, []


def step3(res2):
    # 1. make a two
    best_max = -float('inf')
    
    for start in range(len(res2)):
        p1 = res2[start]
        
        score1 = sum(grid[r][c] for r, c in p1)
        set1 = set(p1)
        
        for i in range(start, len(res2)): 
            p2 = res2[i]
            set2 = set(p2)
            
            common = set1 & set2
            if len(common) == 2:
                score2 = sum(grid[r][c] for r, c in p2)
                
                current_total = score1 + score2
                
                if current_total > best_max:
                    best_max = current_total
                    
    return best_max
            

n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# Please write your code here.
# 상 하 좌 우
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
# step1. make a combination that 8 
res1 = step1()

# step2. choose the 8-connect path
_, res2 = step2(res1, 5)

# step3. choose 2 and compare to answer
answer = step3(res2)

print(answer)
