import math
import random
import matplotlib.pyplot as plt
import os

def generate_random_cities(num_cities=20, seed=42):
    """Genera coordenadas aleatorias para las ciudades."""
    random.seed(seed)
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]

def tour_length(tour, cities):
    """Calcula la distancia total de un recorrido (tour)."""
    return sum(math.dist(cities[tour[i]], cities[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def nearest_neighbor_tour(cities, start_node=0):
    """Genera una solución inicial usando el heurístico del Vecino Más Cercano."""
    n = len(cities)
    unvisited = set(range(n))
    current = start_node
    tour = [current]
    unvisited.remove(current)
    
    while unvisited:
        nearest = None
        min_dist = float('inf')
        for node in unvisited:
            d = math.dist(cities[current], cities[node])
            if d < min_dist:
                min_dist = d
                nearest = node
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
        
    return tour

def random_tour(num_cities):
    """Genera una solución inicial aleatoria."""
    tour = list(range(num_cities))
    random.shuffle(tour)
    return tour

def two_opt_search(initial_tour, cities):
    """Aplica la heurística de búsqueda local 2-opt hasta alcanzar un óptimo local."""
    tour = list(initial_tour)
    improved = True
    improvements_count = 0
    n = len(tour)
    
    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_tour = tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]
                new_len = tour_length(new_tour, cities)
                
                # Si el nuevo tour es estrictamente mejor, se acepta
                if new_len < tour_length(tour, cities) - 1e-6:
                    tour = new_tour
                    improvements_count += 1
                    improved = True
                    break 
            if improved:
                break
                
    return tour, improvements_count, tour_length(tour, cities)

if __name__ == "__main__":
    num_cities = 20
    trials = 30 
    cities = generate_random_cities(num_cities, seed=42)
    
    random_improvements = []
    random_costs = []
    nn_improvements = []
    nn_costs = []
    
    print("Ejecutando experimentos para el Ejercicio 3 (2-opt TSP)...")
    
    for _ in range(trials):
        # Solución inicial aleatoria
        r_init = random_tour(num_cities)
        _, r_imp, r_cost = two_opt_search(r_init, cities)
        random_improvements.append(r_imp)
        random_costs.append(r_cost)
        
        # Solución inicial con Vecino Más Cercano
        start_node = random.randint(0, num_cities - 1)
        nn_init = nearest_neighbor_tour(cities, start_node)
        _, nn_imp, nn_cost = two_opt_search(nn_init, cities)
        nn_improvements.append(nn_imp)
        nn_costs.append(nn_cost)
        
    print(f"{'Escenario Inicial':<30} | {'Promedio de Mejoras':<20} | {'Promedio Costo Final':<20}")
    print("-" * 80)
    print(f"{'Aleatorio':<30} | {sum(random_improvements)/trials:<20.2f} | {sum(random_costs)/trials:<20.2f}")
    print(f"{'Vecino Más Cercano':<30} | {sum(nn_improvements)/trials:<20.2f} | {sum(nn_costs)/trials:<20.2f}")
    print("=" * 80)
    
    os.makedirs('outputs/figures', exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Ejercicio 3: Comparativa 2-opt en TSP (30 Instancias)', fontsize=14, fontweight='bold')
    
    axes[0].boxplot([random_improvements, nn_improvements], patch_artist=True, boxprops=dict(facecolor='#a8d0e6'))
    axes[0].set_title('Número de Mejoras hasta Óptimo Local', fontweight='bold')
    axes[0].set_ylabel('Cantidad de Intercambios (2-opt)')
    axes[0].set_xticks([1, 2])
    axes[0].set_xticklabels(['Aleatorio', 'Vecino Más Cercano'])
    axes[0].grid(True, linestyle='--', alpha=0.6)
    
    axes[1].boxplot([random_costs, nn_costs], patch_artist=True, boxprops=dict(facecolor='#f8b195'))
    axes[1].set_title('Calidad del Óptimo Local Alcanzado', fontweight='bold')
    axes[1].set_ylabel('Costo Total del Tour (Distancia)')
    axes[1].set_xticks([1, 2])
    axes[1].set_xticklabels(['Aleatorio', 'Vecino Más Cercano'])
    axes[1].grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('outputs/figures/ejercicio3_comparativa_completa.png', dpi=300)
    print("Gráfica doble guardada en 'outputs/figures/ejercicio3_comparativa_completa.png'")
    
    plt.show()