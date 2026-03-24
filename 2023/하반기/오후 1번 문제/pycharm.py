from collections import deque
def step1(turn):
    global arr, spos, stuned, der, dec
    # deaf move
    dr = [1, 1, 1, 0, 0, -1, -1, -1]
    dc = [1, 0, -1, 1, -1, 1, 0, -1]
    # 1. find the sp santa
    best_min1 = float("inf")
    cand1 = []
    for santa in spos.keys():
        santa_r, santa_c = spos[santa]
        curr_dist = (der -santa_r)**2 + (dec - santa_c)**2
        if best_min1 > curr_dist:
            best_min1 = curr_dist
            cand1 = [(santa, santa_r, santa_c)]
        elif best_min1 == curr_dist:
            cand1.append((santa, santa_r, santa_c))
    go_to_santa = sorted(cand1, key = lambda x: (-x[1], -x[2]))[0]
    # 2. find the nxt deaf pos
    target_id, tr, tc = go_to_santa
    best_min2 = float("inf")
    dir = -1
    fr, fc = -1, -1
    for i in range(8):
        nr, nc = der + dr[i], dec + dc[i]
        if not(0 <= nr < n and 0 <= nc < n): continue
        curr_dist2 = (tr - nr)**2 + (tc - nc)**2
        if best_min2 > curr_dist2:
            best_min2 = curr_dist2
            dir = i
            fr, fc = nr, nc
    # 3. update the deaf and is collision
    if arr[fr][fc] == 0: # not 충돌
        arr[der][dec] = 0
        der, dec = fr, fc
        arr[der][dec] = -1
        return False, [], None
    else: # 충돌
        coll_santa = arr[fr][fc]
        arr[der][dec] = 0
        der, dec = fr, fc
        arr[der][dec] = -1
        stuned[coll_santa] = turn + 2
        return True, coll_santa, dir
    
def step3(mux, dir, santa,dr,dc):
    global arr, spos, stuned, der, dec, answer
    # 충돌한 산타 spos 수정 > 상호작용
    sr, sc = spos[santa]
    nr, nc = sr + (mux-1)*dr[dir], sc + (mux-1)*dc[dir]

    if not(0 <= nr < n and 0 <= nc < n): # 밖으로 나감
        del spos[santa]
    else: # 벽 안
        if arr[nr][nc] == 0: # not 충돌
            spos[santa] = [nr,nc]
            arr[nr][nc] = santa
        else: # 충돌
            nxt_santa = arr[nr][nc]
            arr[nr][nc] = 0
            nxr, nxc = nr, nc
            spos[santa] = [nr,nc]
            arr[nr][nc] = santa
            flag = True
            while flag:
                next_r, next_c = nxr + dr[dir], nxc + dc[dir]
                if not(0 <= next_r < n and 0 <= next_c < n): # 밖으로 나감
                    del spos[nxt_santa]
                    flag = False
                else: # 벽 안
                    if arr[next_r][next_c] == 0:  # not 충돌
                        spos[nxt_santa] = [next_r, next_c]
                        arr[next_r][next_c] = nxt_santa
                        flag = False
                    else: # 충돌
                        spos[nxt_santa] = [next_r, next_c]
                        nxr, nxc = next_r, next_c
                        prev_santa = arr[next_r][next_c]
                        arr[next_r][next_c] = nxt_santa
                        nxt_santa = prev_santa



def step2(turn):
    global arr, spos, stuned, der, dec, answer
    # santa move 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    for santa in range(1, p + 1):
        if santa in spos: #
            if stuned[santa] <= turn:
                sr, sc = spos[santa]
                curr_dist = (der - sr)**2 + (dec - sc)**2
                fr, fc = -1, -1
                dir = - 1
                for i in range(4):
                    nr, nc = sr + dr[i], sc + dc[i]
                    if not (0 <= nr < n and 0 <= nc < n) or arr[nr][nc] > 0: continue
                    nxt_dist = (der - nr)**2 + (dec - nc)**2
                    if nxt_dist < curr_dist:
                        curr_dist = nxt_dist
                        fr, fc = nr, nc
                        dir = i
                if dir != -1: # move
                    if arr[fr][fc] == -1: # 루돌프와 충돌
                        arr[sr][sc] = 0
                        answer[santa - 1] += d
                        stuned[santa] = turn + 2
                        step3(d, (dir+2)%4, santa, dr, dc)
                    else: # 충돌 x
                        arr[sr][sc] = 0
                        spos[santa] = [sr + dr[dir], sc + dc[dir]]
                        arr[sr + dr[dir]][sc + dc[dir]] = santa

# 1.init
# T = int(input())
T = 1
for ts in range(1, T + 1):
    n, m, p, c, d = map(int, input().split())
    der, dec =  map(int, input().split()) # 1.
    der, dec = der - 1, dec -1
    spos = {} # 2.
    stuned = {} # 3.
    answer = [0 for _ in range(p)]
    arr = [[0]*n for _ in range(n)] # 4.
    for _ in range(1, p + 1):
        sid, sr, sc = map(int, input().split())
        sr, sc = sr - 1, sc - 1
        spos[sid] = [sr,sc]
        arr[sr][sc] = sid
        stuned[sid] = 0
    arr[der][dec] = -1

    for turn in range(1, m + 1):
        if not spos:
            break
        #######################################
        # step1. deaf move: find the move pos and not move
        #######################################
        is_deaf_collision, coll_santa, dir = step1(turn)
        if is_deaf_collision: # 충돌: collision and interation and stunned
            answer[coll_santa - 1] += c
            # deaf move
            dr = [1, 1, 1, 0, 0, -1, -1, -1]
            dc = [1, 0, -1, 1, -1, 1, 0, -1]
            step3(c + 1, dir, coll_santa,dr,dc)
            if not spos:
                break
            step2(turn)
            if not spos:
                break
        else: # not 충돌
            step2(turn)
            if not spos:
                break
        for key in spos.keys():
            answer[key - 1] += 1

    print(*answer)
