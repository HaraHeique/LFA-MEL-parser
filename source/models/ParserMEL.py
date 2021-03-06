# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o parser da expressão passada como entrada seguindo
    as regras definidas pela gramática da linguagem
'''

class ParserMEL:
    def __init__(self, inputExpr: str = None):
        self._inputExpr: str = inputExpr if (inputExpr != None) else None
        self._currentSymbol: str = ''
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
        self.__resetSymbol()
        self.__nextSymbol()
        self._expressionResult = self.__expr()

        # o currentSymbol não ficou no valor final que seria None, logo lança uma exceção
        if (self._currentSymbol != None):
            raise Exception("Something wrong happened. This is not a valid input expression.")

        return self._expressionResult

    # MÉTODOS PRIVADOS

    # Filtra espaços em branco, tabulações e afins da expressão de entrada
    def __filterInputExpression(self, inputExpr: str) -> None:
        self._inputExpr = "".join(inputExpr.split())

    # Reseta para o valor default tanto o currentSymbol quanto o currentIndex
    def __resetSymbol(self) -> None:
        self._currentIndex = 0
        self._currentSymbol = ''

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
            return baseValue ** (self.__factor())

        return baseValue

    # Regra: (‘+’ | ‘-’) <base> | <number> | ‘(’ <expr> ‘)’
    def __base(self) -> float:
        # (‘+’ | ‘-’) <base>
        plusMinusSymbols: tuple = ('+', '-')
        # Guarda o possível operador antes do símbolo corrente passar para o próximo símbolo
        baseOperator: str = self._currentSymbol
        if (self.__checkExpectedSymbols(plusMinusSymbols)):
            if (baseOperator == '+'):
                return self.__base()
            elif (baseOperator == '-'):
                return (-1) * self.__base()
            else:
                raise Exception("Invalid base calculation operator")

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
        plusMinusSymbols: tuple = ('+', '-')

        # (‘E’ | ‘e’)
        if (self.__checkExpectedSymbols(eulerSymbols)):
            # (‘+’ | ‘-’)?
            if (self.__checkExpectedSymbols(plusMinusSymbols)):
                pass

            # <digit>+
            self.__digit(True) # Válida somente para o primeiro dígito que é obrigatório

            # Para os demais dígitos opcionais
            while True:
                if (not self.__digit(False)):
                    break

        #Armazena o index final do number
        indexEnd: int = self._currentIndex - (1 if (self._currentSymbol != '//') else 2) if (self._currentIndex != 0) else len(self._inputExpr)

        return float(self._inputExpr[indexInit : indexEnd])

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
    parserMEL1: ParserMEL = ParserMEL("2E-1")
    print("Expression: {0} = {1}".format(parserMEL1.expression, parserMEL1.result))

    parserMEL: ParserMEL = ParserMEL()
    expressions: list = ["2 + 2",
                         "3 * 23",
                         "3 - 2 * 7",
                         "2 // 20",
                         "++++++2 - 4.0 / ----1.",
                         "34 + 213 + 2.12 / 21",
                         "10 * 5 + 100 / 10 - 5 + 7 % 2",
                         "(10) * 5 + (100 // 10) - 5 + (7 % 2)",
                         "-((2+2)*2)-((2-0)+2)",
                         "(2.*(2.0+2.))-(2.0+(2.-0))",
                         "-(100) + 21 / (43 % 2)",
                         "3^4+5*(2-5)",
                         "3^2+5//(2-5)",
                         "2^2^2^-2",
                         "0.02e2 + 0.02e-2",
                         "8^-2 + 2E1 * 2e-1 + 3e+3 / 2.012",
                         "8^2 + 2E1 * 2e-1 + 3e+3 // 2.",
                         "(-2.3)^2 + 2.2E1 * 2e-12 + 1e+3"]

    for expr in expressions:
        parserMEL.parseExpression(expr)
        print("Expression: {0} = {1}".format(parserMEL.expression, parserMEL.result))