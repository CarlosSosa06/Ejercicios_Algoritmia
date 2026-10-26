import math
import random
import time
import matplotlib.pyplot as plt
import os

def generate_random_cities(num_cities=25, seed=42):
    """Genera coordenadas aleatorias para las ciudades."""
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]

def tour_length(tour, cities):
    """Calcula la distancia total de un recorrido (tour)."""
    return sum(math.dist(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def random_tour(num_cities):
    """Genera una solución inicial aleatoria."""
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

def random_two_opt_move(tour):
    """Aplica un movimiento 2-opt eligiendo un subsegmento al azar."""
    n = len(tour)
    i = random.randint(1, n - 2)
    k = random.randint(i + 1, n - 1)
    return tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]

def simulated_annealing(cities, schedule_type='exponential', max_iter=6000, t_init=100.0):
    """Implementa Recocido Simulado para el TSP con 2-opt."""
    n = len(cities)
    current_tour = random_tour(n)
    current_cost = tour_length(current_tour, cities)
    
    best_tour = list(current_tour)
    best_cost = current_cost
    
    T = t_init
    costs_history = []
    start_time = time.perf_counter()
    
    if schedule_type == 'exponential':
        alpha = 0.992  
    elif schedule_type == 'linear':
        beta = t_init / max_iter 
        
    for iteration in range(max_iter):
        if T <= 1e-4:
            break
            
        neighbor_tour = random_two_opt_move(current_tour)
        neighbor_cost = tour_length(neighbor_tour, cities)
        
        delta_e = neighbor_cost - current_cost
        
        if delta_e < 0 or random.random() < math.exp(-delta_e / T):
            current_tour = neighbor_tour
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_tour = list(current_tour)
                best_cost = current_cost
                
        costs_history.append(current_cost)
        
        if schedule_type == 'exponential':
            T *= alpha
        elif schedule_type == 'linear':
            T = max(0, T - beta)
            
    elapsed_time = time.perf_counter() - start_time
    return best_tour, best_cost, costs_history, elapsed_time

if __name__ == "__main__":
    num_cities = 25
    cities = generate_random_cities(num_cities, seed=42)
    
    print("Ejecutando experimentos para el Ejercicio 4 (Simulated Annealing)...")
    
    # Enfriamiento Exponencial
    best_exp_tour, best_exp_cost, history_exp, time_exp = simulated_annealing(
        cities, schedule_type='exponential', max_iter=6000, t_init=150.0
    )
    
    # Enfriamiento Lineal
    best_lin_tour, best_lin_cost, history_lin, time_lin = simulated_annealing(
        cities, schedule_type='linear', max_iter=6000, t_init=150.0
    )
   
    print(f"{'Esquema de Enfriamiento':<25} | {'Costo Final (Calidad)':<22} | {'Tiempo de Ejecución (s)':<22}")
    print("-" * 80)
    print(f"{'Exponencial':<25} | {best_exp_cost:<22.2f} | {time_exp:<22.4f}")
    print(f"{'Lineal':<25} | {best_lin_cost:<22.2f} | {time_lin:<22.4f}")
    print("=" * 80)
    
    os.makedirs('outputs/figures', exist_ok=True)
    
    plt.figure(figsize=(9, 5))
    plt.plot(history_exp, label='Exponencial (alpha=0.992)', color='#2b5c8f', linewidth=1.5)
    plt.plot(history_lin, label='Lineal (descenso constante)', color='#d9534f', linewidth=1.5, linestyle='--')
    plt.title('Ejercicio 4: Curvas de Convergencia (Simulated Annealing)', fontweight='bold')
    plt.xlabel('Iteraciones')
    plt.ylabel('Costo del Tour (Distancia)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('outputs/figures/ejercicio4_convergencia.png', dpi=300)
    print("Gráfica 1 guardada en 'outputs/figures/ejercicio4_convergencia.png'")
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    schedules = ['Exponencial', 'Lineal']
    costs = [best_exp_cost, best_lin_cost]
    times = [time_exp, time_lin]
    
    x = range(len(schedules))
    width = 0.35
    
    ax1.set_ylabel('Costo Final (menor es mejor)', color='#2b5c8f', fontweight='bold')
    bars1 = ax1.bar([p - width/2 for p in x], costs, width, label='Costo Final', color='#2b5c8f')
    ax1.tick_params(axis='y', labelcolor='#2b5c8f')
    ax1.set_xticks(x)
    ax1.set_xticklabels(schedules)
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Tiempo (s) (menor es mejor)', color='#d9534f', fontweight='bold')
    bars2 = ax2.bar([p + width/2 for p in x], times, width, label='Tiempo (s)', color='#d9534f', alpha=0.8)
    ax2.tick_params(axis='y', labelcolor='#d9534f')
    
    plt.title('Ejercicio 4: Comparativa de Calidad y Tiempo por Esquema', fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/figures/ejercicio4_tiempo_calidad.png', dpi=300)
    print("Gráfica 2 guardada en 'outputs/figures/ejercicio4_tiempo_calidad.png'")
    
    plt.show()