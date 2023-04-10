# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系
def FindMaxSubArray( aList, start, end ) :
    if start == end - 1 :
        return start, end, aList[start]
    else :
        mid = ( start + end ) // 2
        leftStart, leftEnd, leftMax = FindMaxSubArray( aList, start, mid )
        rightStart, rightEnd, rightMax = FindMaxSubArray( aList, mid, end )
        crossStart, crossEnd, crossMax = FindMaxCrossingSubArray( aList, start, mid, end )
        if leftMax > rightMax and leftMax > crossMax:
            return leftStart, leftEnd, leftMax
        elif rightMax > leftMax and rightMax > crossMax:
            return rightStart, rightEnd, rightMax
        else :
            return crossStart, crossEnd, crossMax


def FindMaxCrossingSubArray( aList, start, mid, end ) :
    sumLeft = float( '-inf' )
    sumTemp = 0
    crossStart = mid
    for i in range( mid - 1, start - 1, -1 ) :
        sumTemp += aList[i]
        if sumTemp > sumLeft :
            sumLeft = sumTemp
            crossStart = i

    sumRight = float( '-inf' )
    sumTemp = 0
    crossEnd = mid + 1
    for i in range( mid, end ) :
        sumTemp += aList[i]
        if sumTemp > sumRight :
            sumRight = sumTemp
            crossEnd = i + 1

    return crossStart, crossEnd, sumLeft + sumRight


numOfNumbers = -1
while 1:
    numOfNumbers = int( input() )
    if numOfNumbers == 0 :
        break
    if numOfNumbers < 0 :
        print( "ERROR!!" )
        break
    numList = [ int( n ) for n in input().split() ]
    low, high, sum = FindMaxSubArray( numList, 0, numOfNumbers )
    print( 'Low = ' + str( low + 1 ) + ', High = ' + str( high ) + ', Sum = ' + str( sum ) )
