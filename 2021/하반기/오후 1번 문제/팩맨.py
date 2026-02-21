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



# # 2. execute
# ######################################
# # step
# ######################################
# for turn in range(t):
# ######################################
# # step1&2. copy monster and monster move
# ######################################
#     eggs = []
#     dead_pos = {(r, c) for (r, c, _) in dead}
#     tmp_pos = []

#     new_arr = []
#     new_loc = [[0]*4 for _ in range(4)]
#     pr, pc = ploc[0]-1, ploc[1]-1
#     # new_loc[pr][pc] = -1

#     for i in range(len(arr)):
#         r, c, cur_d = arr[i]
#         eggs.append((arr[i][:]))
#         move = False
#         for d in range(8):
#             nd = (cur_d + d) % 8
#             nr, nc = r + mr[nd], c + mc[nd]
#             if not(0 <= nr < 4 and 0 <= nc <4):
#                 continue
#             if (nr,nc)==(pr,pc):
#                 continue
#             if (nr, nc) not in dead_pos:
#                     new_arr.append([nr, nc, nd])
#                     new_loc[nr][nc] += 1
#                     tmp_pos.append([nr, nc])
#                     move = True
#                     break
#         if not move:
#             new_arr.append([r, c, cur_d])
#             new_loc[r][c] += 1
#     arr = new_arr
#     # print(loc)
#     loc = new_loc
# ######################################
# # step3.packman move
# ######################################
#     best = -1
#     best_path = None
#     dead_loc_turn = ()
#     for pro in products:
#         pos = []
#         number = 0
#         visited = set()
#         cr,cc = pr, pc
#         possible = True
#         for p in pro:
#             nr, nc = cr + ppr[p], cc + ppc[p]
#             if not(0 <= nr < 4 and 0 <= nc <4):
#                 possible = False
#                 break
#             if (nr,nc) not in visited:
#                 number += loc[nr][nc]
#                 visited.add((nr,nc))
#                 if loc[nr][nc] > 0:
#                     pos.append((nr,nc,turn))
#             cr, cc = nr, nc
#         if possible:
#             if best < number:
#                 best = number
#                 best_path = [cr,cc]
#                 dead_loc_turn = tuple(pos)


#     ploc = [best_path[0] + 1, best_path[1] + 1]
#     dead_cells = {(r, c) for (r, c, _) in dead_loc_turn}
#     arr = [m for m in arr if (m[0], m[1]) not in dead_cells]
#     for r, c in dead_cells: loc[r][c] = 0 # << 격자 0으로 초기화

# ######################################
# # step4.update the dead
# ######################################
#     dead = {(r, c, t) for (r, c, t) in dead if t + 2 > turn}
        
# ######################################
# # step5. hatch the eggs
# ######################################
#     # print(eggs)
#     for egg in eggs:
#         arr.append(egg)

#     for dea in dead_loc_turn:
#         dead.add(dea)

# print(len(arr))
