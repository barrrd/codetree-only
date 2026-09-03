N = int(input())
records = input()

# Please write your code here.
def solution(N, records):
    answer = "No"
    if N % 2 == 1:
        return answer
    
    i_cnt, o_cnt = 0, 0
    left_in, left_out = N // 2, N // 2
    dct_change= {"(": (1,0),")": (0,1), "?": [(1,0), (0,1)]}

    for record in records:
        if record == "(":
            left_in -= 1
        elif record == ")":
            left_out -= 1

    answer = "Yes"
    for num, record in enumerate(records, 1):

        # 1. in
        if record == "(":
            i_cnt += 1
            # left_in -= 1
        
        # 2. out
        elif record == ")":
            o_cnt += 1
            # left_out -= 1
        
        # 3. ?
        else:
            if left_in > 0:
                i_cnt += 1
                left_in -= 1
            
            else:
                o_cnt += 1
                left_out -= 1
        
        ## 판단
        if num == N:
            if i_cnt == o_cnt:
                answer = "Yes"
                return answer
            else:
                answer = "No"
                return answer
  

        if i_cnt < o_cnt or left_in < 0 or left_out < 0:
            answer = "No"
            return answer
        
        # print(f"현재 in, 현재_out: {i_cnt}, {o_cnt}")
        # print(f"남은_in, 남은_out: {left_in}, {left_out}")      
        # print()  
    
    return answer

print(solution(N, records))