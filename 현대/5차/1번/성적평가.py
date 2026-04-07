N = int(input())
scores = [list(map(int, input().split())) for _ in range(3)]

# Please write your code here.
# 1. 3 competition
for score in scores:
    
    score_idx = [(s, idx)for idx, s in enumerate(score)]
    score_idx.sort(key = lambda x: -x[0])

    answer = [0 for _ in range(len(score_idx))]
    plus = 0
    rank = 1
    prev = score_idx[0][0]
    for s, idx in score_idx:
        if s == prev:
            answer[idx] = rank
            plus += 1
        else:
            rank += plus
            answer[idx] = rank
            prev = s
            plus = 1
    print(*answer)

# 2. final_score
final_score = [0 for _ in range(len(scores[0]))]
for r in range(len(scores)):
    for c in range(len(scores[0])):
        final_score[c] += scores[r][c]
final_idx = [(s,idx) for idx, s in enumerate(final_score)]
final_idx.sort(key = lambda x: -x[0])
answer = [0 for _ in range(len(final_idx))]
plus = 0
rank = 1
prev = final_idx[0][0]
for s, idx in final_idx:
    if s == prev:
        answer[idx] = rank
        plus += 1
    else:
        rank += plus
        answer[idx] = rank
        prev = s
        plus = 1
print(*answer)

