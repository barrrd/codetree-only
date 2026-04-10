H, W = map(int, input().split())
arr = [list(input()) for _ in range(H)]

# Please write your code here.
from collections import deque
def step1():
    for r in range(H - 1, - 1, -1):
        for c in range(W - 1, - 1, - 1):
            if arr[r][c] == ".":
                continue

            sharp_cnt = 0
            dir = -1
            for i in range(4):
                if sharp_cnt > 2:
                    break
                nr, nc = r + dr[i], c + dc[i]
                if not(0 <= nr  < H and 0 <= nc < W ):
                    continue
                if arr[nr][nc] == "#":
                    sharp_cnt += 1
                    dir = i
            
            if sharp_cnt == 1:
                return r, c, dir

def can_go(r,c,d,v):
    # 1. can_left or right okay?
    nr1, nc1 = r + dr[d], c + dc[d]
    if not(0 <= nr1 < H and 0 <= nc1 < W) or v[nr1][nc1] or arr[nr1][nc1] == ".":
        return False
    
    # 2. can go 2 times okay
    for i in range(1, 3):
        nr, nc = r + i*dr[d], c + i*dc[d]
        if not(0 <= nr < H and 0 <= nc < W) or v[nr][nc] or arr[nr][nc] == ".":
            return False
    
    # 3. update a v
    for i in range(1,3):
        nr, nc = r + i*dr[d], c + i*dc[d]
        v[nr][nc] = True

    return True

    
def step2(sr, sc, curr_d):
    result = ""
    
    v = [[False]*W for _ in range(H)]
    v[sr][sc] = True
    cr, cc, cd = sr, sc, curr_d
    while True:
  
        can_move = True
        for ni in range(1,3):
            nr, nc = cr + ni*dr[cd], cc + ni*dc[cd]
            if not(0 <= nr < H and 0 <= nc < W) or v[nr][nc] or arr[nr][nc] == ".":
                can_move = False
                break
        # Case1. 직진
        if can_move:
            for ni in range(1,3):
                nr, nc = cr + ni*dr[cd], cc + ni*dc[cd]
                v[nr][nc] = True
            cr, cc = nr, nc
            result += "A"
        # Case2. l or R
        else:
            left_d = (cd - 1) % 4
            right_d = (cd + 1) % 4
            # left
            if can_go(cr,cc,left_d, v):
                cd = left_d
                result += "LA"
            elif can_go(cr,cc,right_d, v):
                cd = right_d
                result += "RA"

            else:
                break

            cr += 2 * dr[cd]
            cc += 2 * dc[cd]
    return result

# step1. find the start or end point
# 북 동 남 서
dr = [-1, 0, 1, 0] 
dc = [0, 1, 0, -1]
ser, sec, dir = step1()
print(ser + 1, sec + 1)
get_dir = {0: "^", 1: ">", 2: "v", 3: "<"}
print(get_dir[dir])

# step2. find the candidates
answer = step2(ser, sec, dir)
print(answer)
