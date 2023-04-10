# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系

import itertools
import random

listCardNum = []  # 四張牌列表
listCardSet = []  # 四個數所有排列組合列表
terminateList = [ 0, 0, 0, 0 ]
Card = ()  
listOperator = ["+", "-", "*", "/"]  
ansFormula = []  # All answer formula list
ansFormulaList = []  # Final answer output
processed = []
cardOne = 0
cardTwo = 0
cardThree = 0
cardFour = 0  # 四張牌的點數
parenState = { "+-+" : 3, "+--" : 3, "+-*" : 4, "+-/" : 4, "+*+" : 1, "+*-" : 1, "+**" : 2, "+*/" : 2, "+/+" : 1, "+/-" : 1, "+/*" : 1, "+//" : 2, 
              "--+" : 3, "---" : 3, "--*" : 4, "--/" : 4, "-*+" : 1, "-*-" : 1, "-**" : 2, "-*/" : 2, "-/+" : 4, "-/-" : 4, "-/*" : 2, "-//" : 2,
              "-+" : 3, "--" : 3, "*+" : 3, "*-" : 3, "/+" : 3, "/-" : 3, "/*" : 3,
              "-*" : 4, "-/" : 4, "**" : 4, "*/" : 4, "//" : 4 }
parenType = { 1 : "(%s%s%s)%s(%s%s%s)=24", 2 : "(%s%s%s)%s%s%s%s=24", 3 : "%s%s%s%s(%s%s%s)=24", 4 : "%s%s%s%s%s%s%s=24" }

def is_add_sub(operator) :
    if operator == '+' or operator == '-':
        return True
    else : return False

def is_multi_div(operator) :
    if operator == '*' or operator == '/' :
        return True
    else : return False


def card_permutation():  # User input 4 cards, and return all permutation lists of 4 cards.
    listCardNum = list(map(int,input().split()))
    inputCorrect = True 
    for i in listCardNum :
        if i > 13 or i < 1 : inputCorrect = False
    if (inputCorrect == False and listCardNum != terminateList) or len(listCardNum) != 4 :
        return False

    if listCardNum == terminateList :
        return listCardNum

    listCardSet = list(set(itertools.permutations(listCardNum, 4)))
    return listCardSet

def formula_process(case, card1, operator1 ,card2, operator2OR4, card3, operator3, card4) :
    processed = []
    if case == 1 :
        if is_multi_div( operator1 ) :
            if is_multi_div( operator2OR4 ) or (is_add_sub( operator2OR4 ) and is_add_sub( operator3 )):
                processed.append( "%s%s%s%s%s%s%s=24" % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4) )
            elif is_add_sub( operator2OR4 ) and is_multi_div( operator3 ) :
                processed.append("(%s%s%s%s%s)%s%s=24" % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))

        elif is_add_sub( operator1 ) :
            if is_multi_div( operator2OR4 ) :
                processed.append("(%s%s%s)%s%s%s%s=24" % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))
            elif is_add_sub( operator2OR4 ) and is_add_sub( operator3 ) :
                processed.append("%s%s%s%s%s%s%s=24" % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))
            elif is_add_sub( operator2OR4 ) and is_multi_div( operator3 ) :
                processed.append("(%s%s%s%s%s)%s%s=24" % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))

    elif case == 2 :
        if ( operator2OR4 == "+" ) :
            processed.append("%s%s%s%s%s%s%s=24" % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))
        elif ( is_multi_div( operator1 ) ) :
            opStr = operator2OR4 + operator3 
            state = parenState.get( opStr )
            processed.append( parenType.get(state) % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))
        else :
            opStr = operator1 + operator2OR4 + operator3 
            state = parenState.get( opStr )
            processed.append( parenType.get(state) % (card1, operator1 ,card2, operator2OR4, card3, operator3, card4))

    return processed

    


def card_calculate():  # return one of answer formulas
    ansFormula = []
    processed_formula = []
    for i in range(len(cardList)):
        Card = cardList[i]

        # 取得四張牌的點數
        card1 = Card[0]
        card2 = Card[1]
        card3 = Card[2]
        card4 = Card[3]

        getAnswer = False

        try:
            for operator1 in listOperator:
                result1 = 0  # 前兩張牌運算的結果
                if operator1 == "+" :
                    result1 = card1 + card2
                elif operator1 == "-":
                    result1 = card1 - card2
                elif operator1 == "*":
                    result1 = card1 * card2
                elif operator1 == "/":
                    result1 = card1 / card2

                for operator2 in listOperator:
                    result2 = 0  # 前三張牌運算的結果
                    if operator2 == "+" :
                        result2 = result1 + card3
                    elif operator2 == "-":
                        result2 = result1 - card3
                    elif operator2 == "*":
                        result2 = result1 * card3
                    elif operator2 == "/":
                        result2 = result1 / card3

                    for operator3 in listOperator:
                        result3 = 0 
                        result_lastTwoCards = 0  # 最後兩張牌的運算結果。有可能最終答案是後面兩張括號運算
                        if operator3 == "+":
                            result3 = result2 + card4
                            result_lastTwoCards = card3 + card4
                        elif operator3 == "-":
                            result3 = result2 - card4
                            result_lastTwoCards = card3 - card4
                        elif operator3 == "*":
                            result3 = result2 * card4
                            result_lastTwoCards = card3 * card4
                        elif operator3 == "/":
                            result3 = result2 / card4
                            result_lastTwoCards = card3 / card4
                        
                        # 判斷結果是否為24
                        if result3 == 24 :
                            processed_formula = formula_process( 1, card1, operator1 ,card2, operator2, card3, operator3, card4 )
                            ansFormula.append(processed_formula[0])
                            getAnswer = True

                        # 最後兩張牌括號運算
                        elif getAnswer == False :
                            for operator4 in listOperator :
                                result3 = 0

                                if operator4 == "+" :
                                    result3 = result1 + result_lastTwoCards
                                elif operator4 == "-":
                                    result3 = result1 - result_lastTwoCards
                                elif operator4 == "*":
                                    result3 = result1 * result_lastTwoCards
                                elif operator4 == "/":
                                    result3 = result1 / result_lastTwoCards

                                if result3 == 24 :
                                    processed_formula = formula_process( 2, card1, operator1 ,card2, operator4, card3, operator3, card4 )
                                    ansFormula.append(processed_formula[0])
                                    getAnswer = True
                                

                                if getAnswer :
                                    break
                        if getAnswer :
                            break
                    if getAnswer :
                        break
                if getAnswer :
                    break
        except ZeroDivisionError:
            pass

    cal = ansFormula

    list(set(ansFormula))  # 去除重複結果
    if len(ansFormula) == 0 : # Those cards cannot make up 24 
        ansFormula.append(0)

    return ansFormula[0]   # return one of the answers




cardList = card_permutation()  # 排列組合結果列表

while cardList != terminateList :
    if cardList == False:
        ansFormulaList.append("Input Error")
        cardList = card_permutation()

    elif card_calculate() == 0 :
        ansFormulaList.append("No Solution")
        cardList = card_permutation()
    else:
        ansFormulaList.append(card_calculate())
        cardList = card_permutation() 

for i in ansFormulaList :
    print(i)




