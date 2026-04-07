from collections import deque
def alive_count():
    cnt = 0
    for r in range(n):
        for c in range(m):
            if arr[r][c][0] > 0:
                cnt += 1
    return cnt


def step1():
    # 1. find the attacker
    candidates = []
    best_min = float("inf")
    for r in range(n):
        for c in range(m):
            if arr[r][c][0] == 0:
                continue
            if arr[r][c][0] < best_min:
                best_min = arr[r][c][0]
                candidates = [(arr[r][c][0], arr[r][c][1], r, c)]
            elif arr[r][c][0] == best_min:
                candidates.append((arr[r][c][0], arr[r][c][1], r, c))

    candidates.sort(key = lambda x: (x[0],-x[1], -(x[2]+ x[3]), -x[3]))
    attacker = candidates[0]
    ar, ac = attacker[2], attacker[3]

    # 2. find the target
    target_cand  = []
    best_max = 0
    for r in range(n):
        for c in range(m):
            if arr[r][c][0] == 0 or (ar, ac) == (r,  c):
                continue
            if arr[r][c][0] > best_max:
                best_max = arr[r][c][0]
                target_cand = [(arr[r][c][0], arr[r][c][1], r, c)]
            elif arr[r][c][0] == best_max:
                target_cand.append((arr[r][c][0], arr[r][c][1], r, c))

    target_cand.sort(key = lambda x: (-x[0], x[1], (x[2]+ x[3]), x[3]))
    target = target_cand[0]

    return attacker, target

def step2(attacker, target):
    global arr
    # 1. update  attacker's damage and turn
    damage, _, ar, ac = attacker
    damage += n + m
    arr[ar][ac] = [damage, turn]

    _, _, tr, tc = target

    # 2. razor or turret
    except_lst = [(ar,ac), (tr,tc)]
    # 우 하 좌 상
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]

    is_razor = False
    parent = [[None]*m for _ in range(n)]
    parent[ar][ac] = [ar,ac]
    q = deque([(ar,ac)])
    while q:
        cr, cc = q.popleft()
        if (cr,cc) == (tr, tc):
            is_razor = True
            break
        for i in range(4):
            nr = (cr + dr[i]) % n
            nc = (cc + dc[i]) % m

            if parent[nr][nc] or arr[nr][nc][0] == 0:
                continue
            q.append((nr,nc))
            parent[nr][nc] = [cr, cc]

    arr[tr][tc][0] = max(arr[tr][tc][0] - damage, 0)
    if is_razor:
        path = []
        cr, cc = tr, tc
        while True:
            pr, pc = parent[cr][cc]
            if (pr,pc) == (ar,ac):
                break
            path.append((pr,pc))
            cr, cc = pr, pc
            except_lst.append((cr, cc))

        # attack
        for pr, pc in path:
            arr[pr][pc][0] = max(arr[pr][pc][0] - damage//2, 0)

    # 3. turret
    else:
        for dr, dc in [(-1, 0),(1, 0),(0, -1),(0, 1),(-1, -1),(-1, 1),(1, -1),(1, 1)]:
            nr, nc = (tr + dr) % n, (tc + dc) % m
            if (nr, nc) == (ar, ac) or arr[nr][nc][0] == 0:
                continue
            except_lst.append((nr, nc))
            arr[nr][nc][0] = max(arr[nr][nc][0] - damage//2, 0)

    # 4. update a
    for r in range(n):
        for c in range(m):
            if (r,c) in except_lst or arr[r][c][0] == 0:
                continue
            arr[r][c][0] += 1

# 1. init
T = int(input())
for ts in range(1, T+ 1):
    n, m, k = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(n)]
    for r in range(n):
        for c in range(m):
            arr[r][c] = [arr[r][c], 0]
    # for row in arr:
    #     print(row)
    # 2. execute
    for turn in range(1, k + 1):
        if alive_count() <= 1:
            break
        # step1. find the attacker and attacked
        attacker, target = step1()
        # step2. attack
        step2(attacker, target)

    answer = 0
    for r in range(n):
        for c in range(m):
            if arr[r][c][0] > answer:
                answer = arr[r][c][0]
    print(answer)
