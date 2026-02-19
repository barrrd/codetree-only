"""
# left, down, right, top
dr = [0, 1, 0, -1]
dc = [-1, 0, 1, 0]

# 2의 배수
0(0,1): 1
1(2,3): 2
2(4,5): 3

# center() -> (0,0) or
while step < n**2:
        이동
        step += 1
######################
curr 위치에서 먼지 제거 및 분산
1. 빗자루: prev -> curr
2. 먼지: 

"""
# 1. init
n = int(input())
dust = [list(map(int,input().split())) for _ in range(n)]
prev = (n//2, n//2)
dr = [0, 1, 0, -1]
dc = [-1, 0, 1, 0]
# print(dust)
# [[123, 20, 212, 32, 7], [170, 13, 37, 43, 23], [52, 57, 0, 248, 123], [12, 10, 721, 112, 147], [37, 89, 231, 13, 36]]

# step2.
def check_dust(prev, curr, dir_num):
    """
    dir_num 기준 
    1. dir_num: a%, 5%
    2. dir_num + 1: 
    2. dir_num - 1:
    """
    global dust, total
    pr, pc = prev
    cr, cc = curr
    # 1.dir_num 방향
    ## case1. a 
    a_sum = dust[cr][cc] - (int(dust[cr][cc]*0.1) + int(dust[cr][cc]*0.07) + int(dust[cr][cc]*0.01) + int(dust[cr][cc]*0.02)) * 2 - int(dust[cr][cc]*0.05)
    ar, ac = cr + dr[dir_num], cc + dc[dir_num]
    if 0 <= ar < n and 0 <= ac < n: dust[ar][ac] += a_sum 
    else: total += a_sum
    ## case2. 5%
    tr, tc =  ar + dr[dir_num], ac + dc[dir_num]
    if 0 <= tr < n and 0 <= tc < n : dust[tr][tc] += int(dust[cr][cc]*0.05)
    else: total += int(dust[cr][cc]*0.05)

    # 2. dir_num + 1
    tr, tc = cr + dr[(dir_num + 1) % 4], cc + dc[(dir_num + 1) % 4]
    ## case1. 7%
    if 0 <= tr < n and 0 <= tc < n : dust[tr][tc] += int(dust[cr][cc]*0.07)
    else: total += int(dust[cr][cc]*0.07)
    ## case2. 2%
    r2, c2 = tr + dr[(dir_num + 1) % 4], tc + dc[(dir_num + 1) % 4]
    if 0 <= r2 < n and 0 <= c2 < n : dust[r2][c2] += int(dust[cr][cc]*0.02)
    else: total += int(dust[cr][cc]*0.02)
    ## case3. 10%
    r3, c3 = tr + dr[dir_num], tc + dc[dir_num]
    if 0 <= r3 < n and 0 <= c3 < n: dust[r3][c3] += int(dust[cr][cc]*0.1)
    else: total += int(dust[cr][cc]*0.1)
    ## case4. 1%
    r4, c4 = tr + dr[(dir_num + 2) % 4], tc + dc[(dir_num + 2) % 4]
    if 0 <= r4 < n and 0 <= c4 < n: dust[r4][c4] += int(dust[cr][cc]*0.01)
    else: total += int(dust[cr][cc]*0.01)

   # 3. dir_num - 1
    tr, tc = cr + dr[(dir_num - 1) % 4], cc + dc[(dir_num - 1) % 4]
    ## case1. 7%
    if 0 <= tr < n and 0 <= tc < n: dust[tr][tc] += int(dust[cr][cc]*0.07)
    else: total += int(dust[cr][cc]*0.07)
    ## case2. 2%
    r2, c2 = tr + dr[(dir_num - 1) % 4], tc + dc[(dir_num - 1 % 4)]
    if 0 <= r2 < n and 0 <= c2 < n: dust[r2][c2] += int(dust[cr][cc]*0.02)
    else: total += int(dust[cr][cc]*0.02)
    ## case3. 10%
    r3, c3 = tr + dr[dir_num], tc + dc[dir_num]
    if 0 <= r3 < n and 0 <= c3 < n: dust[r3][c3] += int(dust[cr][cc]*0.1)
    else: total += int(dust[cr][cc]*0.1) 
    ## case4. 1%
    r4, c4 = tr + dr[(dir_num - 2)% 4], tc + dc[(dir_num - 2) % 4]
    if 0 <= r4 < n and 0 <= c4 < n: dust[r4][c4] += int(dust[cr][cc]*0.01)
    else: total += int(dust[cr][cc]*0.01)






# 2. execute
        #########################################################
        # step1. prev
        #########################################################
step = 0
total = 0
flag = False
# while ttt != n**2 - 1 :
while True :
        #########################################################
        # step1. prev
        #########################################################
        nr, nc = dr[step % 4], dc[step % 4]
        mul = step // 2 + 1
        pr, pc = prev[0], prev[1]
        cr, cc = pr, pc
        er, ec = nr * mul + pr, nc * mul + pc
        # print(f"er, ec: {er, ec}")
        # print('*'*10)
        while prev != (er, ec):
                cr += nr
                cc += nc
                if cr < 0 or cc < 0:
                        flag = True
                        break
        #########################################################
        # step2. calculate the dust
        #########################################################
                check_dust(prev, (cr,cc), step % 4) 
                # print((cr,cc))
                prev = (cr,cc)

        # print()
        if flag:
                break

        
        #########################################################
        # step
        #########################################################
        step += 1
print(total)
