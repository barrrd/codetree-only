from collections import deque


def step1(turn):
    global ppos, block
    block_candidates = []

    for pid in range(1, turn):
        if pid in ppos:  # 도착하지 않은 player만
            ### 1. make a sp
            sr, sc, tr, tc = ppos[pid]
            if sr == -1: continue

            v = [[-1] * n for _ in range(n)]
            v[tr][tc] = 0
            q = deque([(tr, tc)])
            while q:
                cr, cc = q.popleft()
                for i in range(4):
                    nr, nc = cr + dr[i], cc + dc[i]
                    # 1. 벽 밖
                    if not (0 <= nr < n and 0 <= nc < n) or block[nr][nc] or v[nr][nc] != -1:
                        continue
                    # 2. 일반적인 경우
                    v[nr][nc] = v[cr][cc] + 1
                    q.append((nr, nc))
            ### 2.
            min_dist = float('inf')
            nxt_r, nxt_c = -1, -1
            for i in range(4):
                nr, nc = sr + dr[i], sc + dc[i]
                if not (0 <= nr < n and 0 <= nc < n) or block[nr][nc] or v[nr][nc] == -1:
                    continue
                if v[nr][nc] < min_dist:
                    min_dist = v[nr][nc]
                    nxt_r, nxt_c = nr, nc
            ### 3.
            ppos[pid][0], ppos[pid][1] = nxt_r, nxt_c
            if (nxt_r, nxt_c) == (tr, tc):
                block_candidates.append((pid, tr, tc))
    ### 4. block 처리
    for bid, br, bc in block_candidates:
        block[br][bc] = True
        del ppos[bid]


def step2(turn):
    global ppos, block
    # 1. make a parent
    tr, tc, sr, sc = ppos[turn]
    visited = [[-1] * n for _ in range(n)]
    visited[sr][sc] = 0
    q = deque([(sr, sc)])
    candidates = []
    while q:
        cr, cc = q.popleft()
        # 1. 베이스 캠프 도착
        if arr[cr][cc] == 1:
            candidates.append((visited[cr][cc], cr, cc))
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]
            # 2. 격자 밖과 block
            if not (0 <= nr < n and 0 <= nc < n) or block[nr][nc] or visited[nr][nc] != -1:
                continue
            # 3. 일반적인 경우 None 일 때,
            visited[nr][nc] = visited[cr][cc] + 1
            q.append((nr, nc))
    # 2.
    candidates.sort(key=lambda x: (x[0], x[1], x[2]))
    tr, tc = candidates[0][1:]
    ppos[turn] = [tr, tc, sr, sc]
    block[tr][tc] = True


# 1.init
T = int(input())
# 상 좌 우 하
dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]
for ts in range(1, T + 1):
    n, m = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(n)]  # 1.
    ppos = {}  # 2.
    for i in range(1, m + 1):
        start_r, start_c = map(int, input().split())
        start_r, start_c = start_r - 1, start_c - 1
        ppos[i] = [-1, -1, start_r, start_c]
    block = [[False] * n for _ in range(n)]  # 3.

    turn = 0
    while ppos:
        turn += 1
        #####################################
        # step1. m < turn인 player 이동
        #####################################
        step1(turn)
        #####################################
        # step2. m == turn인 player basecamp 이동
        #####################################
        if turn <= m:
            step2(turn)

    print(turn)




