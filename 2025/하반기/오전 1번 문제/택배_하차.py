from collections import deque
def can_down(sr,sc, h, w):
    for chr in range(sr, sr + h):
        for chc in range(sc, sc + w):
            if not(0 <= chr < n and 0 <= chc < n) or arr[chr][chc] != 0:
                return False
    return True
def update(number):
    global arr, pos
    cr, cc, h, w = pos[number]
    sr, sc = cr, cc
    # 0. clear the cur
    for clr in range(cr, cr + h):
        for clc in range(cc, cc + w):
            arr[clr][clc] = 0
    # 1. find a start point
    while can_down(sr + 1, sc, h, w):
        sr += 1
    # 2. clear the prev
    pos[number] = [sr, sc, h, w]
    for mr in range(sr, sr + h):
        for mc in range(sc, sc + w):
            arr[mr][mc] = number


def can_remove(direction):
    global arr, pos
    candidate = None
    if direction == -1: # left
        for key in sorted(pos.keys()):
            sr, sc, h, w = pos[key]
            if sc == 0:
                candidate = key
                return candidate
            else:
                possible = True
                for rr in range(sr, sr + h):
                    for rc in range(0, sc):
                        if arr[rr][rc] != 0: 
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    candidate = key
                    return candidate
                else:
                    continue
    elif direction == 1: # right
        for key in sorted(pos.keys()):
            sr, sc, h, w = pos[key]
            if sc + w == n:
                candidate = key
                return candidate
            else:
                possible = True
                for rr in range(sr, sr + h):
                    for rc in range(sc + w, n):
                        if arr[rr][rc] != 0: 
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    candidate = key
                    return candidate
                else:
                    continue   
    return candidate



def left():
    global arr, pos
    # 1. choose a 택배
    number = can_remove(-1)
    # 2. remove
    if number: # remove
        ## 1. remove number
        sr, sc, h, w = pos[number]
        print(number)
        del pos[number]
        for rr in range(sr, sr + h):
            for rc in range(sc, sc+ w):
                arr[rr][rc] = 0
        ## 2. 모든 것에 대해서
        candidate_keys = list(pos.keys())

        ## 3. 
        if candidate_keys:
            cand_list = [(pos[k][0] + pos[k][2], k) for k in candidate_keys]
            cand_list.sort(key=lambda x: -x[0])
            for _, ca in cand_list:
                update(ca)
    if number:
        return True
    else: 
        return False

def right():
    global arr, pos
    # 1. choose a 택배
    number = can_remove(1)
    # 2. remove
    if number: # remove
        ## 1. remove number
        sr, sc, h, w = pos[number]
        print(number)
        del pos[number]
        for rr in range(sr, sr + h):
            for rc in range(sc, sc+ w):
                arr[rr][rc] = 0
        ## 2. 모든 것에 대해서
        candidate_keys = list(pos.keys())

        ## 3. 
        if candidate_keys:
            cand_list = [(pos[k][0] + pos[k][2], k) for k in candidate_keys]
            cand_list.sort(key=lambda x: -x[0])
            for _, ca in cand_list:
                update(ca)
    if number:
        return True
    else: 
        return False



# 1. init
n, m = map(int, input().split())
# k, h(세로), w(가로), c 
step0 = [list(map(int, input().split())) for _ in range(m)]
## 1. make a arr
pos = {}
arr = [[0]*n for _ in range(n)]
upper = {i:[] for i in range(n)}
for row in step0:
    k, h, w, c = row
    c -= 1
    sr, sc = 0, c
    # 1. find a start point
    while can_down(sr + 1, sc, h, w):
        sr += 1
    # 2. make a arr
    pos[k] = [sr, sc, h, w]
    for mr in range(sr, sr + h):
        for mc in range(sc, sc + w):
            arr[mr][mc] = k
pos = dict(sorted(pos.items(), key=lambda x: x[0]))

       
# # 2.execute
cnt = 0
while True:
    flag1, flag2 = False, False
    ##########################
    # step1. left
    ##########################
    if pos:
        flag1 = left()
    ##########################
    # step2. right
    ##########################
    if pos:
        flag2 = right()
    if not pos or not (flag1 or flag2):
        break
