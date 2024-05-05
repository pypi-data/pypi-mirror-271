# pypl4

O pacote pypl4 foi desenvolvido para auxiliar pesquisadores da área de sistemas elétricos de potência a manipular arquivos com extensão PL4 gerados pelo software ATP (Alternative Transients Program). O pacote foi desenvolvido com base no código disponível no [link](https://github.com/ldemattos/readPL4/tree/master).


## Instalação

Para instalar o pacote você pode utilizar o comando:


```bash
pip install pypl4
```

## Como usar

O pacote pypl permite ler arquivos .pl4 e selecionar as oscilografias registradas nele. Para ler o arquivo .pl4 basta importar o pacote no projeto e executar a função readPL4.

```bash
from pypl4.readPL4 import readPL4

pl4 = readPL4('arquivo.pl4')
```


O objeto pl4 possui métodos que permitem acessar diferentes dados do arquivo. São eles:

* pl4.getFromNode(): retorna uma lista com os nós de saída dos ramos presentes no arquivo;

* pl4.getToNode(): retorna uma lista com os nós de chegada dos ramos presentes no arquivo;

* pl4.getTypeSignal(): retorna uma lista com os tipos desinais presentes no arquivo. Podem ser sinais de tensão, corrente ou lógicos;

* pl4.getDeltaTfromSimulation(): retorna o passo de integração utilizado na simulação;

* pl4.getDeltaTfromPlot(): retorna o passo de integração salvo no plot;

* pl4.getSteps(): retorna a quantidade de pontos do sinal;

* pl4.getTmax(): retorna o tempo total da simulação;

* pl4.getVarData(Type, From, To): recebe o tipo do sinal, o nó de saída e o nó de chegada do ramo e retorna uma oscilografia.


Exemplo de uso 1:

```bash
voltage = pl4.getVarData('V-node', 'BUS3B', '')

```

O exemplo retorna a oscilografia da tensão no nó BUS3B presente no arquivo.


Exemplo de uso 2:

```bash
corrente = pl4.getVarData('I-bran', 'BUS3B', 'BUS4B')
```

O exemplo retorna a oscilografia da corrente entre os nós BUS3B e BUS4B.