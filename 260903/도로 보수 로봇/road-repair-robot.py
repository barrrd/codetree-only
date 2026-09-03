N, K = map(int, input().split())
positions = list(map(int, input().split()))

# Please write your code here.
def solution(N, K, positions):
    answer = 0
    
    min_l = 1
    max_l = max(positions) + 1
    
    while min_l <= max_l:
        length = (min_l + max_l)//2
        possible = True

        tmp_k = 0
        end = 0
        for p in positions:
            if end >= p:
                continue
            end = p + length - 1
            tmp_k += 1

            if tmp_k > K:
                possible = False
                break
        # print(f"{length}: {possible}하고 {tmp_k}개")
        if possible:
            answer = length
            max_l = length - 1
            
        else:
            min_l = length + 1


    return answer

# answer
print(solution(N, K, positions))

