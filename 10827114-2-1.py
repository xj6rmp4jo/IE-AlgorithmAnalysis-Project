# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系


import sys
def LCSLength(x, y):
    m = len(x)
    n = len(y)
    b = [[0 for i in range( n + 1 )] for j in range( m + 1 )]
    c = [[0 for i in range( n + 1 )] for j in range( m + 1 )]

    for i in range( 1, m + 1 ):
        for j in range( 1, n + 1 ):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 'diagonal'
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 'up'
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 'pre'
    return b, c

def PrintLcs(b, X, i, j, ansList):
    if i == 0 or j == 0:
        return
    if b[i][j] == 'diagonal':
        PrintLcs(b, X, i - 1, j - 1, ansList)
        ansList.append( X[i - 1] )
    elif b[i][j] == 'up':
        PrintLcs(b, X, i - 1, j, ansList)
    else:
        PrintLcs(b, X, i, j - 1, ansList)


if __name__ == '__main__':
    q = False
    while not q:
        try:
            while True :
                M = int( input( "Input first array length [1,100]: " ) )
                N = int( input( "Input second array length [1,100]: " ) )
                if M == 0 and N == 0 :
                    q = True
                    break
                elif ( 1 <= M <= 100 ) and ( 1 <= N <= 100 ) :
                    break
        except :
            print( "Error with inputting the length" )
            continue

        if q :
            quit()
        X = []
        firstArrayNum = M
        while True :
            tempCh = input( f"Input char for array( { firstArrayNum } ) : " )
            if tempCh.isalpha() and len( tempCh ) == 1 :
                X.append( tempCh )
                firstArrayNum -= 1
                if firstArrayNum == 0 :
                    break
            else :
                print( "Error with inputting the array members" )
        print( "Finish first array" )

        Y = []
        secondArrayNum = N
        while True:
            tempCh = input( f"Input char for array( {secondArrayNum} ) : " )
            if tempCh.isalpha() and len( tempCh ) == 1:
                Y.append( tempCh )
                secondArrayNum -= 1
                if secondArrayNum == 0:
                    break
            else:
                print( "Error with inputting the array members" )
        print( "Finish second array" )

        b, c = LCSLength( X, Y )
        ans = []
        PrintLcs( b, X, M, N, ans )
        print( "Length of LCS =", len( ans ) )
        StrA = "".join( ans )
        print( "LCS =", StrA )
