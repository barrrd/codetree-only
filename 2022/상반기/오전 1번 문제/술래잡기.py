# 1. init
n, m, h, k = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(m)]
tree = [[0]*n for _ in range(n)]
for _ in range(h):
    r, c = map(int,input().split())
    tree[r-1][c-1] = 1

runner = [[[0]*4 for _ in range(n)] for _ in range(n)]
for r, c, d in arr:
    runner[r-1][c-1][2*d-2] = 1 

chaser = [n//2, n//2] 
dr = [0, 0, 1, -1]
dc = [1, -1, 0, 0]
#     up right down left
ccr = [-1, 0, 1, 0]
ccc = [0, 1, 0, -1]
c_num = 0
cw = []
for idx in range(1, n):
    if idx == n - 1:
        cw.append(idx - 1 )
    else:
        cw.append(idx)
        cw.append(idx)
ccw = [c for c in cw[::-1]]
flag_cw = True
run_len = 1 # 현재 방향으로 몇 칸 이동해야 하는지 
run_cnt = 0 # 현재 방향으로 몇 칸 이동했는지 
turn_cnt = 0 # run_len을 몇 번 썼는지 (2번 쓰면)
# 2.execute
score = 0
for turn in range(k):
##############################
# step1. runner move
##############################
    chr, chc = chaser
    new_runner = [[[0]*4 for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            for d in range(4):
                if runner[r][c][d] == 0: continue
                if abs(chr - r) + abs(chc - c) > 3: 
                    new_runner[r][c][d] += runner[r][c][d]
                    continue
                temp = runner[r][c][d]
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < n and 0 <= nc < n:
                    if (nr,nc) == (chr, chc): 
                        new_runner[r][c][d] += temp
                    else:
                        new_runner[nr][nc][d] += temp
                else: # 방향 전환
                    if d <=1: # 우 좌
                        nd = (d+1) % 2
                        nr, nc = r + dr[nd], c + dc[nd]
                        if (nr,nc) == (chr, chc): 
                            new_runner[r][c][nd] += temp
                        else:
                            new_runner[nr][nc][nd] += temp
                    else:
                        nd = (d+1) % 2 + 2
                        nr, nc = r + dr[nd], c + dc[nd]
                        if (nr,nc) == (chr, chc): 
                            new_runner[r][c][nd] += temp
                        else:
                            new_runner[nr][nc][nd] += temp
    runner = new_runner
##############################
# step2. chaser move
##############################
    # 1. chaser 좌표
    """
    run_len = 1 # 현재 방향으로 몇 칸 이동해야 하는지 
    run_cnt = 0 # 현재 방향으로 몇 칸 이동했는지 
    turn_cnt = 0 # run_len을 몇 번 썼는지 (2번 쓰면)
    
    """
    
    cr, cc = chaser

    if flag_cw: # cw
        c_nr, c_nc = cr + ccr[c_num], cc + ccc[c_num]
        run_cnt += 1
        if run_len == run_cnt:
            turn_cnt += 1
            run_cnt = 0
            if turn_cnt == 2:
                run_len += 1
                run_cnt = 0
                turn_cnt = 0
            c_num = (c_num + 1) % 4 
        if (c_nr, c_nc) == (0,0):
            flag_cw = False
            run_cnt = 1
            turn_cnt = 1
            c_num = (c_num + 2) % 4
        chaser = [c_nr, c_nc]
    else: # ccw
        c_nr, c_nc = cr + ccr[c_num], cc + ccc[c_num]
        run_cnt += 1
        if (c_nr, c_nc) == (n//2,n//2):
            flag_cw = True
            c_num = (c_num - 2) % 4
            run_len = 1
            run_cnt = 0
            turn_cnt = 0
        if run_len == run_cnt:
            turn_cnt += 1
            run_cnt = 0
            if turn_cnt == 2:
                run_len -= 1
                run_cnt = 0
                turn_cnt = 0
            c_num = (c_num - 1) % 4 
        chaser = [c_nr, c_nc]
    ## 2. catch a chaser 방향 3칸 runner 
    ch_r, ch_c = chaser
    for check in range(3):
        # check_r, check_c = chaser
        check_r, check_c =  ch_r + check*ccr[c_num], ch_c + check*ccc[c_num]
        if not (0 <= check_r < n and 0 <= check_c < n):
            break
        if sum(runner[check_r][check_c]) > 0:
                if tree[check_r][check_c] == 1: 
                    continue
                score +=  (turn + 1) * sum(runner[check_r][check_c])
                runner[check_r][check_c] = [0]*4 
                 
print(score)







