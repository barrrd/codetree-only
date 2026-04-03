from collections import deque
def distance(r1, c1, r2, c2):
    return (r1- r2)**2 + (c1 - c2)**2

def step1():
    global sr, sc, sarr, spos, answer
    # 1. make a candidates which is sp
    best_min = float("inf")
    candidates = []
    for sid in spos.keys():
        r, c = spos[sid]
        dist = distance(r,c, sr, sc)
        if dist < best_min:
            candidates = [(r,c)]
            best_min = dist
        elif dist == best_min:
            candidates.append((r,c))
    candidates.sort(key = lambda x: (-x[0], -x[1]))

    # 2, move deaf
    # cw from 11
    dr = [-1, -1, -1, 0, 1, 1, 1, 0]
    dc = [-1, 0 , 1, 1, 1, 0, -1, -1]
    dist_min = float("inf")
    cr, cc = sr, sc
    dir = -1
    for i in range(8):
        nr, nc = cr + dr[i], cc + dc[i]
        if not (0 <= nr < n and 0 <= nc < n):
                continue

        dist = distance(nr, nc, *candidates[0])
        if dist < dist_min:
            dist_min = dist
            sr, sc = nr, nc
            dir = i

    # 3. 산타와 충돌 여부
    if sarr[sr][sc] > 0 :
        # 1. stunned
        stunned[sarr[sr][sc]] = turn + 2
        # 2. answer
        answer[sarr[sr][sc]] += C
        # 3. collusion and propagation
        step3(C, dr[dir], dc[dir])


def step2():
    global sarr, spos, answer
    # 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    for id in range(1, p + 1):
        if id not in spos:
            continue
        # 1. stunned 시 not move
        if stunned[id] > turn:
            continue
        # 2. move: move or not move
        cr, cc = spos[id]
        curr_dist = distance(cr, cc, sr, sc)

        ## 1. sarr
        sarr[cr][cc] = 0
        dir = -1
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not (0 <= nr < n and 0 <= nc < n) or sarr[nr][nc] > 0:
                continue

            nxt_dist = distance(nr, nc, sr, sc)

            if nxt_dist < curr_dist:
                curr_dist = nxt_dist
                dir = i

        if dir != -1:
            cr, cc = cr + dr[dir], cc + dc[dir]
        sarr[cr][cc] = id
        spos[id] = [cr,cc]

        # 3. 충돌 여부
        if (cr,cc) == (sr,sc): # 충돌
        # if sarr[sr][sc] > 0: # 충돌
            nxt_dr, nxt_dc = dr[(dir + 2) % 4], dc[(dir + 2) % 4]

            # 1. stunned
            stunned[sarr[sr][sc]] = turn + 2
            # 2. answer
            answer[sarr[sr][sc]] += D

            # 3. collusion and propagation
            step3(D, nxt_dr, nxt_dc)

def step3(move, ndr,ndc):
    global sarr, spos, answer
    # 1. collusion santa
    santa_id = sarr[sr][sc]

    # 2. move a santa
    sarr[sr][sc] = 0

    nr, nc = sr + move*ndr, sc + move*ndc

    q = deque([(santa_id, nr,nc)])
    while q:
        curr_id, nr, nc,  = q.popleft()
        # 격자 박
        if not(0 <= nr < n and 0 <= nc < n):
            del spos[curr_id]
            break

        nxt_id = sarr[nr][nc]

        sarr[nr][nc] = curr_id
        spos[curr_id] = [nr,nc]

        # 3. propagation: 산타 있음
        if nxt_id != 0:
            q.append((nxt_id, nr + ndr, nc + ndc))
        else:
            break

# 1. init
T = int(input())
for ts in range(1, T + 1):
    n, m, p, C, D = map(int,input().split())
    sr, sc = map(int,input().split())
    sr, sc = sr - 1, sc - 1 # 1.
    sarr = [[0]*n for _ in range(n)] # 2.
    spos = {} # 3.
    answer = {} # 4.
    stunned = {} # 5.
    for _ in range(p):
        sid, r, c = map(int, input().split())
        sarr[r - 1][c - 1] = sid
        spos[sid] = [r - 1, c - 1]
        answer[sid] = 0
        stunned[sid] = 0

    # 2. execute
    for turn in range(1, m + 1):
       # step1. move deaf
       step1()
       if not spos:
           break

       # step2. move santa
       step2()
       if not spos:
           break

       for id in answer.keys():
            if id in spos:
                answer[id] += 1

    print(*(answer[s_id] for s_id in sorted(answer.keys())))

