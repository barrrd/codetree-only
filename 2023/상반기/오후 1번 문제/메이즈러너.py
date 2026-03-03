"""
step2. rotate arr
> make a 출구 and candidates
> 두 개 이상시, low r > low c
    cw and 내구도 -= 1

"""
def cw(arr,sr,sc,length):
    # 1. copy
    tmp = [row[:]for row in arr]
    # 2.
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):
            if 1 <= arr[r][c] <= 9:
                arr[r][c] -= 1
            ## 1. (0,0) 기준으로 move
            orr, occ = r - sr, c - sc
            ## 2. cw 의 좌표
            rr, rc = occ, length - 1 - orr
            ## 3.다시 원래 위치로
            tmp[sr+rr][sc+rc] = arr[r][c]
    # 3.회전된 부분만 원본에 반영
    for r in range(sr, sr + length):
        for c in range(sc, sc + length):

            arr[r][c] = tmp[r][c]

def rot_point_cw(sr, sc, length, r, c):
    orr, occ = r - sr, c - sc
    rr, rc = occ, length - 1 - orr
    return sr + rr, sc + rc   

# 1. init
n, m, k = map(int,input().split())
arr = [list(map(int,input().split())) for _ in range(n)]
players = []
for _ in range(m):
    r, c = map(int,input().split())
    players.append([r - 1,c - 1])
tr, tc = map(int,input().split())
tr -= 1
tc -= 1
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
answer = 0
# 2.execute
for time in range(k):
    ###################################
    # step1. move a players
    ###################################
    nxt = []
    for sr, sc in players:
        dist = abs(sr-tr) + abs(sc - tc)
        moved = False
        for i in range(4):
            nr, nc = sr + dr[i], sc + dc[i]
            if not (0 <= nr < n  and 0 <= nc < n) : continue
            if arr[nr][nc] == 0:
                if  abs(nr- tr) + abs(nc - tc) < dist:
                    nxt.append([nr,nc])
                    moved = True
                    answer += 1
                    break
        if not moved:
            nxt.append([sr,sc])
    # print(players)
    # print(nxt)
    players = []
    for nr, nc in nxt:
        if (nr,nc) == (tr, tc):
            continue
        players.append([nr,nc])
    if len(players) == 0:
        break
    # print(players)
    ###################################
    # step2. rotate a square
    ###################################
    # 1. make a square
    square = []
    found = False
    for length in range(2,n+1):
        for row in range(n - length + 1):
            for col in range(n - length + 1):
                row_end, col_end = row + length - 1, col + length - 1
                if row_end >= n or col_end >= n: continue
                if not (row <= tr <= row_end and col <= tc <= col_end): continue
                if any( row <= pr <= row_end and col <= pc <= col_end for pr, pc in players):
                    square = [row, col, length]
                    found = True
                    break
            if found:
                break
        if found:
            break
    # print(square)
    # [0, 0, 3, 3]
    # 2. rotate a square
    cw(arr,*square)
    # 3. sr,sc, tr, tc rotate
    row, col, length = square
    # 1) tr, tc 
    tr, tc = rot_point_cw(row, col, length, tr, tc)
    # 2) player
    new_players = []
    # print(players)
    for pr, pc in nxt:
        if row <= pr < row + length and col <= pc < col + length:
            pr, pc = rot_point_cw(row, col, length, pr, pc)
        new_players.append([pr, pc])

    players = new_players
    # print(players)
    # if time == 0:
    #     break

print(answer)
print(tr+1,tc+1)
