from collections import deque
def step1(order, number):
    global arr, order_dct
    # 0. 기존 미생물 침투 여부
    checks = set()
    # 1. 미새물 투입
    r1, c1, r2, c2 = order
    order_dct[number] = [r1, c1, r2, c2]
    for r in range(r1,r2):
        for c in range(c1, c2):
            if arr[r][c] != 0 and arr[r][c] != number:
                checks.add(arr[r][c])
            arr[r][c] = number
    # 2. 2개 이상
    v = [[False]*n  for _ in range(n)]
    for check in checks:
        cr1, cc1, cr2, cc2 = order_dct[check]
        divide_num = 0
        for r in range(cr1, cr2):
            for c in range(cc1, cc2):
                if v[r][c] or arr[r][c] != check: continue
                divide_num += 1
                v[r][c] = True
                q = deque([(r,c)])
                while q:
                    cr, cc = q.popleft()
                    for i in range(4):
                        nr, nc = cr + dr[i], cc + dc[i]
                        if not(0<= nr < n and 0 <= nc < n) or v[nr][nc]: continue
                        if arr[nr][nc] == check:
                            v[nr][nc] = True
                            q.append((nr,nc))
        # 3. 2개 이상 시, 제거
        if divide_num >= 2:
            del order_dct[check]
            for mr in range(cr1, cr2):
                for mc in range(cc1, cc2):
                    if arr[mr][mc] == check:
                        arr[mr][mc] = 0

def step2():
    global arr, order_dct 
    # 1. 모드 용기에 대한 순서
    candidates = []
    for k, v in order_dct.items():
        r1, c1, r2, c2 = v
        
        min_r, max_r = n, -1
        min_c, max_c = n, -1
        total = 0
        
        for r in range(r1, r2):
            for c in range(c1, c2):
                if arr[r][c] == k:
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
                    total += 1
                    
        if total == 0:
            continue 
            
        t_rlen = max_r - min_r + 1
        t_clen = max_c - min_c + 1
        shape = [[False] * t_clen for _ in range(t_rlen)]
        
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if arr[r][c] == k:
                    shape[r - min_r][c - min_c] = True 
                    
        candidates.append((total, k, shape))
        
    order = sorted(candidates, key = lambda x: (-x[0], x[1]))
    # 2. update
    new_arr = [[0]*n for _ in range(n)]
    new_order_dct = {}
    for o in order:
        _, number, shape = o
        rlen, clen = len(shape), len(shape[0])
        r1, c1, r2, c2 = order_dct[number]
        
        for r in range(n - rlen + 1):
            for c in range(n - clen + 1):
                possible = True
                for nr in range(rlen):
                    for nc in range(clen):
                        if shape[nr][nc] == True and new_arr[r + nr][c + nc] != 0:
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    break
            if possible:
                break
        if possible:
            for rr in range(r, r + rlen):
                for rc in range(c, c + clen):
                    if shape[rr - r][rc- c]:
                        new_arr[rr][rc] = number
            new_order_dct[number] = [r, c, r + rlen, c + clen]
    
    arr = new_arr
    order_dct = new_order_dct
                            
def step3():
    global arr, order_dct
    # 1. 인접한 도형
    max_id = max(order_dct.keys())
    adj = [[0]*(max_id+ 1) for _ in range(max_id+ 1)]
    square = [0]*(max_id+ 1)
    
    for key, value in order_dct.items():
        r1, c1, r2, c2 = value
        v = [[False]*n for _ in range(n)]
        start_r, start_c = -1, -1
        for r in range(r1, r2):
            for c in range(c1, c2):
                if arr[r][c] == key:
                    start_r, start_c = r, c
                    square[key] += 1
        ## 2. 인접한 곳 리스트로         
        for r in range(r1, r2):
            for c in range(c1, c2):
                if arr[r][c] == key and not v[r][c]:
                    v[r][c] = True
                    q = deque([(r,c)])
                    while q:
                        cr, cc = q.popleft()
                        for i in range(4):
                            nr, nc = cr + dr[i], cc + dc[i]
                            if not(0 <= nr  < n and 0 <= nc < n) or v[nr][nc]: continue
                            if arr[nr][nc] !=0:
                                if key != arr[nr][nc]:
                                    adj[key][arr[nr][nc]] = 1
                                    adj[arr[nr][nc]][key] = 1
                                else:
                                    q.append((nr,nc))
                                    v[nr][nc] = True
    ## 3. answer
    ans3 = [[False]*(max_id+ 1) for _ in range(max_id+ 1)]
    answer = 0
    for r in range(max_id+ 1):
        axis = square[r]
        for c in range(max_id+ 1):
            if adj[r][c] == 0: continue
            tmp = 0
            if adj[r][c] == 1 and not ans3[r][c]:
                ans3[r][c] = True
                ans3[c][r] = True
                tmp += square[c]
            answer += axis * tmp

    # print(adj)
    # print(square)
    print(answer)
                        

# 1. init
n, q = map(int,input().split())
orders = [list(map(int,input().split())) for _ in range(q)]
arr = [[0]*n  for _ in range(n)]
order_dct = {}
# 상 하 좌 우
dr = [-1, 1, 0, 0] 
dc = [0, 0, -1, 1]
# 2. execute
for turn in range(q):
    ####################################
    # step1. 미생물 투입
    ####################################

    step1(orders[turn], turn + 1)
    # # if turn >= 2:
    # for row in arr:
    #     print(row)
    # print()

    ####################################
    # step2. 배양용기 이동
    ####################################
    step2()
    # if turn >= 2:
    # for row in arr:
    #     print(row)
    # print()
    # print(order_dct)

    ####################################
    # step3. 배양용기 이동
    ####################################
    step3()
    # if turn == 2:
    #     break
