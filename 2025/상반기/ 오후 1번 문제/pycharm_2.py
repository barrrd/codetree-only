from collections import deque
def count_square(cand):
    # 1. 시작 위치 찾기
    sr,sc = 0, 0
    is_found = False
    for r in range(N):
        for c in range(N):
            if arr[r][c] == cand:
                sr,sc = r, c
                is_found = True
                break
        if is_found:
            break
    # 2. count
    q = deque([(sr,sc)])
    v = [[False]*N for _ in range(N)]
    v[sr][sc] = True
    count = 1

    while q:
        cr, cc = q.popleft()
        for (dr, dc) in [(1,0), (-1,0), (0, 1), (0, -1)]:
            nr, nc = cr + dr, cc + dc
            if not(0 <= nr < N and 0 <= nc < N):
                continue
            if v[nr][nc] or arr[nr][nc] != cand:
                continue

            v[nr][nc] = True
            count += 1
            q.append((nr,nc))

    return count

def remove(cand, square):
    count = 0
    for r in range(N):
        for c in range(N):
            if arr[r][c] == cand:
                arr[r][c] = 0
                count += 1

            if count == square:
                break
        if count == square:
            break

def more_two(candidates):
    global arr
    # 1. 2개로 나눈지
    for cand in candidates:
        count = 0
        for r in range(N):
            for c in range(N):
                if arr[r][c] == cand:
                    count += 1
        # 2.
        ## 두개 이상
        if count_square(cand) < count:
            remove(cand, count)



def step1(sr, sc, er, ec, turn):
    global arr
    # 1. 투입
    candidates = set()
    for r in range(sr, er):
        for c in range(sc, ec):
            if arr[r][c] != 0:
                candidates.add(arr[r][c])
            arr[r][c] = turn

    # 2. more_two
    if candidates:
        more_two(candidates)

def step2():
    global arr
    cand = []
    dct = {}
    new_arr = [[0] * N for _ in range(N)]
    # 1. 각 미생물 저장
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                continue

            dct.setdefault(arr[r][c],{
                "square": 0,
                "lst": [],
            })

            dct[arr[r][c]]["square"] += 1
            dct[arr[r][c]]["lst"].append((r,c))

    # 2. 이동 순서 정렬
    cand = list(dct.keys())
    cand.sort(key = lambda x: (-dct[x]["square"], x))

    # 3. 배치
    for can in cand:
        lst = dct[can]["lst"]

        min_r = min(r for r, c in lst)
        min_c = min(c for r, c in lst)

        shape = []
        for r, c in lst:
            shape.append((r - min_r, c - min_c))

        sr, sc = -1, -1

        for r in range(N):
            for c in range(N):
                possible = True

                for dr, dc in shape:
                    nr, nc = r + dr, c + dc

                    if not(0 <= nr < N and 0 <= nc < N):
                        possible = False
                        break
                    if new_arr[nr][nc] != 0:
                        possible = False
                        break

                if possible:
                    sr, sc = r, c
                    break

            if possible:
                break

        # 2. update
        if (sr,sc) == (-1, -1):
            continue

        for dr, dc in shape:
            nr, nc = sr + dr, sc + dc
            new_arr[nr][nc] = can

    arr = new_arr

def step3():
    # 1. pairs
    pairs = set()
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                 continue

            cur = arr[r][c]

            for dr, dc in [(1,0), (0,1)]:
                nr, nc = r + dr, c + dc

                if not(0 <= nr < N and 0 <= nc < N):
                    continue

                nxt = arr[nr][nc]

                if cur == nxt or nxt == 0:
                    continue

                a, b = sorted((cur, nxt))
                pairs.add((a, b))

    # 2. answer
    answer = 0
    for pair in pairs:
        tmp = 1
        for p in pair:
            tmp *= count_square(p)
        answer += tmp

    return answer


# 1. init
T = 1
for ts in range(1, T + 1):
    N, Q = map(int,input().split())
    arr = [[0]*N for _ in range(N)]
    # 2. execute
    for turn in range(1, Q + 1):
        sr, sc, er, ec = map(int,input().split())

        # step1. 미생물 투입
        step1(sr,sc,er,ec,turn)

        # step2. 배양 용기 이동
        step2()

        # step3. 실험 결과 기록
        answer = step3()

        print(answer)

