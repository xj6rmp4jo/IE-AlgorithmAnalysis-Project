# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系


from operator import truediv


class State :
    def __init__( self, you, box, map ) :
        self.you    = you
        self.box    = box
        self.map    = map


    def Same( self, state ) :
        if self.you == state.you and self.box == state.box :
            return True
        else :
            return False


    def PrintState( self ) :
        print( "S : " + repr( self.you[0] )    + " " + repr( self.you[1] )    )
        print( "B : " + repr( self.box[0] )    + " " + repr( self.box[1] )    )
        print()

    def PrintMap( self ) :
        for line in self.map :
            print( line )

# ----------------------  End of Class Sokoban ---------------------------


class Sokoban :

    def __init__( self, map ) : # set coordinate
        self.you      = [-1, -1] # S
        self.box      = [-1, -1] # B
        self.target   = [-1, -1] # T
        self.map      = map
        self.mapError = False
  

        for a in range( 0, len( map ) ) :

            lineOfMap = map[a]
            for b in range( 0, len( lineOfMap ) ) :
                if   lineOfMap[b] == 'S' :
                    self.you = [a, b]
                elif lineOfMap[b] == 'B' :
                    self.box = [a, b]
                elif lineOfMap[b] == 'T' :
                    self.target = [a, b]

        if self.you == [-1, -1] or self.box == [-1, -1] or self.target == [-1, -1] : # not find
            self.mapError = True
        else :
            self.nowState = State( self.you, self.box, map )
            self.stateList = [ ]
            self.ansList = [ ]
 
    
    def PrintCoordinate( self ) :
        print( "S : " + repr( self.you[0] )    + " " + repr( self.you[1] )    )
        print( "B : " + repr( self.box[0] )    + " " + repr( self.box[1] )    )
        print( "T : " + repr( self.target[0] ) + " " + repr( self.target[1] ) )
        print()

    
    def GoToPushBox( self, count, nowState, traceList ) :

        for a in range( 0, len( nowState.map ) ) :  # renew map
            for b in range( 0, len( nowState.map[a] ) ) :
                if nowState.map[a][b] == 'S' :
                    nowState.map[a] = nowState.map[a][:b] + '.' + nowState.map[a][b + 1:]
                elif nowState.map[a][b] == 'B' :
                    nowState.map[a] = nowState.map[a][:b] + '.' + nowState.map[a][b + 1:]

        nowState.map[nowState.you[0]] = nowState.map[nowState.you[0]][ : nowState.you[1]] + 'S' + nowState.map[nowState.you[0]][nowState.you[1] + 1 : ] # renew map
        nowState.map[nowState.box[0]] = nowState.map[nowState.box[0]][ : nowState.box[1]] + 'B' + nowState.map[nowState.box[0]][nowState.box[1] + 1 : ] # renew map
        traceList.append( nowState )

        # Success ~
        if nowState.box == self.target :
            if len( self.stateList ) == 0 or len( traceList ) < len( self.stateList ) :
                self.stateList = traceList[ : ]
                return True

        distance1 = abs( nowState.box[0] - self.target[0] ) + abs( nowState.box[1] - self.target[1] )
        # box's left and right == '.' or 'T'
        if nowState.box[1] >= 1                         and nowState.map[nowState.box[0]][nowState.box[1] - 1] == '.' or \
           nowState.box[1] + 1 < len( nowState.map[0] ) and nowState.map[nowState.box[0]][nowState.box[1] + 1] == '.' or \
           nowState.box[1] >= 1                         and nowState.map[nowState.box[0]][nowState.box[1] - 1] == 'T' or \
           nowState.box[1] + 1 < len( nowState.map[0] ) and nowState.map[nowState.box[0]][nowState.box[1] + 1] == 'T'    :

            boxLeft  = [nowState.box[0], nowState.box[1] - 1]
            boxRight = [nowState.box[0], nowState.box[1] + 1]

            if nowState.you == boxLeft : # push to right
                distance2 = abs( boxRight[0] - self.target[0] ) + abs( boxRight[1] - self.target[1] )
                nextState = State( nowState.box, boxRight, nowState.map[ : ] ) # ( you, box, map )

                if not Sokoban.TraceSame( self, nextState, traceList ) and distance1 > distance2 :
                    if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                        return True

            if nowState.you == boxRight : # push to left
                distance2 = abs( boxLeft[0] - self.target[0] ) + abs( boxLeft[1] - self.target[1] )
                nextState = State(  nowState.box, boxLeft, nowState.map[ : ] ) # ( you, box, map )

                if not Sokoban.TraceSame( self, nextState, traceList ) and distance1 > distance2 :
                    if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                        return True

        # box's up and down == '.' or 'T'
        if nowState.box[0] >= 1                      and nowState.map[nowState.box[0] - 1][nowState.box[1]] == '.' or \
           nowState.box[0] + 1 < len( nowState.map ) and nowState.map[nowState.box[0] + 1][nowState.box[1]] == '.' or \
           nowState.box[0] >= 1                      and nowState.map[nowState.box[0] - 1][nowState.box[1]] == 'T' or \
           nowState.box[0] + 1 < len( nowState.map ) and nowState.map[nowState.box[0] + 1][nowState.box[1]] == 'T'    :

            boxUp   = [nowState.box[0] - 1, nowState.box[1]]
            boxDown = [nowState.box[0] + 1, nowState.box[1]]

            if nowState.you == boxUp : # push to down
                distance2 = abs( boxDown[0] - self.target[0] ) + abs( boxDown[1] - self.target[1] )
                nextState = State( nowState.box, boxDown, nowState.map[ : ] ) # ( you, box, map )

                if not Sokoban.TraceSame( self, nextState, traceList ) and distance1 > distance2 :
                    if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                        return True

            if nowState.you == boxDown : # push to up
                distance2 = abs( boxUp[0] - self.target[0] ) + abs( boxUp[1] - self.target[1] )
                nextState = State( nowState.box, boxUp, nowState.map[ : ] ) # ( you, box, map )

                if not Sokoban.TraceSame( self, nextState, traceList ) and distance1 > distance2 :
                    if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                        return True


        distance1 = abs( nowState.box[0] - nowState.you[0] ) + abs( nowState.box[1] - nowState.you[1] )

        # your left == '.'
        if nowState.you[1] >= 1 and nowState.map[nowState.you[0]][nowState.you[1] - 1] == '.' :
            youLeft = [nowState.you[0], nowState.you[1] - 1]
            nextState = State( youLeft, nowState.box, nowState.map[ : ] ) # ( you, box, map )

            if not Sokoban.TraceSame( self, nextState, traceList ) :
                if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                    return True

        # your right == '.'
        if nowState.you[1] + 1 < len( nowState.map[0] ) and nowState.map[nowState.you[0]][nowState.you[1] + 1] == '.' :
            youRight = [nowState.you[0], nowState.you[1] + 1]
            nextState = State( youRight, nowState.box, nowState.map[ : ] ) # ( you, box, map )

            if not Sokoban.TraceSame( self, nextState, traceList ) :
                    if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                        return True

        # your up == '.'
        if nowState.you[0] >= 1 and nowState.map[nowState.you[0] - 1][nowState.you[1]] == '.' :
            youUp = [nowState.you[0] - 1, nowState.you[1]]
            nextState = State( youUp, nowState.box, nowState.map[ : ] ) # ( you, box, map )

            if not Sokoban.TraceSame( self, nextState, traceList ) :
                if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                    return True

        # your down == '.'
        if nowState.you[0] + 1 < len( nowState.map ) and nowState.map[nowState.you[0] + 1][nowState.you[1]] == '.' :
            youDown = [nowState.you[0] + 1, nowState.you[1]]
            nextState = State( youDown, nowState.box, nowState.map[ : ] ) # ( you, box, map )

            if not Sokoban.TraceSame( self, nextState, traceList ) :
                if Sokoban.GoToPushBox( self, count, nextState, traceList ) :
                    return True

        traceList.pop()


    def TraceSame( self, state, stateList ) :
        for stateInStateList in stateList :
            if stateInStateList.Same( state ) :
                return True

        return False


    def SetAnsList( self ) :

        for a in range( 0, len( self.stateList ) - 1 ) :
            if self.stateList[a].box[0] < self.stateList[a + 1].box[0] :
                self.ansList.append( "S" )
            elif self.stateList[a].box[0] > self.stateList[a + 1].box[0] :
                self.ansList.append( "N" )
            elif self.stateList[a].box[1] < self.stateList[a + 1].box[1] :
                self.ansList.append( "E" )
            elif self.stateList[a].box[1] > self.stateList[a + 1].box[1] :
                self.ansList.append( "W" )
            elif self.stateList[a].you[0] < self.stateList[a + 1].you[0] :
                self.ansList.append( "s" )
            elif self.stateList[a].you[0] > self.stateList[a + 1].you[0] :
                self.ansList.append( "n" )
            elif self.stateList[a].you[1] < self.stateList[a + 1].you[1] :
                self.ansList.append( "e" )
            elif self.stateList[a].you[1] > self.stateList[a + 1].you[1] :
                self.ansList.append( "w" )


        while ( 1 ) :
            find = False

            for a in range( 0, len( self.ansList ) - 2 ) :
                #print( "a = " + repr( a ) + ", len = " + repr( len( self.ansList ) - 2 ) )
                if a == len( self.ansList ) - 2 :
                    break

                if self.ansList[a] == 'e' and self.ansList[a + 1] == 'n' and self.ansList[a + 2] == 'w' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 'n'
                    find = True
                elif self.ansList[a] == 'w' and self.ansList[a + 1] == 'n' and self.ansList[a + 2] == 'w' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 'n'
                    find = True
                elif self.ansList[a] == 'E' and self.ansList[a + 1] == 'N' and self.ansList[a + 2] == 'W' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 'N'
                    find = True
                elif self.ansList[a] == 'W' and self.ansList[a + 1] == 'N' and self.ansList[a + 2] == 'E' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 'N'
                    find = True
                elif self.ansList[a] == 'e' and self.ansList[a + 1] == 's' and self.ansList[a + 2] == 'w' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 's'
                    find = True
                elif self.ansList[a] == 'w' and self.ansList[a + 1] == 's' and self.ansList[a + 2] == 'w' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 's'
                    find = True
                elif self.ansList[a] == 'E' and self.ansList[a + 1] == 'S' and self.ansList[a + 2] == 'W' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 'S'
                    find = True
                elif self.ansList[a] == 'W' and self.ansList[a + 1] == 'S' and self.ansList[a + 2] == 'E' :
                    self.ansList.pop(a + 1)
                    self.ansList.pop(a + 1)
                    self.ansList[a] = 'S'
                    find = True
            
            if not find :
                break
# ----------------------  End of Class Sokoban ---------------------------


count = 0
while ( 1 ) :
    r, c = map( int, input().split() )

    if r == 0 and c == 0 :
        break
    elif r > 20 or c > 20 :
        print( "Out of range !!" )
    elif r < 1 or c < 1 :
        print( "Find zero or negative number !!" )
    else :
        count += 1
        mapList = []
        mapError = False

        for a in range ( 1, r + 1 ) : # input map
            lineOfMap = input()

            if len( lineOfMap ) != c :
                mapError = True
            else :
                for ch in lineOfMap :
                    if ch != 'S' and ch != 'B' and ch != '.' and ch != 'T' and ch != '#' :
                        mapError = True
                mapList.append( lineOfMap )

        if not mapError :
            s = Sokoban( mapList )


        print( "\nMaze #" + repr( count ) )

        if mapError :
            print( "Map Error" + "\n" )
        else :
            traceList = []

            if s.GoToPushBox( 0, s.nowState, traceList ) :
                s.SetAnsList()

                for ch in s.ansList :
                    print( ch, end = '' )
                print("\n")

            else :
                print( "Impossible" + "\n" )

