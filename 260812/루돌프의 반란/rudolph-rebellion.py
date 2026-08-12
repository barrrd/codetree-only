from collections import deque
def dist(r1,c1, r2, c2):
    return (r1- r2)**2 + (c1 - c2)**2

def step1():
    global  start_r, start_c

    # 1. find the target santa
    cand = []
    best = float("inf")

    for id in sorted(santa.keys()):
        if santa[id]["alive"] :
            pr, pc = santa[id]["pos"]

            cur_dist = dist(pr,pc,start_r, start_c)

            if cur_dist < best:
                cand = [(id,pr,pc)]
                best = cur_dist
            elif cur_dist == best:
                cand.append((id,pr,pc))

    cand.sort(key = lambda  x: (-x[1], -x[2]))

    target = cand[0]
    tid, tr, tc = target

    # 2. move deaf
    move_r = 0
    move_c = 0

    if tr > start_r:
        move_r = 1
    elif tr < start_r:
        move_r = -1

    if tc > start_c:
        move_c = 1
    elif tc < start_c:
        move_c = -1

    start_r += move_r
    start_c += move_c

    if (tr, tc) == (start_r, start_c):
        return tid, move_r, move_c

    return None, move_r, move_c

def step2(turn):
    global start_r, start_c
    for id in sorted(santa.keys()):
        if santa[id]["alive"] and santa[id]["stun"] < turn:
            sr, sc = santa[id]["pos"]
            best_dist= dist(start_r, start_c, sr, sc)
            best_r = sr
            best_c = sc
            best_dr = 0
            best_dc = 0
            is_moved = False

            # santa: 상 우 하 좌
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = sr + dr, sc + dc

                if 0 <= nr < n and 0 <= nc <n:
                    if arr[nr][nc] == 0:
                        nxt_dist = dist(nr,nc, start_r, start_c)
                        if nxt_dist < best_dist:
                            is_moved = True
                            best_dist = nxt_dist

                            best_r, best_c = nr, nc
                            best_dr, best_dc = dr, dc

            if is_moved:
                sr, sc = santa[id]["pos"]
                arr[sr][sc] = 0
                santa[id]["pos"] = [best_r, best_c]
                arr[best_r][best_c] = id

                if (best_r, best_c) == (start_r, start_c):
                    move_r, move_c = -best_dr, -best_dc
                    power = D
                    collision_handle(id, move_r, move_c, power, turn)






def interaction(collision_id, move_r, move_c, power):
    global alive_count, santa, arr
    # 1. 충돌 판단
    count = 0
    q = deque([collision_id])
    moved = []

    while q:
        count += 1
        id = q.popleft()
        sr, sc = santa[id]["pos"]
        if count != 1:
            power = 1

        nr, nc = sr + move_r * power, sc + move_c * power

        # case1. 밖으로 나간 경우
        if not(0 <= nr < n and 0 <= nc <n):
            alive_count -= 1
            arr[sr][sc] = 0
            santa[id]["alive"] = False
            continue

        # case2. 안인 경우
        ## case2.1 이동 후에 거기에 다른 산타가 있을 경우
        if arr[nr][nc] != 0:
            moved.append((id,nr,nc))
            nxt_id = arr[nr][nc]
            q.append(nxt_id)

        ## cas2.2 아무도 없는 경우
        else:
            arr[sr][sc] = 0
            arr[nr][nc] = id
            santa[id]["pos"] = [nr,nc]

    # 2. case2.1 처리
    while moved:
        id, nr, nc = moved.pop()
        sr, sc = santa[id]["pos"]

        arr[sr][sc] = 0
        arr[nr][nc] = id

        santa[id]["pos"] = [nr,nc]


def collision_handle(collision_id, move_r, move_c, power, turn):
    global answer
    # 1. update a answer
    answer[collision_id] += power

    # 2.stun
    santa[collision_id]["stun"] = turn + 1

    # 3. interaction
    interaction(collision_id, move_r, move_c, power)


# 1.init
T = 1
for ts in range(1, T + 1):
    n, m, p, C, D = map(int,input().split())
    start_r, start_c = map(int,input().split())
    start_r, start_c  = start_r - 1, start_c - 1
    arr = [[0] * n for _ in range(n)]

    santa = {}
    for _ in range(p):
        id, r, c = map(int,input().split())

        r, c = r - 1, c - 1
        santa[id] = {
            "pos": [r, c],
            "stun": 0,
            "alive": True
        }
        arr[r][c] = id

    # 2. execute
    answer = { id: 0 for id in range(1, p + 1)}
    alive_count = p
    for turn in range(1, m + 1):
        # step0. all dead
        if alive_count == 0:
            break

        # step1. move a deaf
        collision_id, move_r, move_c =  step1()

        if collision_id:
            collision_handle(collision_id, move_r, move_c, C, turn)

        # step2. move a santa
        step2(turn)

        # update a answer
        for id in santa.keys():
            if santa[id]["alive"]:
                answer[id] += 1

    ## final
    final = []
    for id in sorted(santa):
            final.append(answer[id])
    print(*final)