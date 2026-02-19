"""
step1. 
격자 벗어나지 않을떄, 4방향 중 좋아하는 친구 수 
step2.
> step1 에서 동일한 것이 존재 -> 인접한 곳에서 비어있는 칸 수 높은 순
step3.
> step2 에서 동일한 것이 존재 -> 행이 row한 거 choose
step4.
> step3 에서 동일한 것이 존재 -> 열이 row한 거 choose
"""
# 1.init
n = int(input())
lst = [list(map(int,input().split())) for _ in range(n**2)]
arr = [[0]*n for _ in range(n)]
# cr, cc = (2, 2)
# arr[1][1] = lst[0][0]
# print(lst)
# [[3, 5, 8, 9, 2], [6, 1, 2, 3, 4], [1, 5, 8, 7, 6], [8, 2, 5, 3, 1], [9, 4, 8, 2, 1], [4, 6, 5, 7, 8], [7, 3, 4, 2, 9], [2, 1, 6, 3, 5], [5, 4, 3, 8, 6]]

# 2.execute
    ###############################################
    # step
    ###############################################
dr = [0, -1, 0, 1] # left, top, right, down
dc = [-1, 0, 1, 0] # left, top, right, down
step = 0
for idx, l in enumerate(lst):
    # if step == 4:
    #     break
    ###############################################
    # step1.격자 벗어나지 않을떄, 4방향 중 좋아하는 친구 수 
    ###############################################  
    n0, n1, n2, n3, n4 = l
    # # 1. first  
    # if idx == 0:
    #     arr[n//2][n//2] = n0
    #     continue
    # 2. 전체에서 찾기
    tmp = {}
    for rr in range(n):
        for rc in range(n):
                if arr[rr][rc] != 0:
                    continue
                # 3. check the 4 dirs
                like_cnt = 0
                empty_cnt = 0
                for d in range(4):
                    r1, c1 = rr + dr[d], rc + dc[d]
                    if 0 <= r1 < n and 0 <= c1 < n:
                        if arr[r1][c1] in [n1, n2, n3, n4]:
                            like_cnt += 1
                        if arr[r1][c1] == 0:
                            empty_cnt += 1
                tmp[(rr, rc)] = [like_cnt, empty_cnt]
                # print(tmp)
                # {(1, 0): [1, 2], (0, 1): [1, 2], (1, 2): [1, 2], (2, 1): [1, 2]}
    ###############################################
    # step2~4
    ###############################################  
    sorted_tmp = sorted(tmp.items(), key = lambda x: (-x[1][0], -x[1][1], x[0][0], x[0][1]))
    best = sorted_tmp[0][0]
    arr[best[0]][best[1]] = n0
    # print(arr)
    # [(1, 0), (0, 1), (1, 2), (2, 1)]

# 3. final calculate
llst = sorted(lst, key = lambda x: x[0])
answer = 0
for r in range(n):
    for c in range(n):
        check = arr[r][c]
        cnt = 0
        for d in range(4):
            r5, c5 = r + dr[d], c + dc[d]
            if 0 <= r5 < n and 0 <= c5 < n:
                if arr[r5][c5] in llst[check - 1][1:]:
                    cnt += 1
        if cnt > 0:
            answer += 10**(cnt - 1)
print(answer)      
            
