digital_logic = input()
K, M = map(int, input().split())

# Please write your code here.
def solution(digital_logic, K, M):
    answer = 0
    
    # 1. dct update
    dct = {}
    cur = int(digital_logic[:K], 2)
    dct[cur] = 1
    if dct[cur] >= M:
        answer = 1
        return answer

    tmp = 0
    for i in range(K, len(digital_logic)):
        # cur = digital_logic[i: i + K]
        # 1. remove digital char
        remove_digital = int(digital_logic[i - K])
        
        # 2. remove
        cur -= remove_digital*(2**(K-1))

        # 3. 옆으로 밀기
        cur *= 2

        # 4. plus
        cur += int(digital_logic[i])
        
        dct.setdefault(cur, 0)
        dct[cur] += 1
        tmp = max(tmp, dct[cur])

        if tmp == M:
            answer = 1
            break
        
    return answer

# answer
print(solution(digital_logic, K, M))

