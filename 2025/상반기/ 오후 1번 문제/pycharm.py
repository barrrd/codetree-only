from collections import deque


def step0(input_id):
    global bpos
    r1, c1, r2, c2 = map(int,input().split())
    bpos[input_id] = {
        "shape": [],
        "size": 0,
        "min": [n,n]
    } #
    size = 0
    for r in range(r1, r2):
        for c in range(c1, c2):
            bpos[input_id]["shape"].append((r,c))
            bpos[input_id]["min"][0] = min(r, bpos[input_id]["min"][0])
            bpos[input_id]["min"][1] = min(c, bpos[input_id]["min"][1])
            size += 1

    bpos[input_id]["size"] = size

def step1(input_id):
    global arr, bpos
    attacked = set()
    for (r,c) in bpos[input_id]["shape"]:
        if arr[r][c] != 0:
            attacked_id = arr[r][c]
            attacked.add(arr[r][c])
            bpos[attacked_id]["size"] -= 1
            bpos[attacked_id]["shape"].remove((r,c))
        arr[r][c] = input_id
    if attacked:
        return True, attacked
    else:
        return False, []

def step2(id):
    global arr, bpos
    # 1. update a min_r, min_c
    new_r, new_c = n, n
    for r,c in bpos[id]["shape"]:
        new_r, new_c = min(new_r, r), min(new_c, c)
    bpos[id]["min"] = [new_r, new_c]


    # 2. is_possbile
    shape = bpos[id]["shape"]
    size = bpos[id]["size"]
    # 상 우 하 좌
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    sr,sc = shape[0]
    tmp = 1

    q = deque([(sr,sc)])
    v = set()
    v.add((sr,sc))
    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            if not(0 <= nr < n and 0 <= nc < n) or (nr,nc) in v:
                continue
            if arr[nr][nc] != id:
                continue
            q.append((nr,nc))
            v.add((nr,nc))
            tmp += 1
    # 2.
    if size != tmp: # 2개
        del bpos[id]
        # print(f"2개 이상인 id: {id}")
    # else:
    #     print(input_id)
    #     print(" safe")

def step3():
    global arr, bpos
    # 1. make a candidates
    new_arr = [[0]*n for _ in range(n)]
    new_bpos = {}

    candidates = []
    for id in bpos.keys():
        candidates.append((bpos[id]["size"], id))

    candidates.sort(key = lambda x: (-x[0], x[1]))

    # 2. put the candidate and update arr, bpos
    for size, id in candidates:
        shape = bpos[id]["shape"]
        new_bpos[id] = {
            "size" : size,
            "shape" : [],
            "min" : [n,n]
        }
        ## 1. input 가능한지
        for r in range(n):
            for c in range(n):
                is_possible = True
                min_r, min_c = bpos[id]["min"]
                shape = bpos[id]["shape"]
                for (rr,rc) in shape:
                    orr, occ = r + rr - min_r, c + rc - min_c
                    if not (0 <= orr < n and 0 <= occ < n) or new_arr[orr][occ] != 0:
                        is_possible = False
                        break
                if is_possible:
                    break
            if is_possible:
                break
        ## 2. 가능한 경우 update arr ,pos
        if is_possible:
            # new_arr and bpos
            new_r, new_c = n, n
            for (sr,sc) in shape:
                fr, fc = r + sr - min_r, c + sc - min_c
                new_arr[fr][fc] = id

                new_bpos[id]["shape"].append((fr, fc))
                new_r, new_c = min(new_r, fr), min(new_c, fc)

            new_bpos[id]["min"] = [new_r, new_c]
        else:
            del new_bpos[id]

    arr = new_arr
    bpos = new_bpos


def step4():
    # 1: 연결 , 0: 연결 x
    adj = set()
    for id in bpos.keys():
        for r, c in bpos[id]["shape"]:
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if not(0 <= nr < n and 0 <= nc < n):
                     continue

                opp_id = arr[nr][nc]
                if opp_id != 0 and opp_id != id:
                    pair = tuple(sorted((id, opp_id)))
                    adj.add(pair)

    # 2. answer
    answer = 0
    for id1, id2 in adj:
        answer += bpos[id1]["size"] * bpos[id2]["size"]
    print(answer)



# 1. init
T = int(input())
for ts in range(1, T + 1):
    n, q= map(int,input().split())
    bpos = {}  # 1.
    arr= [[0]*n for _ in range(n)] # 2.

    # 2. execute
    for input_id in range(1, q + 1):
        # step0. make a bpos
        step0(input_id)
        # step1. put the 미생물
        is_attacked, attacked_set = step1(input_id)
        if is_attacked: # 분할 여부!:
            attacked_id = list(sorted(attacked_set))

            # step2. 2개 이상인지 판단 >
            for id in attacked_id:
                if bpos[id]["size"] > 0:
                    step2(id)
                else:
                    del bpos[id]
        # step3. move a input_id
        step3()
        # step4.
        step4()


