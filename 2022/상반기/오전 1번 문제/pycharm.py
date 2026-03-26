from collections import deque
def step0():
    paths = []
    # 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    paths = []
    # 1. forward
    sr, sc = tr, tc
    dir = 0
    count = 1
    stop = False
    while True:
        for i in range(2):
            for cnt in range(count):
                if stop:
                    break
                nr, nc = sr + dr[dir], sc + dc[dir]
                sr, sc = nr, nc
                if cnt == count - 1:
                    dir = (dir + 1) % 4
                elif (nr, nc) == (0, 0):
                    dir = (dir + 2) % 4
                    stop =  True
                paths.append((nr,nc,dir))
            if stop:
                break
        count += 1
        if stop:
            break
    # 2. backward
    reversed_paths = list(reversed(paths))
    reversed_paths.append((tr,tc,1))
    sr, sc = paths[-2][:2]
    for nr, nc, _ in reversed_paths[1:]:
        for i in range(4):
            rr, cc = sr + dr[i], sc + dc[i]
            if (nr,nc) == (rr,cc):
                paths.append((sr, sc, i))
                sr, sc = nr, nc
                break
    paths.append((tr,tc,0))
    return paths

def step1(turn, paths):
    global ppos
    # 좌 우 하 상
    dr = [0, 0, 1, -1]
    dc = [1, -1, 0, 0]
    target_r, target_c = paths[(turn - 1 - 1) % len(paths)][:2]
    for pid in range(1, m + 1):
        if pid not in ppos: continue
        pr, pc, pd = ppos[pid]
        dist = abs(target_r - pr) + abs(target_c - pc)

        if dist > 3: continue

        if pd > 0:
            dir = 2*(pd - 1)
        else:
            dir = 2*(abs(pd) - 1) + 1

        nr, nc =  pr + dr[dir], pc + dc[dir]
        if 0 <= nr < n and 0 <= nc < n : # 격자 안
            if (nr,nc) != (target_r, target_c):
                ppos[pid][:2] = [nr,nc]
        else: # 격자 밖
            pd = -pd
            ppos[pid][2] = pd

            if pd > 0:
                dir = 2 * (pd - 1)
            else:
                dir = 2 * (abs(pd) - 1) + 1

            nr, nc =  pr + dr[dir], pc + dc[dir]
            if (nr,nc) != (target_r, target_c):
                ppos[pid][:2] = [nr,nc]

def step2(turn,paths):
    global ppos, answer
    tr, tc, td = paths[(turn - 1) % len(paths)]
    # 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    check_lst = []
    for i in range(3):
        nr, nc = tr + dr[td]*i, tc + dc[td]*i
        if not(0 <= nr < n and 0 <= nc < n):
            break
        check_lst.append((nr,nc))

    for pid in range(1,m+1):
        if pid not in ppos: continue
        pr, pc = ppos[pid][:2]
        if (pr,pc) in check_lst:
            if arr[pr][pc]  == 1 : continue
            answer += turn
            del ppos[pid]

# 1. init
T = 1
# T = 1
for ts in range(1, T + 1):
    # if ts == 2:
    #      break
    n, m, h, k = map(int,input().split())
    ppos = {}

    for pid in range(1, m + 1):
        x, y, d = map(int,input().split())
        x, y = x - 1, y - 1
        ppos[pid] = [x, y, d]
    tr, tc = n // 2, n // 2
    arr = [[0] * n for _ in range(n)]
    # arr[tr][tc] = 2
    for _ in range(h):
        x, y = map(int,input().split())
        x, y = x - 1, y - 1
        arr[x][y] = 1
    # step0. make a 술래 paths
    paths = step0()
    answer = 0
    for turn in range(1, k + 1):

        # step1. player move
        step1(turn, paths)
        # step2.
        step2(turn, paths)
        tr, tc = paths[(turn - 1) % len(paths)][:2]

        if not ppos:
            break
    print(answer)
