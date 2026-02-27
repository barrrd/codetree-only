# 1. init
n, m, k = map(int,input().split())
gun0 = [list(map(int, input().split())) for _ in range(n)]
gun = [[([] if gun0[i][j] == 0 else [gun0[i][j]]) for j in range(n)] for i in range(n)]
# players = [list(map(int,input().split())) for _ in range(m)]
players = [] # r, c, d, s, g
who = [[-1]*n for _ in range(n)]
for id in range(m):
    r, c, d, s = map(int,input().split())
    r -= 1 
    c -= 1
    who[r][c] = id
    players.append([r,c,d,s,0])
answer = [0]*m
#    up, right, down, left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
# print(gun)
# print(who)
# print(players)
"""
[[[1], [2], [], [1], [2]], [[1], [], [3], [3], [1]], [[1], [3], [], [2], [3]], [[2], [1], [2], [4], [5]], [[], [1], [3], [2], []]]
[[-1, -1, 0, -1, -1], [-1, 1, -1, -1, -1], [-1, -1, 2, -1, -1], [-1, -1, -1, -1, -1], [3, -1, -1, -1, -1]]
[[0, 2, 2, 3, 0], [1, 1, 1, 5, 0], [2, 2, 2, 2, 0], [4, 0, 3, 4, 0]]
"""
# 2. execute
for turn in range(k):
    #################################
    # step1. player move
    #################################
    for id in range(m):
        r, c, d, s, g = players[id]
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < n  and 0 <= nc < n): #
            d = (d + 2) % 4  
            nr, nc = r + dr[d], c + dc[d]
    #################################
    # step2. player or gun
    #################################
        # case1. not player
        if who[nr][nc] == -1:
            who[r][c] = -1
            who[nr][nc] = id
            # case1.1 gun 
            if gun[nr][nc]: 
                gun[nr][nc].append(g)   # # drop the gun
                g = max(gun[nr][nc])    # change the gun
                gun[nr][nc].remove(g)
            players[id] = [nr, nc, d, s, g]
        #case2. player
        else:
            who[r][c] = -1  
            op = who[nr][nc]
            _, _, d2, s2, g2 = players[op]
            p1, p2 = s + g, s2 + g2
            if (p1 > p2) or (p1 == p2 and s > s2):
                winner, loser = id, op
                win_power, lose_power = p1, p2
                players[winner] = [nr, nc, d, s, g]
                gun[nr][nc].append(g2)
                loser_player = [nr, nc, d2, s2]
                winner_player = [nr, nc, d, s, g]
            else:
                winner, loser = op, id
                win_power, lose_power = p2, p1
                gun[nr][nc].append(g)
                loser_player = [nr, nc, d, s]
                winner_player = [nr, nc, d2, s2, g2]

            answer[winner] += (win_power - lose_power)
            who[nr][nc] = winner
            #################################
            # step3. lose
            #################################
            r3, c3, d3, s3 = loser_player
            for i in range(4):
                nd = (d3 + i) % 4
                nr3, nc3 = r3 + dr[nd], c3 +dc[nd]
                if 0 <= nr3 < n and 0 <= nc3 < n and who[nr3][nc3] == -1:
                    who[nr3][nc3] = loser
                    g3 = 0
                    if gun[nr3][nc3]:
                        g3 = max(gun[nr3][nc3])
                        gun[nr3][nc3].remove(g3)
                    players[loser] = [nr3, nc3, nd, s3, g3]
                    break
            #################################
            # step4. winner
            #################################     
            wr, wc, wd, ws, wg = winner_player
            if gun[wr][wc]:
                gun[wr][wc].append(wg)
                wg = max(gun[wr][wc])
                gun[wr][wc].remove(wg)
                players[winner] = [wr, wc, wd, ws,wg]
print(*answer)

