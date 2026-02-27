# [삼성 기출] 싸움땅

> **문제 링크**: [코드트리 - 싸움땅](https://www.codetree.ai/ko/frequent-problems/samsung-sw/problems/battle-ground/description)

---

## ⚠️ 구현하면서 헷갈렸던 핵심 포인트

### 1) 플레이어 / 총 / 위치 상태를 반드시 분리해야 한다

격자(`arr`) 하나에 플레이어와 총을 같이 저장하면  
자료형이 섞이고 상태 업데이트 순서가 꼬이기 쉽다.

➡️ 해결: 상태를 3개의 구조로 분리한다.

- `gun[r][c]` : 해당 칸의 총 리스트
- `who[r][c]` : 해당 칸에 있는 플레이어 id
- `players[id]` : `[r, c, d, s, g]` (위치, 방향, 초기 능력치, 들고 있는 총)

이 구조로 분리하면

```text
이동 → 싸움 → 패자 이동 → 총 교환
