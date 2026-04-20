n = int(input())
records = input()

# Please write your code here.
if n % 2 != 0:
    print("No")
else:
    in_cnt,out_cnt = 0, 0
    need_in, need_out = 0, 0
    for r in records:
        if r == "(":
            in_cnt += 1
        elif r == ")":
            out_cnt += 1
    need_in = n// 2- in_cnt
    need_out = n//2 - out_cnt

    # 2. execute
    total = 0
    is_possible = True
    for r in records:
        if r == "(":
            total += 1
        elif r == ")":
            total -= 1
        elif r == "?":
            if need_in > 0:
                total += 1
                need_in -= 1
            elif need_out > 0:
                total -= 1
                need_out -= 1
        
        if total < 0:
            is_possible = False
            break
    
    if is_possible:
        if total == 0:
            print("Yes")
        else:
            print("No")
    else:
        print("No")
