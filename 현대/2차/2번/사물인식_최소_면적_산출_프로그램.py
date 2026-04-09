N, K = map(int, input().split())
points = [[] for _ in range(K + 1)]

for _ in range(N):
    x, y, k = map(int, input().split())
    points[k].append((x, y))

# Please write your code here.
# 1. make a colors 
colors = [i for i in range(1, K + 1)]
colors.sort(key = lambda x: len(points[x]))


# # 2. make a combinations !!
# cases = [[]]
# for color in colors:
#     new_cases = []
    
#     for case in cases:
#         for point in points[color]:
#             new_cases.append(case + [point])
   
#     cases = new_cases

# # 3. answer
# answer = float("inf")
# for case in cases:
#     min_x, min_y, max_x, max_y = float("inf"), float("inf"), -float("inf"), -float("inf")
#     for x, y in case:
#         min_x, min_y = min(x, min_x), min(y, min_y)
#         max_x, max_y = max(x, max_x), max(y, max_y)
    
#     square = abs(max_x - min_x) * abs(max_y - min_y)
#     answer = min(answer, square)

# print(answer)

# 2. make a dfs
answer = float("inf")
def dfs(idx, min_x, max_x, min_y, max_y):
    global answer
    if idx == K:
        area = (max_x - min_x) * (max_y - min_y)
        answer = min(answer, area)
        return

    color = colors[idx]

    for x, y in points[color]:
        nmin_x = min(min_x, x)
        nmax_x = max(max_x, x)
        nmin_y = min(min_y, y)
        nmax_y = max(max_y, y)
        
        area = (nmax_x - nmin_x) * (nmax_y - nmin_y)
        if area >= answer:
            continue

        dfs(idx + 1, nmin_x, nmax_x, nmin_y, nmax_y)


dfs(0, float("inf"), -float("inf"), float("inf"), -float("inf"))


print(answer)
