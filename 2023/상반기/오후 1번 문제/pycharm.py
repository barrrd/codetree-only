from collections import deque


def step1():
    global arr, parr, ppos
    ans = 0
    for player in list(ppos.keys()):
        pr, pc = ppos[player]
        moved = False
        parr[pr][pc] -= 1
        for i in range(4):
            nr, nc = pr + dr[i], pc + dc[i]
            if not(0 <= nr < n and 0 <= nc < n) or 1 <= arr[nr][nc] <= 9: continue
            curr_dist = abs(pr - er) + abs(pc - ec)
            nxt_dist = abs(nr - er) + abs(nc  - ec)
            if curr_dist > nxt_dist:
                moved = True
                if (nr,nc) == (er,ec):
                    del ppos[player]
                break
        if moved:
            if (nr,nc) != (er,ec):
                parr[nr][nc] += 1
                ppos[player] = [nr, nc]
            ans += 1
        else: # not move
            parr[pr][pc] += 1
    return ans

def rotate(sr, sc, length):
    global arr, parr, ppos, er, ec
    new_arr = [row[:] for row in arr]
    new_parr = [row[:] for row in parr]
    # 1. ppos 리스트
    row_range = [i for i in range(sr, sr + length)]
    col_range = [i for i in range(sc, sc + length)]
    change_player = []
    for key, value in ppos.items():
        if value[0] in row_range and value[1] in col_range:
            change_player.append(key)
    for player in change_player:
        pr, pc = ppos[player]
        # 1.
        prr, pcc = pr - sr, pc - sc
        # 2.
        pprr, ppcc = pcc, length - 1 - prr
        # 3.
        ppos[player] = [sr + pprr, sc + ppcc]

    # 2. rotate
    for start_r in range(sr, sr + length):
        for start_c in range(sc, sc + length):
            # 1.
            orr, occ = start_r - sr, start_c - sc
            # 2. # 0,1 > 1, 2
            rr, cc = occ, length - orr - 1
            # 3.
            if 1 <= arr[start_r][start_c] <= 9:
                arr[start_r][start_c] -= 1
            elif arr[start_r][start_c] == - 1:
                er, ec = sr + rr, sc + cc
            new_arr[sr + rr][sc + cc] = arr[start_r][start_c]
            new_parr[sr + rr][sc + cc] = parr[start_r][start_c]

    arr = new_arr
    parr = new_parr

def step2():
    global arr, parr, ppos
    # 1. 한명 이상 참가자 + 출구
    # r, c를 크기별로 check
    found_p = False
    found_e = False
    for length in range(2,n + 1):
        for sr in range(n - length + 1):
            for sc in range(n - length + 1):
                found_p = False
                found_e = False
                for cr in range(sr, sr + length):
                    for cc in range(sc, sc + length):
                        if (cr, cc) == (er, ec):
                            found_e = True
                        if parr[cr][cc] != 0:
                            found_p = True
                if found_p and found_e:
                    break
            if found_p and found_e:
                break
        if found_p and found_e:
            break
    # 2. rotate
    rotate(sr, sc, length)

# 1.init
# T = int(input())
T = 1
for ts in range(1, T + 1):
    n, m, k = map(int,input().split())
    arr = [list(map(int,input().split())) for _ in range(n)]
    players = [list(map(int,input().split())) for _ in range(m)]
    parr = [[0]*n for _ in range(n)]
    ppos = {}
    for i in range(m):
        rrr, ccc = players[i]
        players[i] = rrr - 1, ccc - 1
        ppos[i + 1] = players[i]
        parr[rrr-1][ccc-1] += 1
    er, ec = map(int,input().split())
    er, ec = er - 1, ec - 1
    arr[er][ec] = -1
    # 상 하 좌 우
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    # 2. execute
    ans1 = 0
    for turn in range(1, k + 1):
        if not ppos:
            break
        ############################
        # step1. players move
        ############################
        ans1 += step1()
        ############################
        # step2. rotate
        ############################
        if not ppos:
            break
        step2()
    print(ans1)
    print(er+1,ec+1)


