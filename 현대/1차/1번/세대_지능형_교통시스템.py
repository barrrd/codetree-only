N, T = map(int, input().split())
signals = [[[int(x) for x in input().split()] for _ in range(N)] for _ in range(N)]

# Please write your code here.
# 1. init
from collections import deque
# 상 우 하 좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]
signal_lr = {1: [0,1,2], 2: [0,1,3], 3: [0, 2, 3], 4: [1,2,3],
             5: [0,1], 6: [0,3], 7: [2,3], 8: [1,2],
             9: [1,2], 10: [0,1], 11: [3, 0], 12: [2,3]
}
signal_in = {
    1: 1, 2: 0, 3: 3, 4: 2,
    5: 1, 6: 0, 7: 3, 8: 2,
    9: 1, 10: 0, 11: 3, 12: 2 
}

# 2. execute

sr, sc = 0, 0
q = deque([(sr,sc, 0, 0)])
v = set([(sr,sc,0, 0)])
answer = set()
while q:
    cr, cc, cd, turn = q.popleft()
    answer.add((cr, cc))

    if turn < T:
        sig = signals[cr][cc][turn % 4]

        if signal_in[sig] == cd:
            for nxt in signal_lr[sig]:
                nr, nc = cr + dr[nxt], cc + dc[nxt]
                nt = turn + 1

                if not (0 <= nr < N and 0 <= nc < N):
                    continue
                if (nr, nc, nxt, nt) in v:
                    continue

                v.add((nr, nc, nxt, nt))
                q.append((nr, nc, nxt, nt))
print(len(answer))
