N = int(input())
sequence = list(map(int, input().split()))

# Please write your code here.


ans = 0
for i in range(N):
    count = 0    
    cnt = [0] * (N + 1)

    for k in range(N - 1, i, - 1):
        if sequence[k] < sequence[i]:
            count += 1
        cnt[k] = count


    for j in range(i + 1, N):
        if sequence[i] < sequence[j]:
            ans += cnt[j]
    

print(ans)
