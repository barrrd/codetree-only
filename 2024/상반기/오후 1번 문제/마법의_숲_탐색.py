from collections import deque
def can_down(r, c):
    flag = True
    for i in range(1,4):
        nr , nc = r + dr[i], c + dc[i]
        if not( 0 <= nr < R +3 and 0 <= nc < C) or arr[nr][nc] != 0: 
            flag = False
            break
    return flag

def can_west(r,c):
    flag = True
    check_lst = [(r-1,c-1), (r, c -2), (r+1, c-1), (r+1,c-2), (r+2,c-1)]
    for (nr,nc) in check_lst:
        if not( 0 <= nr < R +3 and 0 <= nc < C) or arr[nr][nc] != 0:
            flag = False
    return flag

def can_east(r,c):
    flag = True
    check_lst = [(r-1,c+1), (r, c +2), (r+1, c+1), (r+1,c+2), (r+2,c+1)]
    for (nr,nc) in check_lst:
        if not( 0 <= nr < R +3 and 0 <= nc < C) or arr[nr][nc] != 0:
            flag = False
    return flag

def update_arr(arr, number, c, d): # d: 북 동 남 서
    # 1. 이동
    curr_r, curr_c, curr_d = 1, c, d
    while True:
        if can_down(curr_r + 1, curr_c):
            curr_r += 1
        elif can_west(curr_r, curr_c):
            curr_r += 1
            curr_c -= 1
            curr_d = (curr_d - 1) % 4
        elif can_east(curr_r, curr_c):
            curr_r += 1
            curr_c += 1
            curr_d = (curr_d + 1) % 4
        else:
            break
    # 2. 1 <= curr < 3 이면 초기화
    if 1 <= curr_r <= 3:
        for r in range(R+3):
            for c_idx in range(C):
                arr[r][c_idx] = 0
        return False, None
    else: # 아닌떄에는 넣기!
        arr[curr_r][curr_c] = number
        er, ec = curr_r + dr[curr_d], curr_c + dc[curr_d]
        for i in range(4):
            nr, nc = curr_r + dr[i],curr_c + dc[i]
            if (er,ec) == (nr,nc):
                arr[nr][nc] = -number
            else:
                arr[nr][nc] = number
        return True, (curr_r, curr_c)

def bfs(arr, center): 
    global path_dict # [number, 최대 row]
    # 1. exits 찾기
    r, c = center
    q = deque([(r,c)])
    v = [[False]*C for _ in range(R+3)]
    v[r][c] = True
    max_r = 0
    while q:
        cr, cc = q.popleft()
        max_r = max(max_r, cr)
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not( 0 <= nr < R +3 and 0 <= nc < C) or v[nr][nc] or arr[nr][nc] == 0: continue
            if abs(arr[nr][nc]) == abs(arr[cr][cc]):
                v[nr][nc] = True
                q.append((nr,nc))
            elif arr[cr][cc] < 0:
                v[nr][nc] = True
                q.append((nr,nc))
    return max_r - 2
##############################################3
# 1. init
R, C, K = map(int,input().split())
arr = [[0]*C for _ in range(R+3)] # row: 0 ~ 2까지 존재하면 clear
orders = [list(map(int,input().split())) for _ in range(K)]
for idx in range(K):
    ci, di = orders[idx]
    orders[idx] = [ci - 1, di]
# exits: 북 동 남 서
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
answer = 0
# 2. execute
for number, [c, d] in enumerate(orders, start = 1): 
    #############################
    # step1. down
    #############################
    step1, center = update_arr(arr, number, c, d)

    #############################
    # step2. update arr
    #############################
    # 1. path 구하기
    if step1: # not clear
        answer += bfs(arr, center)
print(answer)

