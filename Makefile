# Nome da biblioteca compartilhada a ser gerada (.so para Linux/macOS, .dll para Windows)
ifeq ($(OS),Windows_NT)
    LIB_NAME = libsimulation.dll
else
    LIB_NAME = libsimulation.so
endif

#compila a biblioteca C++
all: $(LIB_NAME)

#Regra para compilar a biblioteca
$(LIB_NAME): cpp_simulation/simulation.cpp
	@echo "Compilando a biblioteca C++: $(LIB_NAME)..."
	g++ -shared -fPIC -o $(LIB_NAME) cpp_simulation/simulation.cpp
	@echo "Compilação concluída."
# -shared cria uma biblioteca compartilhada (dinâmica), necessário para CDLL
# -fPIC gera "Position-Independent Code", necessário para bibliotecas compartilhadas

#Executa
run: $(LIB_NAME)
	@echo "Executando a aplicação Python..."
	python3 python_gui/main.py

#Limpa
clean:
	@echo "Limpando arquivos gerados..."
	rm -f $(LIB_NAME) *.o
	@echo "Limpeza concluída."

#Define 'all' como o alvo padrão a ser executado quando 'make' é chamado sem argumentos
.PHONY: all run clean