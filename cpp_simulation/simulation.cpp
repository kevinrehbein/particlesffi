#include "particula.hpp"
#include <vector>
#include <cstdlib> 
#include <ctime> 
#include <cmath>

std::vector<Particula> particulas;

extern "C" {

    void simulation_init(int num_particulas, int WIDTH, int HEIGHT) {
        srand(time(NULL));
        particulas.clear(); // Limpa partículas de uma simulação anterior
        
        for (int i = 0; i < num_particulas; ++i) {
            Particula p = {
                // posição aleatória dentro da tela
                (float)(rand() % WIDTH),
                (float)(rand() % HEIGHT),
                // Velocidade aleatória entre -100 e +100
                (float)((rand() % 200) - 100),
                (float)((rand() % 200) - 100)
            };
            particulas.push_back(p);
        }
    }

    void simulation_update(double tempoVariacao, int WIDTH, int HEIGHT, float PARTICULA_RAIO) {
        
        // Laço aninhado para verificar cada par de partículas uma única vez
        for (size_t i = 0; i < particulas.size(); ++i) {
            for (size_t j = i + 1; j < particulas.size(); ++j) {
                
                //1. DETECÇÃO DE COLISÃO
                auto& p1 = particulas[i];
                auto& p2 = particulas[j];

                float dx = p2.x - p1.x;
                float dy = p2.y - p1.y;
                float dist_sq = dx * dx + dy * dy;

                if (dist_sq < (2 * PARTICULA_RAIO) * (2 * PARTICULA_RAIO)) {
                    
                    //2. RESOLUÇÃO DA COLISÃO (A FÍSICA)
                    float distancia = sqrt(dist_sq);
                    
                    if (distancia != 0) {

                        float normal_x = dx / distancia;
                        float normal_y = dy / distancia;

                        float tangente_x = -normal_y;
                        float tangente_y = normal_x;

                        float v1n = p1.vx * normal_x + p1.vy * normal_y;
                        float v1t = p1.vx * tangente_x + p1.vy * tangente_y;
                        
                        float v2n = p2.vx * normal_x + p2.vy * normal_y;
                        float v2t = p2.vx * tangente_x + p2.vy * tangente_y;

                        float v1n_final = v2n;
                        float v2n_final = v1n;

                        p1.vx = (v1n_final * normal_x) + (v1t * tangente_x);
                        p1.vy = (v1n_final * normal_y) + (v1t * tangente_y);

                        p2.vx = (v2n_final * normal_x) + (v2t * tangente_x);
                        p2.vy = (v2n_final * normal_y) + (v2t * tangente_y);

                        float overlap = 0.5 * (2 * PARTICULA_RAIO - distancia);
                        p1.x -= overlap * normal_x;
                        p1.y -= overlap * normal_y;
                        p2.x += overlap * normal_x;
                        p2.y += overlap * normal_y;
                    }
                }
            }
        }
        
        for (auto& p : particulas) {
            p.x += p.vx * tempoVariacao;
            p.y += p.vy * tempoVariacao;

            //Se atingir uma borda, inverte a velocidade
            if (p.x < 0 || p.x > WIDTH) {
                p.vx *= -1;
            }
            if (p.y < 0 || p.y > HEIGHT) {
                p.vy *= -1;
            }
        }
    }

    Particula* get_particulas_data() {
        return particulas.data();
    }
}