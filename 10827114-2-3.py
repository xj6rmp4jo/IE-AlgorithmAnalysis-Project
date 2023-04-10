# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系


class Node :

    def __init__( self, letter, count ) : # letter's constructor
        self.type      = "letter"
        self.code      = "@"
        self.letter    = letter
        self.count     = count
        self.leftNode  = None
        self.rightNode = None

# ----------------------  End of Class Node ---------------------------

class HuffmanCoding : 
    def __init__( self ) : # constructor
        self.letterList = []
        self.nodeList   = []
        self.ansList    = []


    def push( self, node ) :
        self.letterList.append( node )
        self.nodeList.append( node )

    
    def printLetterList( self ) :

        for node in self.letterList :
            print( node.letter + " " + node.code )


    def setHuffmanCode( self, node, code ) :

        if node.type == "dot" :
            HuffmanCoding.setHuffmanCode( self, node.leftNode,  code + "0" )
            HuffmanCoding.setHuffmanCode( self, node.rightNode, code + "1" )

        elif node.type == "letter" :
            for node_ in self.letterList :
                if node.letter == node_.letter :
                    node_.code = code


    def sortNodeList( self ) :

        for a in range( 0, len( self.nodeList ) - 1 ) : # range( 1, howManyNumber + 1 )  ->  1 ~ howManyNumber
            for b in range( a + 1, len( self.nodeList ) ) :
                if self.nodeList[a].count > self.nodeList[b].count :
                    temp = self.nodeList[a]
                    self.nodeList[a] = self.nodeList[b]
                    self.nodeList[b] = temp


    def combineNodeList( self ) :
        n = Node( "", self.nodeList[0].count + self.nodeList[1].count )
        n.type      = "dot"
        n.code      = -1
        n.leftNode  = self.nodeList[0]
        n.rightNode = self.nodeList[1]

        self.nodeList[0].code = "0"
        self.nodeList[1].code = "1"

        self.nodeList.pop( 0 )
        self.nodeList.pop( 0 )
        self.nodeList.append( n )


    def generateTree( self ) :

        while ( len( self.nodeList ) > 1 ) :
            HuffmanCoding.sortNodeList( self )
            HuffmanCoding.combineNodeList( self )

        HuffmanCoding.setHuffmanCode( self, self.nodeList[0], "" )


    def decode( self, code ) :
        re = ""
        findAll = False

        while ( not findAll ) :
            findcode = ""
            findOne = False

            for a in range( 0, len( code ) ) :
                findcode += code[a]
                #print( "findcode = " + findcode )

                for node in self.letterList :

                    if node.code == findcode :
                        findOne = True
                        re += node.letter
                        #print( "re = " + re )

                        if code == findcode :
                            findAll = True
                        else :
                            code = code[ a + 1 : len( code ) ]
                            #print( "code = " + code )

                        break

                if findOne :
                    break

        return re


# ----------------------  End of Class Tree ---------------------------

count = 0

while ( 1 ) : 
    count += 1
    howManyNumber = int( input() )

    if ( howManyNumber == 0 ) :
        break

    HC = HuffmanCoding()
    illegalChar = False
    positiveNumber = True

    for a in range( 1, howManyNumber + 1 ) : # range( 1, howManyNumber + 1 )  ->  1 ~ howManyNumber
        letter, num = map( str, input().split() )
        num = int( num )

        if 'a' <= letter and letter <= 'z' or 'A' <= letter and letter <= 'Z' :
            None
        else :
            illegalChar = True

        if num <= 0 :
            positiveNumber = False

        node = Node( letter, num )
        HC.push( node )

    code = input()
    print( "\nHuffman Codes #" + repr( count ) )

    if illegalChar == True :
        print( "Find Illegal Char !!" )
    elif positiveNumber == False :
        print( "Find zero or negative number !!" )
    else :
        HC.generateTree()
        HC.printLetterList()
        print( "Decode = " + HC.decode( code ) )
        print()