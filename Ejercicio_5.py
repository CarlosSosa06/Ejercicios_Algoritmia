import math
import random
import itertools
import matplotlib.pyplot as plt
import os

def mst_prim(points):
    """Algoritmo de Prim desde la ciudad 0; retorna el árbol como {nodo: [hijos]}."""
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, len(points))}
    children = {v: [] for v in range(len(points))}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)
    return children

def preorder(children, root=0):
    """Recorrido en preorden del árbol; omitiendo visitas repetidas (shortcutting)."""
    return [root] + [c for child in children[root] for c in preorder(children, child)]

def tour_length(points, tour):
    """Calcula la longitud total de un recorrido cerrado."""
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def two_opt_search(initial_tour, points):
    """Aplica búsqueda local 2-opt como post-procesamiento."""
    tour = list(initial_tour)
    improved = True
    n = len(tour)
    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_tour = tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]
                if tour_length(points, new_tour) < tour_length(points, tour) - 1e-6:
                    tour = new_tour
                    improved = True
                    break
            if improved:
                break
    return tour

if __name__ == "__main__":
    num_instances = 100
    num_cities = 9
    
    ratios = []
    mst_costs = []
    mst_2opt_costs = []
    nn_2opt_costs = []
    
    print("Ejecutando 100 instancias para el Ejercicio 5 (MST Approximation)...")
    
    for seed in range(num_instances):
        random.seed(seed)
        points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(num_cities)]
        
        # Óptimo por fuerza bruta 
        optimal_tour = min(((0,) + p for p in itertools.permutations(range(1, len(points)))),
                          key=lambda t: tour_length(points, t))
        opt_cost = tour_length(points, optimal_tour)
        
        # Approximation Puro
        mst_tree = mst_prim(points)
        mst_tour = preorder(mst_tree)
        mst_cost = tour_length(points, mst_tour)
        mst_costs.append(mst_cost)
        
        # Razón de aproximación
        ratio = mst_cost / opt_cost
        ratios.append(ratio)
        mst_2opt_tour = two_opt_search(mst_tour, points)
        mst_2opt_costs.append(tour_length(points, mst_2opt_tour))
        unvisited = set(range(1, num_cities))
        current = 0
        nn_tour = [current]
        while unvisited:
            nxt = min(unvisited, key=lambda node: math.dist(points[current], points[node]))
            nn_tour.append(nxt)
            unvisited.remove(nxt)
            current = nxt
        nn_2opt = two_opt_search(nn_tour, points)
        nn_2opt_costs.append(tour_length(points, nn_2opt))

    avg_ratio = sum(ratios) / num_instances
    max_ratio = max(ratios)
    
    print(f"Razón promedio (MST / Opt):   {avg_ratio:.4f}")
    print(f"Razón máxima observada:       {max_ratio:.4f}  (Límite teórico: 2.0)")
    print(f"Costo promedio MST Puro:      {sum(mst_costs)/num_instances:.2f}")
    print(f"Costo promedio MST + 2-opt:   {sum(mst_2opt_costs)/num_instances:.2f}")
    print(f"Costo promedio NN + 2-opt:    {sum(nn_2opt_costs)/num_instances:.2f}")
    print("=" * 80)
    
    os.makedirs('outputs/figures', exist_ok=True)
    
    plt.figure(figsize=(8, 5))
    plt.hist(ratios, bins=15, color='#4b6584', edgecolor='black', alpha=0.8)
    plt.axvline(2.0, color='#eb4d4b', linestyle='--', linewidth=2, label='Límite Teórico (2.0)')
    plt.axvline(avg_ratio, color='#f0932b', linestyle='-', linewidth=2, label=f'Promedio Observado ({avg_ratio:.2f})')
    plt.title('Ejercicio 5: Distribución de la Razón de Aproximación (MST / Óptimo)', fontweight='bold')
    plt.xlabel('Razón de Aproximación ($C_{MST} / C_{opt}$)')
    plt.ylabel('Frecuencia (Instancias)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('outputs/figures/ejercicio5_razon_histograma.png', dpi=300)
    print("Gráfica 1 guardada en 'outputs/figures/ejercicio5_razon_histograma.png'")
    
    plt.figure(figsize=(8, 5))
    plt.boxplot([mst_costs, mst_2opt_costs, nn_2opt_costs], 
                patch_artist=True, 
                boxprops=dict(facecolor='#badc58'))
    plt.xticks([1, 2, 3], ['MST Puro', 'MST + 2-opt', 'Vecino Más Cercano + 2-opt'])
    plt.title('Ejercicio 5: Comparativa de Costo Total entre Métodos (100 Instancias)', fontweight='bold')
    plt.ylabel('Costo Total del Tour (Distancia)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('outputs/figures/ejercicio5_comparativa_costos.png', dpi=300)
    print("Gráfica 2 guardada en 'outputs/figures/ejercicio5_comparativa_costos.png'")
    
    plt.show()