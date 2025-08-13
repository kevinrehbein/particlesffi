import ctypes
import tkinter as tk
import os

NUM_PARTICULAS = 500
PARTICULA_RAIO = 3.0
WIDTH = 800
HEIGHT = 600
INTERVALO_ATUALIZACAO_MS = 16   # A cada 16ms, teremos aproximadamente 60 fps

class Particula(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("vx", ctypes.c_double),
                ("vy", ctypes.c_double)]

def load_cpp_library():
    
    lib_name = 'libsimulation.so'
    if os.name == 'nt':
        lib_name = 'libsimulation.dll'  #se o sistema for Windows, o nome da biblioteca é .dll
    
    lib_path = os.path.join(os.path.dirname(__file__), '..', lib_name)
    
    try:
        return ctypes.CDLL(lib_path)    #função para abrir biblioteca compartilha em C
    except OSError as e:
        print(f"Erro: Não foi possível carregar a biblioteca '{lib_path}'")
        print("Você executou o comando 'make' para compilá-la primeiro?")
        exit()

def setup_library_functions(lib):        #Configura os tipos de argumentos e retorno das funções C++
    
    # void simulation_init
    lib.simulation_init.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
    lib.simulation_init.restype = None

    # void simulation_update
    lib.simulation_update.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.c_float]
    lib.simulation_update.restype = None

    # particula* get_particulas_data
    lib.get_particulas_data.argtypes = []
    lib.get_particulas_data.restype = ctypes.POINTER(Particula)

def animate():

    #Pede para a biblioteca C++ calcular o próximo quadro
    lib.simulation_update(0.016, WIDTH, HEIGHT, PARTICULA_RAIO)
    
    #Pega o endereço de memória do array de partículas atualizado
    particulas_ptr = lib.get_particulas_data()
    
    for i in range(NUM_PARTICULAS):
        particula_data = particulas_ptr[i]
        
        x0 = particula_data.x - PARTICULA_RAIO
        y0 = particula_data.y - PARTICULA_RAIO
        x1 = particula_data.x + PARTICULA_RAIO
        y1 = particula_data.y + PARTICULA_RAIO
        canvas.coords(particula_shapes[i], x0, y0, x1, y1)
        
    # Agenda a próxima chamada desta mesma função
    window.after(INTERVALO_ATUALIZACAO_MS, animate)


#Fluxo Principal de Execução

lib = load_cpp_library()
setup_library_functions(lib)
window = tk.Tk()
window.title("Simulação de Partículas (Python + C++)")
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

#Inicializa a simulação no C++
lib.simulation_init(NUM_PARTICULAS, WIDTH, HEIGHT)

#Cria uma forma de círculo no canvas para cada partícula
particula_shapes = []
for _ in range(NUM_PARTICULAS):
    shape = canvas.create_oval(-10, -10, -10, -10, fill="cyan", outline="") #cria círculos fora da tela, eles serão movidos para o lugar certo
    particula_shapes.append(shape)

animate()
window.mainloop()