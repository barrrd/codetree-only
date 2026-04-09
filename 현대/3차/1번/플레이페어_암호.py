message = input()
key = input()

# Please write your code here.
# 1. make a array that 5*5
from collections import deque

arr = [[""]*5 for _ in range(5)]
idx_tmp = 0
vis = set()
vis.add("J")
for k in key:
    if k in vis:
        continue
    arr[(idx_tmp // 5)][idx_tmp % 5] = k
    vis.add(k)
    idx_tmp += 1

for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    if ch in vis:
        continue
    arr[(idx_tmp // 5)][idx_tmp % 5] = ch
    vis.add(idx_tmp)
    idx_tmp += 1

# 2. make a 암호하: 같은 경우 X
step2 = []
tmp = deque()
for idx, ch in enumerate(message, start = 1):
    tmp.append(ch)
    
    if len(tmp) != 2:
        continue
    
    fir = tmp.popleft()
    sec = tmp.popleft()

    if fir != sec:
        step2.append((fir + sec))
        tmp = deque()
    else:
        if fir == "X":
            step2.append((fir + "Q" ))
            tmp.append(sec)
        else:
            step2.append((fir + "X"))
            tmp.append(sec)

if tmp:
    fir = tmp.popleft()
    step2.append((fir + "X"))


# 3. 
step3 = ""
for char in step2:
    fir, sec = char[0], char[1]
    for r in range(5):
        for c in range(5):
            if fir == arr[r][c]:
                fr, fc = r, c
            if sec == arr[r][c]:
                sr, sc = r, c

    # case1: same row
    if fr == sr:
        n_fc, n_sc = (fc + 1) % 5, (sc + 1) % 5
        new_f, new_s = arr[fr][n_fc], arr[sr][n_sc]
        step3 += new_f + new_s

    # case2: same col:
    elif fc == sc:
        n_fr, n_sr = (fr + 1) % 5, (sr + 1) % 5
        new_f, new_s = arr[n_fr][fc], arr[n_sr][sc]
        step3 += new_f + new_s
    
    # case3. different
    else:
        new_f, new_s = arr[fr][sc], arr[sr][fc]
        step3 += new_f + new_s

print(step3)

