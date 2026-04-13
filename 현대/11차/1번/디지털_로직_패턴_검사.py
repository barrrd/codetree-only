digital_logic = input()
K, M = map(int, input().split())

# Please write your code here.
dct = {}
full_mask = (1<<K) - 1
mask = 0
flag = True
# for i in range(len(digital_logic)- K + 1):
for i, ch in enumerate(digital_logic):
    bit = int(ch)

    mask = ((mask<<1) | bit) & full_mask

    if i >= K - 1:
        dct[mask] = dct.get(mask, 0) + 1
        if dct[mask] >= M:
            print(1)
            break
else:
    print(0)
