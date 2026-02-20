from collections import deque
def move():
    global dices
    top, bottom, up, down, left, right = dices
    # case1. left: top = right, bottom = left, left = top, right = bottom
    if dir == 0: top, bottom, left, right = right, left, top, bottom
    # case2. up: top = right, bottom = left, left = top, right = bottom
    elif dir == 1: top, bottom, up, down = down, up, top, bottom  
    # case3. right: top = left, bottom = right, left = bottom, right = top
    elif dir == 2: top, bottom, left, right = left, right, bottom, top
    # case4. down
    elif dir == 3: top, bottom, up, down = up, down, bottom, top  

    dices = [top, bottom, up, down, left, right]
    
def bfs():
    r, c = start[0], start[1]
    check = arr[r][c]
    v = [[False]*n for _ in range(n)]
    q = deque()
    q.append(start)
    v[r][c] = True
    cnt = 1
    while q:
        cr, cc = q.popleft()
        for d in range(4):
            nr, nc = cr + dr[d], cc + dc[d]
            if 0 <= nr < n and 0 <= nc <n:
                if not v[nr][nc] and arr[nr][nc] == check:
                    v[nr][nc] = True
                    cnt += 1
                    q.append((nr,nc))
    return check*cnt


# 1. init
n, m = map(int, input().split())
arr = [list(map(int,input().split())) for _ in range(n)]
# top, bottom, up, down, left, right
dices = [1,6,5,2,4,3] 
start = [0,0]
# left, up, right, down
dr = [0, -1, 0, 1] 
dc = [-1, 0, 1, 0]
dir = 2

# 2.execute
answer = 0
for _ in range(m):
##############################
# step.1 move the dices and start
##############################
    cr, cc = start[0] + dr[dir], start[1] + dc[dir]
    if 0 <= cr < n and 0 <= cc <n:
         start = [cr,cc]
    else: 
        dir = (dir+2)%4
        start = [start[0] + dr[dir], start[1] + dc[dir]]
    move()
##############################
# step2. bfs
##############################
    answer += bfs()    
##############################
# step3. check the nxt dir
##############################
    if dices[1] > arr[start[0]][start[1]]:
        dir = (dir + 1) % 4
    elif dices[1] < arr[start[0]][start[1]]:
        dir = (dir - 1 ) % 4

print(answer)
