def can_move(s_player, s_d, to_move=None):
    candidates = set()
    check_lst = []
    # print(players) # r, c, h, w, k
    r, c, h, w, k = players[s_player]
    is_valid = True
    possible = True
    if to_move is None:
            to_move = set([s_player])

    if s_d == 0: # 위
        for sc in range(c, c+w):
            if not(0 <= r - 1 < l and 0 <= sc < l):
                is_valid = False
                break
            if (r-1,sc) in wall:
                is_valid = False
                break
            if arr[r-1][sc] > 0:
                candidates.add(arr[r-1][sc])
                possible = False
    elif s_d == 1: # right
        for sr in range(r, r + h):
            if not(0 <= sr < l and 0 <= c + w < l):
                is_valid = False
                break
            if (sr,c + w) in wall:
                is_valid = False
                break
            if arr[sr][c + w] > 0:
                candidates.add(arr[sr][c + w])
                possible = False
    elif s_d == 2: # down
        for sc in range(c, c+w):
            if not(0 <= r + h  < l and 0 <= sc < l):
                is_valid = False
                break
            if ( r + h ,sc) in wall:
                is_valid = False
                break
            if arr[r + h][sc] > 0:
                candidates.add(arr[ r + h][sc])
                possible = False
    elif s_d == 3: # left
        for sr in range(r, r + h):
            if not(0 <= sr < l and 0 <= c - 1 < l):
                is_valid = False
                break
            if (sr,c-1) in wall:
                is_valid= False
                break
            if arr[sr][c-1] > 0:
                candidates.add(arr[sr][c-1])
                possible = False
    if not is_valid:
        return None
    if not possible:
        for nxt_player in candidates:
            if nxt_player not in to_move:
                to_move.add(nxt_player)
                temp = can_move(nxt_player,s_d,to_move)
                if temp is None:
                    return None
    return to_move
###############################################################
# 1. init
l, n, q = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(l)]
hazard = []
wall = []
for r in range(l):
    for c in range(l):
        if arr[r][c] == 1:
            hazard.append((r,c))
        if arr[r][c] == 2:
            wall.append((r,c))
        arr[r][c] = 0
players = {}
for i in range(1,n+1):
    r, c, h, w, k = map(int,input().split())
    for sr in range(r-1, r-1+h):
        for sc in range(c-1, c-1+w):
            arr[sr][sc] = i
    players[i] = [r-1,c-1,h,w,k]
commands = [list(map(int,input().split())) for _ in range(q)]
# 위 오른쪽 아 왼
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
# print(hazard)
# print(wall)
# print(players) # r, c, h, w, k
# print(arr)
"""
[(0, 2), (1, 2), (2, 0), (2, 1), (2, 3)]
[(3, 2)]
{1: [0, 1, 2, 1, 5], 2: [1, 0, 2, 1, 1], 3: [2, 1, 1, 2, 3]}
[[0, 0, 0, 0], [0, 0, 1, 0], [0, 2, 1, 0], [0, 2, 3, 3]]

"""
ans = {i:0 for i in range(1,n+1)}
# 2. execute
for i, (s_player, s_d) in enumerate(commands):
    #################################
    # step1. check to can move
    ################################
    # 1. died
    if s_player not in players:
        continue
    # 2. to check 
    candidates = []
    candidates = can_move(s_player, s_d)
    if candidates is None: # can not move
        continue
    # ################################
    # step2. damage
    # ################################
    # 1. move
    for candidate in candidates:
        ## 1. 기존 좌표 = 0
        r, c, h, w, k = players[candidate]
        for i in range(r, r + h):
            for j in range(c, c + w):
                arr[i][j] = 0
    ## 2. update
    for candidate in candidates:
        r, c, h, w, k = players[candidate]
        nr, nc = r + dr[s_d], c + dc[s_d]
        damage = 0
        if candidate != s_player: # 무적, only move
            for i in range(nr, nr + h):
                for j in range(nc, nc+ w):
                    if (i,j) in hazard:
                        damage += 1
        players[candidate][4] -= damage
        ans[candidate] += damage
        if players[candidate][4] > 0:
            players[candidate][0], players[candidate][1] = nr, nc
            for i in range(nr, nr + h):
                for j in range(nc, nc + w):
                    arr[i][j] = candidate
        else:
            del players[candidate]
            del ans[candidate]

answer = sum( v for v in ans.values()) 
print(answer)
