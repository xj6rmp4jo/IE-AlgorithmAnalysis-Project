# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系
import numpy as np

def InputAndCheck( num, answerList ):
    stoneList = []
    for i1 in range( num ) :
        temp = input()
        if len( temp ) == 1 :
            print( 'Length of word must be more than 1' )
            return False;
        stoneList.append( temp )

    for index in range( len( stoneList ) ) :
        tempList = [stoneList[index]]
        bool = False
        while not bool:
            bool = True
            for j in range( len( stoneList ) ) :
                if CheckNotExist( stoneList[j], tempList ) and ( tempList[len( tempList ) - 1][len( tempList[len( tempList ) - 1] ) - 1] == stoneList[j][0] ) :
                    tempList.append( stoneList[j] )
                    bool = False

        if len( tempList ) == num :
            for copyI in range( len( tempList ) ) :
                answerList.append( tempList[copyI] )
            return True

    return False

def CheckNotExist( name, List ) :
    for i2 in range( len(List) ) :
        if name == List[i2] :
            return False

    return True


indexOfDoor = 1
numOfStone = -1
while 1:
    numOfStone = int( input() )
    if numOfStone == 0 :
        break
    if ( numOfStone < 3 ) or ( numOfStone > 9 ) :
        print( 'Error Num!!' )
        break
    aList = []
    print( 'Secret Door ' + str(indexOfDoor) )
    if InputAndCheck( numOfStone, aList ) :
        print( 'Can be opened.' )
        for i in range( len( aList ) - 1 ) :
            print( aList[i], end = '-' )
        print( aList[len( aList ) - 1] + '\n' )
    else :
        print( 'Can not be opened.' + '\n')
    indexOfDoor += 1
