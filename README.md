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
3.  **Tkinter**: A biblioteca gráfica padrão do Python. Na maioria das vezes já vem instalada. Caso contrário, instale-a:
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

## Explicação da Interface entre Linguagens

Interface de Função Externa (FFI) via **`ctypes`**
A forma mais elegante e eficiente de fazer Python e C++ conversarem neste cenário é compilando o código C++ como uma biblioteca compartilhada (.so no Linux/macOS ou .dll no Windows) e carregando-a no Python usando a biblioteca padrão ctypes.

1.  **Exportação em C++**: O código C++ é compilado como uma biblioteca compartilhada. Funções que precisam ser acessíveis pelo Python são declaradas com `extern "C"`. Isso impede que o compilador C++ altere os nomes das funções (um processo chamado *name mangling*), garantindo que o Python possa encontrá-las pelos seus nomes originais.

2.  **Carregamento em Python**: O script Python (`main.py`) usa `ctypes.CDLL()` para carregar a biblioteca `libsimulation.so` em tempo de execução.

3.  **Definição de Tipos**: Python não conhece as estruturas de dados do C++. Por isso, criamos uma classe `Particle(ctypes.Structure)` que espelha exatamente a `struct Particle` do C++. Também configuramos os tipos de argumentos (`.argtypes`) e o tipo de retorno (`.restype`) para cada função C++ importada. Isso garante a correta passagem de dados (inteiros, doubles, ponteiros).

4.  **Fluxo de Dados**:
    - O Python chama `simulation_init()` para que o C++ aloque a memória e inicialize as partículas.
    - Em um loop contínuo, o Python chama `simulation_update()`, passando o tempo decorrido. O C++ realiza todos os cálculos de física.
    - Imediatamente depois, o Python chama `simulation_get_particles()`, que retorna um **ponteiro** para o array de partículas no lado C++.
    - O Python lê os dados de posição (`x`, `y`) diretamente da memória C++ através do ponteiro e atualiza as coordenadas dos círculos na tela do Tkinter.