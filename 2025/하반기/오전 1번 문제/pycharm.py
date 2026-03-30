from collections import deque
def can_down(cr, cc, h, w):
    possible = True
    for r in range(cr, cr + h):
        for c in range(cc, cc + w):
            if not(0 <= r < n  and 0 <= c < n) or arr[r][c] !=0:
                possible = False
                return possible
    return possible

def step0(orders):
    global arr, bpos
    for bid in orders:
        if bid not in bpos: continue
        # 1. find the sr
        sc, h, w = bpos[bid]
        sr = 0
        while  can_down(sr + 1, sc, h, w):
            sr += 1

        # 2. update a arr and bpos
        for r in range(sr, sr + h):
            for c in range(sc, sc + w):
                arr[r][c] = bid
        bpos[bid] = [sr, sc, h, w]

def step1():
    global arr, bpos
    for bid in list(bpos.keys()):
        # 1, check to remove
        sr, sc, h, w = bpos[bid]

        ## 2.
        possible = True
        for r in range(sr, sr + h):
            for c in range(sc):
                if not (arr[r][c] == 0 or arr[r][c] == bid):
                    possible = False
                    break
            if not possible:
                break

        if possible:
            for r in range(sr, sr + h):
                for c in range(sc, sc + w):
                    arr[r][c] = 0
            del bpos[bid]
            print(bid)

            # ## 연쇄작용: down
            ## 2.1 make a candidates
            candidates = []
            v = set()
            v.add(0)
            for check_r in range(sr -1, -1, -1):
                for check_c in range(n):
                    if arr[check_r][check_c] not in v:
                        candidates.append(arr[check_r][check_c])
                        v.add(arr[check_r][check_c])
            # 2.2 update a arr and bpos
            if candidates:
                for tid in candidates:
                    ## 2.3 can down
                    tr, tc, th, tw = bpos[tid]
                    for r in range(tr, tr + th):
                        for c in range(tc, tc + tw):
                            arr[r][c] = 0

                    while can_down(tr + 1, tc, th, tw):
                        tr += 1

                    # 2.4 update a arr and bpos
                    for r in range(tr, tr + th):
                        for c in range(tc, tc + tw):
                            arr[r][c] = tid
                    bpos[tid] = [tr, tc, th, tw]
            return

def step2():
    global arr, bpos
    for bid in list(bpos.keys()):
        # 1, check to remove
        sr, sc, h, w = bpos[bid]

        ## 2.
        possible = True
        for r in range(sr, sr + h):
            for c in range(sc + w, n): # !!
                if not (arr[r][c] == 0 or arr[r][c] == bid):
                    possible = False
                    break
            if not possible:
                break
        if possible:
            for r in range(sr, sr + h):
                for c in range(sc, sc + w):
                    arr[r][c] = 0
            del bpos[bid]
            print(bid)

            # ## 연쇄작용: down
            ## 2.1 make a candidates
            candidates = []
            v = set()
            v.add(0)
            for check_r in range(sr -1, -1, -1):
                for check_c in range(n):
                    if arr[check_r][check_c] not in v:
                        candidates.append(arr[check_r][check_c])
                        v.add(arr[check_r][check_c])
            # 2.2 update a arr and bpos
            if candidates:
                for tid in candidates:
                    ## 2.3 can down
                    tr, tc, th, tw = bpos[tid]
                    for r in range(tr, tr + th):
                        for c in range(tc, tc + tw):
                            arr[r][c] = 0

                    while can_down(tr + 1, tc, th, tw):
                        tr += 1

                    # 2.4 update a arr and bpos
                    for r in range(tr, tr + th):
                        for c in range(tc, tc + tw):
                            arr[r][c] = tid
                    bpos[tid] = [tr, tc, th, tw]
            return


# 1.init
T = 1
for ts in range(1, T + 1):
    n, m = map(int,input().split())
    bpos = {}  # 1.
    orders = []
    for _ in range(m):
        k, h, w, c = map(int,input().split())
        orders.append(k)
        c -= 1
        bpos[k] = [c,h,w]
    arr = [[0]*n for _ in range(n)] # 2.
    # step0: put the block(택배) and update a arr
    step0(orders)
    bpos = dict(sorted(bpos.items()))
    while True:
        # step1. left
        step1()
        if not bpos:
            break
        # step2. right
        step2()
        if not bpos:
            break
