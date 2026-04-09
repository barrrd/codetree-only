N, B = map(int, input().split())
a = list(map(int, input().split()))

# Please write your code here.
def can(x):
    cost = 0
    for v in a:
        if v < x:
            cost += (x-v)**2
            if cost > B:
                return False
    return True


# 1. binary search
low = min(a)
high = max(a) + int(B**0.5) + 1
ans = 0
while low <= high:
    x = (low+ high) // 2
    if can(x):
        low = x + 1
        ans = x
    else:
        high = x - 1

print(ans)
