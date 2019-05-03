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
        self.__expr()

        # o currentSymbol não ficou no valor final que seria None, logo lança uma exceção
        if (self._currentSymbol != None):
            raise Exception("Something wrong happened. This is not a valid input expression.")

        return 0.0

    # MÉTODOS PRIVADOS

    # Filtra espaços em branco, tabulações e afins da expressão de entrada
    def __filterInputExpression(self, inputExpr: str) -> None:
        self._inputExpr = "".join(inputExpr.split())

    # Seta o próximo símbolo em __currentSymbol que é o caractere da indice corrente do objeto
    def __nextSymbol(self) -> None:
        if (self.__readAllSymbols()):
            self._currentSymbol = None
            self._currentIndex = 0
        else:
            self._currentSymbol = self._inputExpr[self._currentIndex]
            self._currentIndex += 1
            self.__checkExpectSymbolDividBy()

    # Checa se todas os símbolos da Input Expression foi lido
    def __readAllSymbols(self) -> bool:
        return self._currentIndex >= len(self._inputExpr)

    # Checa se o símbolo corrente é o mesmo que o símbolo esperado naquele momento do parser e passa para próximo símbolo
    def __expectSymbol(self, expectSymbol: str) -> bool:
        isExpected: bool = self._currentSymbol == expectSymbol
        if (isExpected): self.__nextSymbol()
        return isExpected

    # Checa um conjunto para dois ou mais símbolos terminais para checar se ele é o esperado
    def __checkExpectedSymbols(self, expectSymbols: tuple) -> bool:
        for exp in expectSymbols:
            if self.__expectSymbol(exp):
                return True
        return False

    # Em caso do símbolo que pode ser '/' ou '//'
    def __checkExpectSymbolDividBy(self) -> None:
        # Checa se o próximo símbolo é um '/' também, pois caso seja estamos lidando com um '//'
        if (self._currentSymbol == '/') and (self._inputExpr[self._currentIndex] == '/'):
            self._currentSymbol = '//'
            self._currentIndex += 1
            
    # Métodos dos símbolos não-terminais 
    
    # Regra: <term> ((‘+’ | ‘-’) <term>)*
    def __expr(self) -> float:
        # <term>
        leftTermValue: float = self.__term()

        # ((‘+’ | ‘-’) <term>)*
        termSymbols: tuple = ('+', '-')
        while True:
            # Guarda o possível operador antes do símbolo corrente passar para o próximo símbolo
            termOperator: str = self._currentSymbol

            if (self.__checkExpectedSymbols(termSymbols)):
                rightTermValue: float = self.__term()

                if (termOperator == '+'):
                    leftTermValue += rightTermValue
                elif (termOperator == '-'):
                    leftTermValue -= rightTermValue
                else:
                    raise Exception("Invalid term calculation operator")
            else:
                break
        
        return leftTermValue

    # Regra: <factor> ((‘*’ | ‘/’ | ‘//’ | ‘%’) <factor>)*
    def __term(self) -> float:
        # <factor>
        leftFactorValue: float = self.__factor()

        # ((‘*’ | ‘/’ | ‘//’ | ‘%’) <factor>)*
        factorSymbols: tuple = ('*', '/', '//', '%')
        while True:
            # Guarda o possível operador antes do símbolo corrente passar para o próximo símbolo
            factorOperator: str = self._currentSymbol

            if (self.__checkExpectedSymbols(factorSymbols)):
                rightFactorValue: float = self.__factor()

                if (factorOperator == '*'):
                    leftFactorValue *= rightFactorValue
                elif (factorOperator == '/'):
                    leftFactorValue /= rightFactorValue
                elif (factorOperator == '//'):
                    leftFactorValue //= rightFactorValue
                elif (factorOperator == '%'):
                    leftFactorValue %= rightFactorValue
                else:
                    raise Exception("Invalid factor calculation operator")
            else:
                break
        
        return leftFactorValue
    
    # Regra: <base> (‘^’ <factor>)?
    def __factor(self) -> float:
        # <base>
        baseValue: float = self.__base()

        # (‘^’ <factor>)?
        if (self.__expectSymbol('^')):
            return self.__factor()

        return baseValue

    # Regra: (‘+’ | ‘-’) <base> | <number> | ‘(’ <expr> ‘)’
    def __base(self) -> float:
        # (‘+’ | ‘-’) <base>
        addSubSymbols: tuple = ('+', '-')
        if (self.__checkExpectedSymbols(addSubSymbols)):
            return self.__base()

        # ‘(’ <expr> ‘)’
        if (self.__expectSymbol('(')):
            exprValue: float = self.__expr()
            if (self.__expectSymbol(')')):
                return exprValue

        # <number>
        return self.__number()

        #raise Exception("Error. Unexpected base symbol. Please check your expression!")

    # Regra: <digit>+ ‘.’? <digit>* ((‘E’ | ‘e’)(‘+’ | ‘-’)? <digit>+)?
    def __number(self) -> float:
        # Armazena o index inicial do number
        indexInit: int = self._currentIndex - 1

        # <digit>+
        self.__digit(True)

        # Para os demais dígitos opcionais
        while True:
            if (not self.__digit(False)):
                break
        
        # ‘.’? <digit>*
        if (self.__expectSymbol('.')):
            # <digit>* - Para dígitos opcionais
            while True:
                if (not self.__digit(False)):
                    break

        # ((‘E’ | ‘e’)(‘+’ | ‘-’)? <digit>+)?
        eulerSymbols: tuple = ('E', 'e')
        addSubSymbols: tuple = ('+', '-')

        # (‘E’ | ‘e’)
        if (self.__checkExpectedSymbols(eulerSymbols)):
            # (‘+’ | ‘-’)?
            if (self.__checkExpectedSymbols(addSubSymbols)):
                pass

            # <digit>+
            self.__digit(True) # Válida somente para o primeiro dígito que é obrigatório

            # Para os demais dígitos opcionais
            while True:
                if (not self.__digit(False)):
                    break

        return float(self._inputExpr[indexInit:self._currentIndex])
    
    # Regra: ‘0’ | ‘1’ | ‘2’ | ‘3’ | ‘4’ | ‘5’ | ‘6’ | ‘7’ | ‘8’ | ‘9’
    def __digit(self, isRequired: bool) -> bool:
        validDigits: tuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        if (self.__checkExpectedSymbols(validDigits)):
            return True

        # Caso seja um dígito requerido e não consegue identificá-lo como esperado então é uma exception
        if (isRequired):
            raise Exception("Error. Unexpected digit symbol. Please check your expression!")
        
        return False


# Para testes unitário do módulo
if __name__ == '__main__' :
    #parserMEL: ParserMEL = ParserMEL("32.4 % 32 / 2")
    parserMEL: ParserMEL = ParserMEL()
    expressions: list = ["34 + 213 + 2.12 / 21",
                         "10 * 5 + 100 / 10 - 5 + 7 % 2",
                         "(10) * 5)) + (100 // 10)( - 5 + (7 % 2)",
                         "(34) + 21 // (43 % 2)",
                         "((3) - 32",
                         "3^2+5*(2-5)",
                         "3^2+5(2-5)",
                         "8^-2 + 2E1 * 2e-1 + 3e+3 // 2.012",
                         "8^2 + 2E1 * 2e-1 + 3e+3 // 2."]
    parserMEL.parseExpression(expressions[8])
    print("Expression: {0} = {1}".format(parserMEL.expression, parserMEL.result))