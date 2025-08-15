# Simulação de Partículas com Python e C++

Este projeto é um trabalho acadêmico que demonstra a integração de duas linguagens de programação com vocações distintas: Python para a interface gráfica e C++ para cálculos de alta performance.

A aplicação implementada é uma simulação 2D de partículas que se movem e colidem com as paredes de uma caixa. A lógica de atualização da física (cálculo de posição e velocidade) é inteiramente feita em C++, enquanto a janela, a renderização e o controle do loop de animação são gerenciados pelo Python.

## Estrutura do Repositório

- **`README.md`**: Este arquivo.
- **`Makefile`**: Arquivo para automatizar a compilação e execução.
- **`cpp_simulation/`**: Contém o código-fonte da simulação em C++.
  - `particle.hpp`: Define a estrutura de dados de uma partícula.
  - `simulation.cpp`: Implementa a lógica da simulação e exporta as funções para o Python.
- **`python_gui/`**: Contém o código da interface gráfica em Python.
  - `main.py`: Script principal que cria a janela, carrega a biblioteca C++ e gerencia a animação.

## Dependências

Para compilar e executar este projeto, você precisará de:

1.  **Compilador C++**: `g++` (geralmente incluído no pacote `build-essential` em sistemas baseados em Debian/Ubuntu).
2.  **Python 3**: A linguagem de script para a interface.
3.  **Tkinter**: A biblioteca gráfica padrão do Python. Caso contrário seja necessário, instale-a:
    - Em Debian/Ubuntu: `sudo apt-get install python3-tk`
    - Em Fedora: `sudo dnf install python3-tkinter`

## Como Compilar

O `Makefile` automatiza o processo de compilação. Ele irá compilar o código C++ em uma **biblioteca compartilhada** (`libsimulation.so` em Linux ou `libsimulation.dll` em Windows).

Abra um terminal na raiz do repositório e execute:

```
make
```

## Como Executar

Após a compilação bem-sucedida, você pode executar o programa usando o `Makefile`. Este comando iniciará a aplicação gráfica em Python, que por sua vez carregará e utilizará a biblioteca C++ recém-compilada.

```
make run
```

Uma janela preta deverá aparecer com 500 partículas ciano se movendo.

## Limpeza

Para remover os arquivos gerados pela compilação, execute:

```
make clean
```