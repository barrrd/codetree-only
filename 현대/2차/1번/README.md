# [HSAT] Garage Game

> **문제 링크**: [코드트리 - Garage Game](https://www.codetree.ai/ko/frequent-problems/hsat/problems/garage-game/description)

---

## ⚠️ 구현 시 주의해야 할 핵심 포인트

### 1) 제거 가능한 그룹은 `크기 2 이상`이어야 함

문제에서 자동차는 **선택한 칸과 상하좌우 중 같은 색이 있을 때만** 사라지기 시작한다.
즉, **혼자 떨어져 있는 1칸짜리 그룹은 제거할 수 없다.**

따라서 BFS/DFS로 같은 색 연결 요소를 구한 뒤에도 반드시 다음 조건을 확인해야 한다.

```python
if len(point) == 1:
    continue
```

이 조건이 없으면 실제로는 제거할 수 없는 칸도 제거 후보로 들어가 정답이 틀리게 된다.

---

### 2) 중력은 `보이는 N칸`만이 아니라 `전체 3N칸`에 대해 적용해야 함

입력은 총 `3N`행으로 주어지고, 실제로 현재 보이는 차고는 **아래쪽 `N행`** 이다.
하지만 자동차가 사라진 뒤에는 위쪽에 대기하던 자동차들이 아래로 떨어져 빈 칸을 채우므로,
중력은 **각 열 전체 `3N`칸을 하나의 세로 스택처럼 보고 처리**해야 한다.

즉 각 열마다:

1. `0`이 아닌 값만 위에서 아래 순서대로 모으고
2. 그것을 다시 **아래에서부터 채우고**
3. 남는 윗칸은 `0`으로 채운다.

```python
for col in range(N):
    temp = []
    for row in range(3 * N):
        if new_colors[row][col] != 0:
            temp.append(new_colors[row][col])

    idx = 3 * N - 1
    for i in range(len(temp) - 1, -1, -1):
        new_colors[idx][col] = temp[i]
        idx -= 1

    while idx >= 0:
        new_colors[idx][col] = 0
        idx -= 1
```

---

### 3) BFS는 현재 보이는 **아래쪽 `N x N` 영역만** 탐색해야 함

같은 색 연결 요소를 찾을 때는 실제로 선택 가능한 영역인 **아래 `N행`만** 대상으로 봐야 한다.
따라서 범위 조건은 다음과 같다.

```python
2 * N <= nr < 3 * N and 0 <= nc < N
```

위쪽 `2N`행은 자동차 공급 영역일 뿐, 현재 선택 가능한 차고 칸이 아니다.

---

### 4) 점수 계산은 `제거 개수 + 최소 직사각형 넓이`

한 번 제거할 때의 점수는 다음 두 값의 합이다.

* 사라진 자동차의 개수
* 사라진 칸들을 모두 포함하는 가장 작은 직사각형의 넓이

따라서 연결 요소 좌표를 구한 뒤 다음처럼 계산한다.

```python
min_r = min(r for r, c in point)
max_r = max(r for r, c in point)
min_c = min(c for r, c in point)
max_c = max(c for r, c in point)

area = (max_r - min_r + 1) * (max_c - min_c + 1)
score = len(point) + area
```

---

### 5) 총 3턴이므로 `DFS 완전탐색` 가능

매 턴마다 선택 가능한 그룹 중 하나를 제거해야 하고,
이 선택이 다음 상태의 보드에 영향을 주므로 **그리디로 풀 수 없다.**

하지만 턴 수가 정확히 `3번`으로 매우 작기 때문에,
현재 상태에서 제거 가능한 모든 그룹을 시도해 보는 **DFS 완전탐색**이 가능하다.

구조는 다음과 같다.

* **BFS**: 현재 보이는 영역에서 같은 색 그룹 찾기
* **DFS**: 3턴 동안 가능한 모든 선택 시도

---

### 6) 제거 가능한 그룹이 하나도 없으면 그 상태에서 종료

현재 턴에서 제거 가능한 그룹이 없다면 더 이상 진행할 수 없으므로,
그 시점의 누적 점수로 정답을 갱신해야 한다.

```python
if not found:
    answer = max(answer, total)
```

이 처리가 없으면 중간에 더 이상 제거할 수 없는 경우를 놓쳐서 오답이 날 수 있다.

---

### 7) 변수 재사용(`r`, `c`) 실수 주의

바깥 탐색 루프에서도 `r`, `c`를 쓰고,
gravity 내부 루프에서도 다시 `r`, `c`를 쓰면
탐색 중인 좌표 값이 덮어써져 후보를 건너뛰는 문제가 생길 수 있다.

예를 들어 아래처럼 쓰면 위험하다.

```python
for r in range(2 * N, 3 * N):
    for c in range(N):
        ...
        for c in range(N):
            for r in range(3 * N):
```

따라서 중력 처리에서는 `row`, `col`처럼 **다른 이름으로 분리**하는 것이 안전하다.

---

## 풀이 아이디어

### 1. 현재 보이는 아래 `N x N` 영역에서 모든 연결 요소 탐색

각 칸에 대해 BFS를 수행해 같은 색 그룹을 찾는다.
단, 그룹의 크기가 1이면 제거 불가능하므로 제외한다.

---

### 2. 제거 가능한 각 그룹을 하나씩 선택

선택한 그룹에 대해

* 점수 계산
* 해당 칸들을 0으로 제거
* 중력 적용

을 수행해 다음 상태의 보드를 만든다.

---

### 3. 다음 턴으로 재귀 진행

깊이(`depth`)를 1 증가시켜 다음 턴을 탐색한다.
총 3턴 반복 후 최댓값을 정답으로 갱신한다.

---

## 전체 코드

```python
from collections import deque

N = int(input())
colors = [list(map(int, input().split())) for _ in range(3 * N)]


def bfs(sr, sc, colors, v):
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    color = colors[sr][sc]
    q = deque([(sr, sc)])
    v[sr][sc] = True
    group = [(sr, sc)]

    while q:
        cr, cc = q.popleft()
        for i in range(4):
            nr, nc = cr + dr[i], cc + dc[i]

            if not (2 * N <= nr < 3 * N and 0 <= nc < N):
                continue
            if v[nr][nc]:
                continue
            if colors[nr][nc] != color:
                continue

            v[nr][nc] = True
            q.append((nr, nc))
            group.append((nr, nc))

    return group



def dfs(depth, colors, total):
    global answer

    if depth == 3:
        answer = max(answer, total)
        return

    v = [[False] * N for _ in range(3 * N)]
    found = False

    for r in range(2 * N, 3 * N):
        for c in range(N):
            if v[r][c]:
                continue

            point = bfs(r, c, colors, v)

            if len(point) == 1:
                continue

            found = True

            min_r = min(rr for rr, cc in point)
            max_r = max(rr for rr, cc in point)
            min_c = min(cc for rr, cc in point)
            max_c = max(cc for rr, cc in point)

            area = (max_r - min_r + 1) * (max_c - min_c + 1)
            score = len(point) + area

            new_colors = [row[:] for row in colors]
            for rr, rc in point:
                new_colors[rr][rc] = 0

            for col in range(N):
                temp = []
                for row in range(3 * N):
                    if new_colors[row][col] != 0:
                        temp.append(new_colors[row][col])

                idx = 3 * N - 1
                for i in range(len(temp) - 1, -1, -1):
                    new_colors[idx][col] = temp[i]
                    idx -= 1

                while idx >= 0:
                    new_colors[idx][col] = 0
                    idx -= 1

            dfs(depth + 1, new_colors, total + score)

    if not found:
        answer = max(answer, total)


answer = 0
dfs(0, colors, 0)
print(answer)
```

---

## 시간 복잡도

한 상태에서:

* 아래 `N x N` 영역을 BFS로 그룹화
* 제거 가능한 그룹마다 다음 상태 생성

을 수행한다.

턴 수가 고정 `3`이므로 전체 탐색량은 충분히 감당 가능하다.
즉, 이 문제는 **깊이 3의 완전탐색 + BFS 그룹 탐색**으로 해결할 수 있다.

---

## 정리

이 문제의 핵심은 다음 4가지다.

1. **크기 1 그룹은 제거 불가**
2. **중력은 각 열의 전체 `3N`칸에 적용**
3. **현재 보이는 아래 `N행`만 BFS 탐색**
4. **3턴이므로 DFS 완전탐색 가능**

즉, 이 문제는 **BFS로 그룹을 찾고, DFS로 3번의 선택을 모두 탐색하는 구현 문제**라고 볼 수 있다.
