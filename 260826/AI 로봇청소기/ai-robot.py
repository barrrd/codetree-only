from collections import deque
def in_range(r,c):
    return 0 <= r < N and 0 <= c < N

def step1():
    global rarr, rdct
    # 1. cand
    for id in sorted(rdct):
        r, c = rdct[id]

        if arr[r][c] > 0:
            continue
            
        v = [[False]*N for _ in range(N)]
        v[r][c] = True
        best = N*N

        cand = []

        q = deque([(r,c, 0)])
        while q:
            sr, sc, sdist = q.popleft()
            sdist += 1
            if sdist > best:
                continue
            for dr, dc in [(0, -1), (-1, 0), (0, 1), (1, 0)]: # 좌, 상, 우, 하
                nr, nc = sr + dr, sc + dc

                if not in_range(nr,nc):
                    continue
                if arr[nr][nc] == -1 or rarr[nr][nc] > 0:
                    continue
                if v[nr][nc]:
                    continue

                # case1. not 먼지
                if arr[nr][nc] == 0:
                    v[nr][nc] = True
                    q.append((nr,nc,sdist))
                # case2. 먼지
                elif arr[nr][nc] > 0:
                    if sdist < best:
                        cand = [(nr, nc)]
                        best = sdist
                    elif sdist == best:
                        cand.append((nr,nc))

        cand.sort(key = lambda x: (x[0], x[1]))

        # 2. update
        if cand:
            tr, tc = cand[0]
            rarr[r][c] = 0
            rarr[tr][tc] = id
            rdct[id] = (tr, tc)

def step2():
    global arr
    drdc = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    for id in rdct:
        r, c = rdct[id]

        center = min(arr[r][c], 20)
        bmax = center
        except_num = 0

        # 1. choose a dir
        for i in range(4):
            tmp = center
            for e, rc in enumerate(drdc):
                if i == e:
                    continue
                dr, dc = drdc[e]
                nr, nc = r + dr, c + dc

                if not in_range(nr, nc):
                    continue
                if arr[nr][nc] == -1:
                    continue

                tmp += min(arr[nr][nc], 20)

            if tmp > bmax:
                bmax = tmp
                except_num = i

        # 2. clean
        if arr[r][c] > 20:
            arr[r][c] -= 20
        else:
            arr[r][c] = 0

        for i in range(4):
            if i == except_num:
                continue
            dr, dc = drdc[i]
            nr, nc = r + dr, c + dc

            if not in_range(nr, nc):
                continue
            if arr[nr][nc] == -1:
                continue

            if arr[nr][nc] > 20:
                arr[nr][nc] -= 20
            else:
                arr[nr][nc] = 0

def step3():
    global arr
    for r in range(N):
        for c in range(N):
            if arr[r][c] > 0:
                arr[r][c] += 5

def step4():
    global arr
    new_arr = [row[:] for row in arr]

    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                tmp = 0
                for dr, dc in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc

                    if not in_range(nr, nc):
                        continue
                    if arr[nr][nc] == - 1:
                        continue

                    tmp += arr[nr][nc]

                tmp = tmp // 10

                new_arr[r][c] += tmp

    arr = new_arr


    # 1. init
T = 1
for ts in range(1, T + 1):
    N, K, L = map(int,input().split())
    # arr = -1: 물건, 0: not 먼지, 1 >= : 먼지
    arr = [list(map(int, input().split())) for _ in range(N)]
    rarr = [[0]*N  for _ in range(N)]
    rdct = {}
    for id in range(1, K + 1):
        r, c = map(int, input().split())
        r, c = r - 1, c - 1
        rarr[r][c] = id
        rdct[id] = (r, c)

    # 2. execute
    for turn in range(1, L + 1):
        # step1. 청소기 이동
        step1()

        # step2. 청소
        step2()

        # step3. 먼지 측척
        step3()

        # step4. 먼지 확산
        step4()

        # 출력
        answer = 0
        for r in range(N):
            for c in range(N):
                if arr[r][c] > 0:
                    answer += arr[r][c]
        print(answer)

