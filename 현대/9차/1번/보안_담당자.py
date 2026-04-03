n = int(input())
records = input()

# Please write your code here.
# 1. init
get_mapping = {"(": 0, ")": 1, "?": 2} # 0: 들어옴, 1: 나감 2: 에러
record = [get_mapping[r] for r in records]
curr_in= 0
curr_out = 0

total_in = n // 2
total_out = n // 2

need_in = total_in - record.count(0)
need_out = total_out - record.count(1)

# 2. execute
if n % 2 == 1 or need_in < 0 or need_out < 0:
    print("No")
else:
    is_possible = True
    for i, flag in enumerate(record, start = 1):

        # 1.
        if flag == 0:
            curr_in += 1
        elif flag == 1:
            curr_out += 1
        else:
            if curr_in == curr_out:
                curr_in += 1
                need_in -= 1

            elif curr_in > curr_out:
                if curr_in < total_in and need_in > 0 :
                    curr_in += 1
                    need_in -= 1
                else:
                    curr_out += 1
                    need_out -= 1
         
        # 2. breakpoint
        if curr_in < curr_out:
            is_possible = False
            break
        
        if i == n:
            if (curr_in, curr_out) != (total_in, total_out):
                is_possible = False

    # 3.answer
    if not is_possible or curr_in < curr_out :
        # print(curr_in, curr_out)
        print("No" )
    else:
        # print(is_possible)
        # print(curr_in, curr_out)
        print("Yes")
                


