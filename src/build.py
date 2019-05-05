'''
    Responsável pela execução principal do programa
'''

from models.ParserMEL import ParserMEL

def main():
    parserMEL: ParserMEL = ParserMEL()

    while True:
        try:
            inputExpression: str = input("Enter your math expression: ")
            parserMEL.parseExpression(inputExpression)
            print("Expression result: {0} = {1}".format(parserMEL.expression, parserMEL.result))
        except Exception:
            print("Invalid input expression. Please check your expression and try again.")
        finally:
            # Somente para pular uma linha no terminal xD
            print()

    return 0

if __name__ == '__main__' :
    main()