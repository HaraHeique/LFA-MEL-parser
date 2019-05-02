# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o parser da expressão passada como entrada seguindo
    as regras definidas pela gramática da linguagem
'''

class ParserMEL:
    def __init__(self, inputExpr: str = None):
        self._inputExpr: str = inputExpr if (inputExpr != None) else None
        self._currentSymbol: str
        self._currentIndex: int = 0
        self._expressionResult: float = self.parseExpression(self._inputExpr) if (self._inputExpr != None) else 0.0
    
    @property
    def expression(self) -> str:
        return self._inputExpr

    @property
    def result(self) -> float:
        return self._expressionResult

    # Faz o parse da expressão passada como argumento
    def parseExpression(self, inputExpr: str) -> float:
        self.__filterInputExpression(inputExpr)
        self.__nextSymbol()

        return 0.0


    # MÉTODOS PRIVADOS

    # Filtra espaços em branco, tabulações e afins da expressão de entrada
    def __filterInputExpression(self, inputExpr: str) -> None:
        self._inputExpr = "".join(inputExpr.split())

    # Seta o próximo símbolo em __currentSymbol que é o caractere da indice corrente do objeto
    def __nextSymbol(self) -> None:
        if (self.__readAllSymbols()):
            self._currentIndex = -1
        else:
            self._currentSymbol = self._inputExpr[self._currentIndex]
            self._currentIndex += 1

    # Checa se todas os símbolos da Input Expression foi lido
    def __readAllSymbols(self):
        return self._currentIndex >= len(self._inputExpr)

    # Checa se o símbolo corrente é o mesmo que o símbolo esperado naquele momento do parser e passa para próximo símbolo
    def __expectSymbol(self, expectSymbol: str) -> bool:
        isExpected: bool = self._currentSymbol == expectSymbol
        if (isExpected): self.__nextSymbol()
        return isExpected

    # Métodos dos símbolos não-terminais    
    def __expr(self) -> None:
        self.__term()
        self.__severalTerms()

    def __term(self) -> None:
        self.__factor()
        self.__severalFactors()
    
    # Regra: <base> (‘^’ <factor>)?
    def __factor(self):
        self.__base()

        # É opcional
        if (self.__expectSymbol('^')):
            self.__factor()

    # Regra: (‘+’ | ‘-’) <base> | <number> | ‘(’ <expr> ‘)’
    def __base(self):
        # (‘+’ | ‘-’) <base>
        if (self.__checkExpectedSymbols(('+', '-'))):
            self.__base()
            return

        # <number>
        if (self.__number()):
            return
        
        # ‘(’ <expr> ‘)’
        if (self.__expectSymbol('(')):
            self.__expr()
            if (self.__expectSymbol(')')):
                return

        raise Exception("Error: Unexpected base symbol. Please check your expression!")

    def __number(self):
        pass
    
    def __digit(self):
        pass

    def __severalTerms(self):
        pass

    def __severalFactors(self):
        pass

    # Checa um conjunto de símbolos terminais para checar se ele é o esperado
    def __checkExpectedSymbols(self, expectSymbols: tuple):
        for exp in expectSymbols:
            if self.__expectSymbol(exp): 
                return True
        return False


# Para testes unitário do módulo
if __name__ == '__main__' :
    #parserMEL: ParserMEL = ParserMEL("32.4 % 32 / 2")
    parserMEL: ParserMEL = ParserMEL()
    parserMEL.parseExpression("34 + 213 + 2.12 / 21")
    print("Expression: {0} = {1}".format(parserMEL.expression, parserMEL.result))