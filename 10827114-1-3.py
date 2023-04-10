# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系

class Node :
    def __init__(self, Level, WestWolf, WestSheep, BoatSite, EastWolf, EastSheep) : # constructor
        self.level = Level
        self.westWolf  = WestWolf
        self.westSheep = WestSheep

        self.boatSite  = BoatSite  # W = West, E = East

        self.eastWolf  = EastWolf
        self.eastSheep = EastSheep

    def printThisNode( self ) : # { WestWolf WestSheep } { BoatSite } { EastWolf EastSheep }
        #print( repr( self.level ) + " : ", end = '' )
        #print( "( " +         repr( self.westWolf ) + " " + repr( self.westSheep ) + " ) ", end = '' )
        #print( "( " + self.boatSite + " ) ", end = '' )
        #print( "( " +         repr( self.eastWolf ) + " " + repr( self.eastSheep ) + " ) " )
        print( repr( self.westWolf ) + "," + repr( self.westSheep ) + "," + self.boatSite )

    def safe( self ) :
        if self.westWolf > self.westSheep and self.westSheep != 0 : 
            return False
        elif self.eastWolf > self.eastSheep and self.eastSheep != 0 :
            return False
        else :
            return True

    def same( self, node ) :
        if self.westWolf == node.westWolf and self.westSheep == node.westSheep and                      \
           self.eastWolf == node.eastWolf and self.eastSheep == node.eastSheep and                      \
           self.boatSite == node.boatSite :
            return True
        else :
            return False

# ----------------------  End of Class Node ---------------------------

class Type :

    def __init__(self, WestWolf, WestSheep, BoatSite, EastWolf, EastSheep) : # constructor
        self.node = Node( 1, WestWolf, WestSheep, BoatSite, EastWolf, EastSheep )
        self.goal = Node( 0, 0, 0, "E", WestWolf, WestSheep )
        self.list = [ self.node ]

    def printList( self ) :
        for node in self.list :
            node.printThisNode()         

    def findRepeat( self, nowNode ) :
        for node in self.list :
            if node.same( nowNode ) :
                return True

        return False

    def crossTheRiver( self, nowNode ) :
        #nowNode.printThisNode()

        # Case 1 : Achieve Goal
        if nowNode.same( self.goal ) :
            return True

        # Case 2 : Boat W -> E
        if nowNode.boatSite == "W" :
            tryToCrossTheRiver = 0

            # 2 Wolf
            if nowNode.westWolf >= 2 : 
                nextNode = Node( nowNode.level + 1, nowNode.westWolf - 2, nowNode.westSheep, "E", nowNode.eastWolf + 2, nowNode.eastSheep )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # 1 Wolf, 1 Sheep
            if nowNode.westWolf >= 1 and nowNode.westSheep >= 1 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf - 1, nowNode.westSheep - 1, "E", nowNode.eastWolf + 1, nowNode.eastSheep + 1 )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # 2 Sheep
            if nowNode.westSheep >= 2 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf, nowNode.westSheep - 2, "E", nowNode.eastWolf, nowNode.eastSheep + 2 )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # 1 Wolf
            if nowNode.westWolf >= 1 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf - 1, nowNode.westSheep, "E", nowNode.eastWolf + 1, nowNode.eastSheep )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True         
            # 1 Sheep
            if nowNode.westSheep >= 1 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf, nowNode.westSheep - 1, "E", nowNode.eastWolf, nowNode.eastSheep + 1 )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # Can,t Cross The River
            #print( "--- W : return to level " + repr(nowNode.level - 1) )
            self.list.pop()

        # Case 3 : Boat E -> W
        if nowNode.boatSite == "E" :
            tryToCrossTheRiver = 0

            # 2 Wolf
            if nowNode.eastWolf >= 2 : 
                nextNode = Node( nowNode.level + 1, nowNode.westWolf + 2, nowNode.westSheep, "W", nowNode.eastWolf - 2, nowNode.eastSheep )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # 1 Wolf, 1 Sheep
            if nowNode.eastWolf >= 1 and nowNode.eastSheep >= 1 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf + 1, nowNode.westSheep + 1, "W", nowNode.eastWolf - 1, nowNode.eastSheep - 1 )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # 2 Sheep
            if nowNode.eastSheep >= 2 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf, nowNode.westSheep + 2, "W", nowNode.eastWolf, nowNode.eastSheep - 2 )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # 1 Wolf
            if nowNode.eastWolf >= 1 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf + 1, nowNode.westSheep, "W", nowNode.eastWolf - 1, nowNode.eastSheep )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True          
            # 1 Sheep
            if nowNode.eastSheep >= 1 :
                nextNode = Node( nowNode.level + 1, nowNode.westWolf, nowNode.westSheep + 1, "W", nowNode.eastWolf, nowNode.eastSheep - 1 )
                if nextNode.safe() and not Type.findRepeat( self, nextNode ) :
                    tryToCrossTheRiver += 1
                    self.list.append( nextNode )
                    if Type.crossTheRiver( self, nextNode ) :
                        return True
            # Can,t Cross The River
            #print( "--- E : return to level " + repr(nowNode.level - 1) )
            self.list.pop()

# ----------------------  End of class Type ---------------------------

while ( 1 ) : 
    input1, input2 = map( int, input().split() )

    if input1 == 0 and input2 == 0 :
        break

    start = Type( input1, input2, "W", 0, 0 ) # ( WestWolf, WestSheep, BoatSite, EastWolf, EastSheep )

    if start.crossTheRiver( start.node ) : # success crossthe river
        start.printList()
    else :
        print("No solution")