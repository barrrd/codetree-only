from collections import deque
def product(lst,k):
    result = []
    path = []
    def backtracking():
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(len(lst)):
            path.append(lst[i])
            backtracking()
            path.pop()
    backtracking()
    return result

# 1. init
m, t = map(int, input().split())
ploc = list(map(int, input().split()))
dead = set()
loc = [[0]* 4 for _ in range(4)]
mr = [-1, -1, 0, 1, 1, 1, 0, -1]
mc = [0, -1, -1, -1, 0, 1, 1, 1]

monster_grid = [[[0]*8 for _ in range(4)] for _ in range(4)]
for _ in range(m):
    r, c, d = map(int,input().split())
    monster_grid[r-1][c-1][d-1] += 1

ppr = [-1, 0, 1, 0]
ppc = [0, -1, 0, 1]


loc[ploc[0] - 1][ploc[1] - 1] = -1

products = product([0,1,2,3], 3)

pr, pc = ploc[0]-1, ploc[1]-1


# 2. execute
for turn in range(t):
    # Step 1. 몬스터 복제 (현재 상태 저장)
    eggs = [[grid[:] for grid in row] for row in monster_grid]
    
    # Step 2. 몬스터 이동
    dead_pos = {(r, c) for (r, c, _) in dead}
    new_grid = [[[0]*8 for _ in range(4)] for _ in range(4)]
    
    for r in range(4):
        for c in range(4):
            for d in range(8):
                if monster_grid[r][c][d] == 0: continue
                
                cnt = monster_grid[r][c][d]
                moved = False
                for i in range(8):
                    nd = (d + i) % 8
                    nr, nc = r + mr[nd], c + mc[nd]
                    if 0 <= nr < 4 and 0 <= nc < 4 and (nr, nc) != (pr, pc) and (nr, nc) not in dead_pos:
                        new_grid[nr][nc][nd] += cnt
                        moved = True
                        break
                if not moved:
                    new_grid[r][c][d] += cnt
    monster_grid = new_grid

    # Step 3. 팩맨 이동
    # 이동 경로 결정을 위해 칸별 몬스터 합계 계산
    loc = [[sum(monster_grid[r][c]) for c in range(4)] for r in range(4)]
    
    best = -1
    best_path = (pr, pc)
    eaten_cells = []
    
    for pro in products:
        visited = set()
        cr, cc = pr, pc
        number = 0
        possible = True
        temp_path = []
        for p in pro:
            nr, nc = cr + ppr[p], cc + ppc[p]
            if not (0 <= nr < 4 and 0 <= nc < 4):
                possible = False; break
            if (nr, nc) not in visited:
                number += loc[nr][nc]
                visited.add((nr, nc))
            temp_path.append((nr, nc))
            cr, cc = nr, nc
        
        if possible and number > best:
            best = number
            best_path = (cr, cc)
            eaten_cells = temp_path

    # 몬스터 먹기 및 시체 생성
    pr, pc = best_path
    dead_loc_turn = []
    for er, ec in eaten_cells:
        if sum(monster_grid[er][ec]) > 0:
            monster_grid[er][ec] = [0]*8 # 해당 칸 몬스터 전멸
            dead_loc_turn.append((er, ec, turn))

    # Step 4. 시체 소멸 업데이트
    dead = {d for d in dead if d[2] + 2 > turn}
        
    # Step 5. 알 부화 및 시체 추가
    for r in range(4):
        for c in range(4):
            for d in range(8):
                monster_grid[r][c][d] += eggs[r][c][d]
    
    for d in dead_loc_turn:
        dead.add(d)

# 최종 결과 계산
ans = 0
for r in range(4):
    for c in range(4):
        ans += sum(monster_grid[r][c])
print(ans)

"""
from collections import deque
#
def product(lst, k):
    result = []
    path = []
    def backtrack():
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(len(lst)):
            path.append(lst[i])
            backtrack()
            path.pop()
    backtrack()
    return result



# 1. init
## 1. graph
m, t = map(int, input().split())
p_pos = list(map(int, input().split()))
p_pos = [p_pos[0] - 1, p_pos[1] -1 ]
arr = [list(map(int, input().split()))for _  in range(m)]
arr = [[a[0] - 1, a[1] - 1, a[2] - 1] for a in arr]
graph = [[[0]*8 for _ in range(4)] for _ in range(4)] # [r,c,d]
for r, c, d in arr:
    graph[r][c][d] +=1
"""
[
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0]],
[[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
]
"""
## 2.dir
mdr = [-1, -1, 0, 1, 1, 1, 0, -1]
mdc = [0, -1, -1, -1, 0, 1, 1, 1]
pdr = [-1, 0, 1, 0]
pdc = [0, -1, 0, 1]

# 2. execute
dead = set() # [r,c,turn]
for turn in range(t):
###############################
# step1. make a eggs
###############################
    eggs = [[r[:] for r in row]for row in graph]
    # print(eggs)
###############################
# step2. monster move
###############################
    new_graph = [[[0]*8 for _ in range(4)]for _ in range(4)]
    new_dead = {(r, c) for r, c, _ in dead}
    pr, pc = p_pos
    for r in range(4):
        for c in range(4):
            for d in range(8):
                if graph[r][c][d] == 0:
                    continue
                cnt = graph[r][c][d]
                moved = False
                for i in range(8):
                    nd = (d + i) % 8
                    nr, nc = r + mdr[nd], c + mdc[nd]
                    if not(0 <= nr < 4 and 0 <= nc < 4): continue
                    if (nr, nc) in new_dead: continue
                    if (nr, nc) == (pr, pc): continue
                    new_graph[nr][nc][nd] += cnt
                    moved = True
                    break
                if not moved:
                    new_graph[r][c][d] += cnt
    graph = new_graph

###############################
# step3. packman move
###############################
    temp = [0,1,2,3]
    best = -1
    best_path = [pr, pc]
    eaten_cells = []
    for plst in product(temp,3):
        visited = set()
        number = 0
        cr, cc = pr, pc
        temp_path = []
        possible = True
        for p in plst:
            nr, nc = cr + pdr[p], cc + pdc[p]
            if not(0 <= nr < 4 and 0 <= nc < 4): 
                possible = False
                break
            temp_path.append((nr, nc))
            if (nr,nc) not in visited:
                visited.add((nr,nc))
                number += sum(graph[nr][nc])
            
            cr, cc = nr, nc
        if possible and best < number:
            best = number
            best_path = [cr, cc]
            eaten_cells = temp_path
    temp_dead = []
    for er, ec in eaten_cells:
        if sum(graph[er][ec]) > 0:
            temp_dead.append((er,ec,turn))
            graph[er][ec] = [0]*8
    p_pos = best_path
###############################
# step4. update a dead
###############################
    dead = {d for d in dead if d[2] + 2 > turn}
    for temp in temp_dead:
        dead.add(temp)
###############################
# step5. hatch a eggs
###############################
    for r in range(4):
        for c in range(4):
            for d in range(8):
                graph[r][c][d] += eggs[r][c][d] 

# 3. answer
answer = 0
for r in range(4):
    for c in range(4):
        answer += sum(graph[r][c])
print(answer)
"""
