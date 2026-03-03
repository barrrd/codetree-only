# [삼성 기출] 메이즈러너

> **문제 링크**: [코드트리 - 메이즈러너](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/maze-runner/description)

---

## ⚠️ 구현하면서 헷갈렸던 핵심 포인트

### 1) “출구 + 최소 1명 플레이어”를 포함하는 최소 정사각형 찾기 (우선순위까지)

이 문제의 회전은 **아무 정사각형이 아니라 특정 조건을 만족하는 정사각형**을 찾아야 한다.

조건은 다음과 같다.

* **출구 `(tr, tc)`를 반드시 포함**
* **플레이어가 최소 1명 이상 포함**
* **한 변 길이(`length`)가 최소**
* 길이가 같다면 **시작 좌표 `(row → col)`가 작은 것**

핵심은 **이 우선순위를 코드에서 따로 비교하지 않고 탐색 순서 자체로 보장하는 것**이다.

➡️ 해결 방법

* `length`를 **2부터 증가시키며 탐색**
* 같은 길이에서는 **row → col 순서로 탐색**
* **처음 발견되는 정사각형을 바로 확정**

```python
square = []
found = False

for length in range(2, n+1):                    # 1) 최소 길이 보장
    for row in range(n - length + 1):           # 2) row 작은 것 우선
        for col in range(n - length + 1):       # 3) col 작은 것 우선
            row_end, col_end = row + length - 1, col + length - 1

            # 출구 포함 필수
            if not (row <= tr <= row_end and col <= tc <= col_end):
                continue

            # 플레이어 1명 이상 포함 필수
            if any(row <= pr <= row_end and col <= pc <= col_end for pr, pc in players):
                square = [row, col, length]
                found = True
                break
        if found:
            break
    if found:
        break
```

이 방식이면 다음 우선순위를 **추가 비교 없이 자동으로 만족**한다.

```
최소 길이 → row 작은 것 → col 작은 것
```

---

### 2) 부분 회전은 “격자 회전 + 좌표 회전”을 반드시 같이 처리해야 한다

정사각형을 회전할 때는 단순히 `arr`만 회전하는 것이 아니다.

함께 회전해야 하는 것들

* 격자 값 (`arr`)
* 출구 좌표 `(tr, tc)`
* 플레이어 좌표 `(pr, pc)`

여기서 자주 발생하는 실수

* 격자만 회전하고 **좌표를 돌리지 않는 경우**
* 좌표 회전 시 **기준점을 (0,0)으로 이동하지 않고 바로 회전**
* **사각형 밖 플레이어까지 같이 회전하는 경우**

➡️ 해결 방법

좌표 회전은 항상 **정사각형 시작점 `(sr, sc)` 기준으로 로컬 좌표로 변환한 뒤 회전**하고 다시 복귀한다.

```python
def rot_point_cw(sr, sc, length, r, c):
    # (0,0) 기준으로 이동
    orr, occ = r - sr, c - sc

    # 시계 방향 회전
    rr, rc = occ, length - 1 - orr

    # 원래 좌표로 복귀
    return sr + rr, sc + rc
```

그리고 **사각형 내부 좌표만 회전**해야 한다.

```python
row, col, length = square

# 1) 출구 회전
tr, tc = rot_point_cw(row, col, length, tr, tc)

# 2) 플레이어 회전
new_players = []
for pr, pc in players:
    if row <= pr < row + length and col <= pc < col + length:
        pr, pc = rot_point_cw(row, col, length, pr, pc)
    new_players.append([pr, pc])

players = new_players
```

이렇게 **격자 회전과 좌표 회전을 동일한 기준으로 처리하면**
회전 이후 상태가 꼬이지 않는다.
