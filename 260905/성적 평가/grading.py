N = int(input())
scores = [list(map(int, input().split())) for _ in range(3)]

# Please write your code here.
def solution(N, scores):
    final = [0]*len(scores[0])
    for score in scores:
        answer = [0]*len(score)
        
        tmp = {}
        for idx, s in enumerate(score):
            tmp.setdefault(s, {"index" : [], "ranking": 0})
            tmp[s]["index"].append(idx)
            final[idx] += s
        
        # 1. make a ranking
        rank = 1
        plus = 0
        order = sorted(score, reverse = True)
        cur = order[0]
        for s in order:
            if s == cur:
                plus += 1
                tmp[s]["ranking"] = rank
            else:
                rank += plus
                tmp[s]["ranking"] = rank
                plus = 1
                cur = s

        # 2. update a answer
        for k in tmp:
            rank = tmp[k]["ranking"]
            for idx in tmp[k]["index"]:
                answer[idx] = rank
        
        print(*answer)
            
    # 3. final
    answer = [0] * len(scores[0])
    tmp = {}

    # 먼저 tmp 완성
    for idx, s in enumerate(final):
        tmp.setdefault(s, {"index": [], "ranking": 0})
        tmp[s]["index"].append(idx)


    # 그 다음 ranking 계산
    rank = 1
    plus = 0

    order = sorted(final, reverse=True)
    cur = order[0]

    for s in order:
        if s == cur:
            plus += 1
            tmp[s]["ranking"] = rank
        else:
            rank += plus
            tmp[s]["ranking"] = rank

            plus = 1
            cur = s


    # 마지막 answer에 등수 넣기
    for k in tmp:
        rank = tmp[k]["ranking"]

        for idx in tmp[k]["index"]:
            answer[idx] = rank

    print(*answer)


solution(N, scores)