from collections import deque
def check_deaf(lst, d, dr, dc, mul):
    global santa_location, arr
    q = deque([(lst)])
    to_update = []
    first = True

    while q:
        num = q.popleft()
        r, c, k = santa_location[num] 
        if first:
            nr, nc = r + mul*dr[d], c + mul*dc[d]
            first = False
        else:
            nr, nc = r + dr[d], c + dc[d]

        # 2.
        if not(0 <= nr < n and 0 <= nc < n):
            to_update.append((num,nr,nc))
            continue
        to_update.append((num,nr,nc)) 
        if arr[nr][nc] == 0:
            pass
        else:
            target_idx = arr[nr][nc]
            if target_idx != num:
                q.append((target_idx))
    # 3. update
    ## 1. 초기화
    for s_idx, _, _ in to_update:
        sr, sc, _ = santa_location[s_idx]
        if 0 <= sr < n and 0 <= sc < n:
            arr[sr][sc] = 0
    ## 2. update
    for s_idx, snr, snc in to_update:
        santa_location[s_idx][0] = snr
        santa_location[s_idx][1] = snc
        if 0 <= snr < n and 0 <= snc < n:
            arr[snr][snc] = s_idx
        else:
            survied[s_idx] = False

    

##############################################
# 1.init
n, m, p, C, D = map(int,input().split())
arr = [[0]*n for _ in range(n)]
deaf = list(map(int,input().split()))
deaf = [deaf[0]-1, deaf[1] - 1]
# arr[deaf[0]][deaf[1]] = -1
santa_location = {}
survied = [True]*(p+1)
stunned = [-1]*(p+1)
for _ in range(p):
    i, r, c = map(int,input().split())
    arr[r-1][c-1] = i
    santa_location[i] = [r-1,c-1,0]
# left

fdr = [0, -1, -1, -1, 0, 1, 1, 1]
fdc = [-1, -1, 0, 1, 1, 1, 0, -1]
# 상우화좌
sdr = [-1, 0, 1, 0]
sdc = [0, 1, 0, -1]
# 2. execute
for turn in range(1, m+1):
    # print(f"turn:{turn}")
    santa_loc = {}
    for i in range(1,p+1):
        r, c, k = santa_location[i]
        if survied[i]:
            santa_loc[i] = [r,c,k]
    if len(santa_loc) == 0:
        break
    ###################################
    # step1. move a deaf
    ###################################
    ## 1. choose a sp santa
    candidates = []
    best_min = float("inf")
    for s in santa_loc:
        cr, cc, _ = santa_loc[s]
        dist = (deaf[0]-cr)**2  + (deaf[1]-cc)**2
        if best_min > dist:
            best_min = dist
            candidates = [(cr,cc,s)]
        elif best_min == dist:
            candidates.append((cr,cc,s))
    choosen_santa = sorted(candidates, key = lambda x: (-(x[0]), -(x[1])))[0]
    
    ## 2. move a deaf
    best_min = float("inf")
    r1, c1 = -1, -1
    cr, cc, _ = choosen_santa
    nd = -1
    for i in range(8):
        nr, nc = deaf[0] + fdr[i], deaf[1] + fdc[i]
        if not(0 <= nr < n and 0 <= nc < n): continue
        dist = (cr-nr)**2  + (cc-nc)**2
        if best_min > dist:
            best_min = dist
            r1, c1 = nr, nc
            nd = i
    deaf = [r1,c1]
    ###################################
    # step3. santa move and collsion
    ###################################
    # 1. check from deaf 
    if arr[deaf[0]][deaf[1]] != 0:
        sid = arr[deaf[0]][deaf[1]]
        santa_location[sid][2] += C
        stunned[sid] = turn + 1
        arr[deaf[0]][deaf[1]] = 0
        check_deaf(sid, nd, fdr, fdc, C)

    # 2. santa: check and move
    for i in range(1,p+1):
        if not survied[i] or stunned[i] >= turn:
            continue
        ## 1. 이동 가능한지
        r, c, k = santa_location[i]
        best_min = (deaf[0]-r)**2  + (deaf[1]-c)**2
        nxt_d = -1
        for idd in range(4):
            nr, nc = r + sdr[idd], c + sdc[idd]
            dist = (deaf[0]-nr)**2  + (deaf[1]-nc)**2 
            if not(0 <= nr < n and 0 <= nc < n): continue
            if arr[nr][nc] != 0 and arr[nr][nc] != i: continue 
            if best_min > dist:
                best_min = dist
                nxt_d = idd

        if nxt_d != -1:
            nr, nc = r + sdr[nxt_d], c + sdc[nxt_d]
            arr[r][c] = 0
            if (nr,nc) == (deaf[0],deaf[1]):
                santa_location[i][2] += D
                stunned[i] = turn + 1
                santa_location[i][0], santa_location[i][1] = nr, nc
                check_deaf(i, (nxt_d+ 2) % 4, sdr, sdc, D)
            ## 2. 이동 가능하면 from_deaf에 넣어서 move  
            else:
                # santa_location[key][2] += d
                arr[nr][nc] = i
                santa_location[i][0], santa_location[i][1] = nr, nc

    ###################################
    # step4. update
    ###################################
    array = [[0]*n for _ in range(n)]
    for i in range(1,p+1):
        r, c, _ = santa_location[i]
        
        if survied[i]:
            santa_location[i][2] += 1
            array[r][c] = i
    arr = array


ans = [0]*len(santa_location)
for key, value in santa_location.items():
    ans[key-1] = value[2]
print(*ans)
# print(santa_location)
