# 1. init
n, m = map(int,input().split())
tree = [list(map(int,input().split())) for _ in range(n)]
nutr = [(n-1,0),(n-2,0), (n-1,1),(n-2,1)]
dr = [0, -1, -1, -1, 0, 1, 1, 1]
dc = [1, 1, 0, -1, -1, -1, 0, 1]
dirr = [-1, -1, 1, 1]
dirc = [-1, 1, 1, -1]
# 2. execute
for _ in range(m):
    number, mul = map(int,input().split())
    d = number - 1
###########################
# step1. nutr move
###########################
    nxt_nutr = []
    for cr, cc in nutr:
        nr, nc = (cr + mul*dr[d])%n, (cc + mul*dc[d])%n
        nxt_nutr.append((nr, nc))
    # print(nxt_nutr)
    # [(4, 3), (3, 3), (4, 4), (3, 4)]
###########################
# step2. tree update
###########################
    for cr, cc in  nxt_nutr:
        tree[cr][cc] += 1

###########################
# step2~3. tree update
###########################
    for cr, cc in  nxt_nutr:
        cnt = 0
        for idx in range(4):
            nr, nc = cr + dirr[idx], cc + dirc[idx]
            if 0 <= nr < n and 0 <= nc < n:
                if tree[nr][nc] >= 1:
                    cnt += 1
        tree[cr][cc] += cnt
    # print(tree)
    # [[1, 0, 0, 4, 2], [2, 1, 3, 2, 1], [0, 0, 0, 2, 5], [1, 0, 0, 4, 6], [1, 2, 1, 5, 5]]
###########################
# step4.
###########################
    tnt = []
    for r in range(n):
        for c in range(n):
            if (r,c) not in nxt_nutr and tree[r][c] >= 2:
                tnt.append((r,c))
                tree[r][c] -= 2
    nutr = tnt
    # print(tnt)
    # [(0, 3), (0, 4), (1, 0), (1, 2), (1, 3), (2, 3), (2, 4), (4, 1)]
# 3. check the tree heihgt
answer = 0
for t in tree:
    answer += sum(t)
print(answer)
