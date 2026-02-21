# [삼성 기출] 팩맨

> **문제 링크**: [코드트리 - 팩맨](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/pacman/description)

---

## ⚠️ 구현하면서 헷갈렸던 핵심 포인트 정리

### 1. Update elements in-place using index-based iteration

격자 내부를 순회하며 상태를 변경할 때
**원본 데이터를 직접 수정하지 말 것.**

시뮬레이션 중 기존 배열을 바로 수정하면
아직 처리되지 않은 요소에 영향을 주어 논리 오류 발생 가능.

➡️ 해결 방법

* 새로운 격자 `new_grid` 생성 후
* 모든 계산 완료 뒤 한 번에 교체

이 방식이 시뮬레이션 문제에서 가장 안전하다.

---

### 2. 복제(Clone)는 Deep Copy 필수

```python
eggs.append(arr[i][:])
```

몬스터 복제 시
**깊은 복사(Deep Copy)** 필요.

몬스터가 이동하더라도
'알 상태 몬스터'는 복제 당시의 위치와 방향을 유지해야 함.

따라서 슬라이싱(`[:]`) 또는 `copy/deepcopy`로
**상태 snapshot 유지**가 핵심.

---

### 3. product (Cartesian Product)

팩맨 이동: 3칸
각 이동: 4방향

[
4^3 = 64
]

총 64개의 경로 완전탐색 필요.
```python
def product(lst,k):
    result = []
    path = []
    def backtracking():
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(len(lst)):
            path.append(lst[i])
            backtracking()
            path.pop()
    backtracking()
    return result
```

```python
from itertools import product
paths = list(product(range(4), repeat=3))
```

중복 순열을 이용해 모든 경로 생성 후
문제 조건의 우선순위(상-좌-하-우)에 맞춰
최적 경로 선택.

---

### 4. Memory Optimization: Object → Count (핵심)

#### ❌ 문제점

몬스터를 개별 객체 `[r, c, d]`로 관리하면
복제 턴이 반복될수록 객체 수 폭증
→ **메모리 초과(MLE)** 발생

#### ✅ 해결 방법

몬스터 개별 객체 대신
**3차원 카운팅 배열 사용**

```python
grid[r][c][d] = count
```

#### 결과

격자 크기 고정:

[
4 \times 4 \times 8
]

몬스터가 1억 마리여도
메모리는 고정 크기 유지.

➡️ 시뮬레이션 안정성 + 속도 모두 확보
➡️ 이 문제의 가장 핵심 설계 포인트
