# LFA-MEL-parser
Implementação de um parser descendente recursivo para uma Linguagem Livre de Contexto, chamada de MEL.

### Informações gerais
- **Autor**: Harã Heique dos Santos
- **Linguagem de programação**: Python (versão 3.6.7)
- **Ambiente de desenvolvimento**: Visual Studio Code (versão 1.33.1)

### Descrição geral do código fonte
O código fonte está estruturado da seguinte maneira:

![Code structure](https://raw.githubusercontent.com/HaraHeique/LFA-MEL-parser/master/images/Estrutura%20do%20src.png)

##### ParserMEL.py
É um módulo que contém uma classe única chamada `ParserMEL`, o qual representa o parser em si que é responsável por manipular as expressões matemáticas e encontrar o seu resultado.

```python
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
```
A parte do código acima contém o construtor da classe que contém a expressão de entrada(inputExpr), o símbolo corrente que está sendo lido(currentSymbol), a posição corrente(currentIndex) em que se encontra o símbolo e por fim o valor da expressão dada como entrada(expressionResult).

O trecho também mostra o único método público que a classe possui chamada `parseExpression`, o qual é chamado passando uma expressão matemática de entrada e resolvendo até achar um valor que é retornado ou ignorar a expressão por ela ser inválida.
Com a chamada desse método será invocada todas as outras funções da classe seguindo as regras de produção definidas para a gramática que é mostrada logo abaixo.

<p align="center">
  <img src="https://github.com/HaraHeique/LFA-MEL-parser/blob/master/images/Regra%20de%20produ%C3%A7%C3%A3o%20da%20gram%C3%A1tica%20MEL.png?raw=true">
</p>

##### build.py
É o módulo que é buildado e que contém a execução principal do programa, o qual utiliza o módulo `ParserMEL.py` que contém a classe do parser e instancia um objeto fazendo chamada o método `parseExpression` passando como argumento a expressão e recebendo um valor como resultado. Como se pode notar no trecho abaixo a expressão é digitada pelo usuário.

```python
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
```

### Como executar?
Para buildar/executar o app no ambiente Linux basta abrir o CLI(Command Line Interface) no diretório __/source__ e digitar o seguinte comando:
    
    python3 build.py

Neste comando como o SO é o Linux dist. Ubuntu 18.04 e já contém as versões ***2.7.15 e 3.6.7*** como default, o que torna fácil a execução de código utilizando esta linguagem. O outro comando seria a execução do arquivo .sh criado no mesmo diretório. Abaixo execute o mesmo comando que produzirá a mesma ação do primeiro comando mostrado acima:

    sh trab1.sh
    
### Informações adicionais
Todo o código fonte está hospedado no meu [GitHub](https://github.com/HaraHeique/LFA-MEL-parser).


