# 1.init
n, k = map(int,input().split())
stability = list(map(int,input().split()))
# print(n, k)
# print(stability)
"""
3 1
[2, 2, 2, 2, 2, 2]
"""
# 2. execute
answer = 0
person = [0]*n
while True:
    answer += 1
#######################################
# step1. moving work move
#######################################
    stability = [stability[-1]] + stability[:-1] 
    person = [0] + person[:-1] 
    person[-1] = 0
#######################################
# step2. people move
#######################################
    """
    move
        가장 먼저 올라탄 사람부터 
    not move
        1. 앞에 사람있으면 
        2. 안정성 칸 == 0 
    """
    temp = [0]*n
    for x in range(n-2, -1, -1):
        if person[x] == 0:
            continue
        if not (temp[x + 1] == 1 or stability[x + 1] == 0):
            if not (x + 1 == n - 1):
                temp[x+1] = 1
            stability[x+1] -= 1
        else:
            temp[x] = 1
    person = temp
#######################################
# step3. put the people on movingwork 
#######################################      
# 1번 칸 x and 안정성 != 0: 사람을 한 명 더!
    if stability[0] != 0 and person[0] == 0:
        person[0] = 1
        stability[0] -= 1 

#######################################
# step4. finish
#######################################
    if stability.count(0) >= k:
        print(answer)
        break

