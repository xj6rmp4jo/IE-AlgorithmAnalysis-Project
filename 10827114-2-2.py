# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系



def printKnapSack(W, wt, val, n):
    ans = list()
    K = [[0 for w in range(W + 1)] for i in range(n + 1)]

    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    res = K[n][W]
    print("Total value =", res)

    w = W
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            ans.append(i)
            res = res - val[i - 1]
            w = w - wt[i - 1]
    return ans


def check(temp):
    if temp[0] < 0 or len(temp) < 2 or temp[1] < 0:
        return False
    else:
        return True


if __name__ == '__main__':
    Weight = int(input("input your weight : "))
    while True:
        if Weight < 0:
            print("input is Negative number input again")
            Weight = int(input("input your weight : "))
        else:
            break

    index = int(input("input how many item : "))
    while True:
        if index < 0:
            print("input is Negative number input again")
            index = int(input("input your weight : "))
        else:
            break
    i = 0
    all = list()
    all_value = list()
    all_weigt = list()
    ans = list()
    while i < index:
        temp = list(input("input item weight and value : ").split())
        temp = map(int, temp)
        temp = list(temp)
        if not check(temp):
            print("input item weight or value is Negative number input again ")
        else:
            print("you need more input", index - i - 1, "item weight and value")
            all.append(temp)
            i += 1
    for j in range(len(all)):
        all_weigt.append(all[j][0])
        all_value.append(all[j][1])

    ans = printKnapSack(Weight, all_weigt, all_value, index)
    ans.sort( reverse = False )
    print("Items", end=" ")
    for n in range(len(ans)):
        if n + 1 == len(ans):
            print(ans[n], end="")
        else:
            print(ans[n], end=", ")
