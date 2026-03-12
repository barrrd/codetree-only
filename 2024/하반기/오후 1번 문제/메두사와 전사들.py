from collections import deque
def snake_bfs(sr, sc, er, ec):
    v = [[False]* n for _ in range(n)]
    q = deque([(sr,sc,[])])
    v[sr][sc] = True
    paths = None
    while q:
        ccr, ccc, path = q.popleft()
        if (ccr, ccc) == (er,ec):
            paths = path
            return deque(paths)
        for i in range(4):
            nr, nc = ccr + dr[i], ccc + dc[i]
            if not(0 <= nr < n and 0 <= nc < n) or v[nr][nc]: continue
            if arr[nr][nc] == 0:
                v[nr][nc] = True
                new_path = path + [(nr, nc)]
                q.append((nr,nc,new_path))
    return None

def make_stone(sr,sc):
    best = -1
    best_dist = None
    best_dir = -1
    for i in range(4):
        dist, number = blind(sr,sc,i)
        if best < number:
            best = number
            best_dist = dist
            best_dir = i

    return best_dist, best

def blind(mr, mc, d):
    view_map = [[False] * n for _ in range(n)]
    targets = []
    
    for r in range(n):
        for c in range(n):
            is_in = False
            if d == 0: # 상
                if r < mr and abs(c - mc) <= abs(r - mr): is_in = True
            elif d == 1: # 하
                if r > mr and abs(c - mc) <= abs(r - mr): is_in = True
            elif d == 2: # 좌
                if c < mc and abs(r - mr) <= abs(c - mc): is_in = True
            elif d == 3: # 우
                if c > mc and abs(r - mr) <= abs(c - mc): is_in = True
            
            if is_in:
                view_map[r][c] = True
                if warr[r][c] > 0:
                    targets.append((r, c, abs(r - mr) + abs(c - mc)))

    targets.sort(key=lambda x: x[2])
    stoned_count = 0

    for tr, tc, _ in targets:
        if not view_map[tr][tc]: continue
        stoned_count += warr[tr][tc]

        if d == 0: # 상
            rc = tc - mc
            for r in range(tr - 1 , -1, -1):
                if rc != 0:
                    for c in range(n):
                        if rc > 0:
                                if c - tc >= 0 and c - tc <= tr - r:
                                    view_map[r][c] = False
                        elif rc < 0:
                                if c - tc <= 0 and -(c - tc) <= tr - r:
                                    view_map[r][c] = False
                else:
                    view_map[r][tc] = False


        elif d == 1: # 하
            rc = tc - mc
            for r in range(tr + 1 , n):
                if rc != 0:
                    for c in range(n):
                        if rc > 0:
                                if c - tc >= 0 and c - tc <= r - tr:
                                    view_map[r][c] = False
                        else:
                                if c - tc <= 0 and -(c - tc) <= r - tr:
                                            view_map[r][c] = False
                else:
                    view_map[r][tc] = False
        elif d == 2: # 좌
            rr = tr - mr
            for c in range(tc -1 , -1, -1):
                if rr != 0:
                    for r in range(n):
                        if rr > 0:
                                if r - tr >= 0 and r - tr <= abs(c - tc):
                                    view_map[r][c] = False
                        else:
                                if r - tr <= 0 and -(r - tr) <= abs(c - tc):
                                    view_map[r][c] = False
                else:
                    view_map[tr][c] =  False

        elif d == 3: # 우
            rr = tr - mr
            for c in range(tc + 1 , n):
                if rr != 0:
                    for r in range(n):
                        if rr > 0:
                                if r - tr >= 0 and r - tr <= abs(c - tc):
                                    view_map[r][c] = False
                        else:
                                if r - tr <= 0 and -(r - tr) <= abs(c - tc):
                                    view_map[r][c] = False
                else:
                    view_map[tr][c] =  False
    return view_map, stoned_count


def warrior_move(blind_dist, cr, cc):
    global warr, ans0, ans2
    nxt_lst = []
    nxt_warr = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            number = warr[r][c]
            if number > 0:
                if blind_dist[r][c]:
                    nxt_warr[r][c] += warr[r][c]
                    continue
                nxtr, nxtc = r, c
                total_move = 0
                loop1 = False
                
                for mul in range(2):
                    moved = False
                    if mul == 0:
                        dir_order = [0, 1, 2, 3] # 상, 하, 좌, 우
                    else:
                        dir_order = [2, 3, 0, 1] # 좌, 우, 상, 하

                    for i in dir_order:
                        nr, nc = nxtr + dr[i], nxtc + dc[i]
                        if not(0 <= nr < n and 0 <= nc < n) or blind_dist[nr][nc]: continue
                        curr_dist = abs(cr - nxtr) + abs(cc - nxtc)
                        nxt_dist = abs(nr - cr) + abs(nc - cc)
                        if nxt_dist < curr_dist:
                            curr_dist = nxt_dist
                            nxtr, nxtc = nr, nc
                            total_move += 1
                            moved = True
                            if (nr,nc) == (cr, cc):
                                ans2 += warr[r][c]
                                loop1 = True
                                break
                            break
                    if not moved or loop1:
                        break
                ans0 += total_move * warr[r][c]
                if not loop1:
                    nxt_warr[nxtr][nxtc] += warr[r][c]
                    
                    # print(f"({r},{c}) 전사 이동 완료: ({nxtr},{nxtc}), 이동거리: {total_move}")
    warr = nxt_warr





# 1. init
# 상 하 좌 우
dr = [-1, 1, 0, 0]
dc = [0 , 0, -1, 1]
n, m  = map(int, input().split())
sr, sc, er, ec = map(int, input().split())
w_input = list(map(int, input().split()))
warriors = []
for i in range(m):
    warriors.append((w_input[2*i], w_input[2*i + 1]))
arr = [list(map(int, input().split())) for _ in range(n)] 
warr = [[0] * n for _ in range(n)]
for wr, wc in warriors:
    warr[wr][wc] += 1
## 1. 메두사 경로
snake_path = snake_bfs(sr, sc, er, ec)

cnt = 1
if snake_path is None:
    print(-1)
else:
    # 2. execute
    while True:
        #####################################
        # step1. snake move
        #####################################
        ans0 , ans1, ans2 = 0, 0, 0 # 전사 이동 거리합, 메두사로 돌 수, 메두사를 공격한 전사
        # 1. 끝
        cr, cc = snake_path.popleft()
        if (cr, cc) == (er, ec):
            print(0)
            break
        # 2. kill the warriors
        warr[cr][cc] = 0
        #####################################
        # step2. make a stone
        #####################################
        blind_dist, tmp1 = make_stone(cr,cc)
        ans1 = tmp1
        #####################################
        # step3~4. warrior move
        #####################################

        warrior_move(blind_dist,cr,cc)


        print(f"{ans0} {ans1} {ans2}")
        
        # if cnt == 1:
        #     for row in blind_dist:
        #         print(row)
        #     break
