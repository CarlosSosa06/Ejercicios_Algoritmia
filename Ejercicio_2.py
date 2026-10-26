import matplotlib.pyplot as plt
import os

def greedy_knapsack(items, values, weights, capacity, criterion="value_weight"):
    """
    Resuelve el problema de la mochila usando enfoques voraces (greedy).
    """
    n = len(items)
    indexed_items = [{
        'name': items[i],
        'value': values[i],
        'weight': weights[i],
        'ratio': values[i] / weights[i]
    } for i in range(n)]

    #Ordenamiento
    if criterion == "value_weight":
        indexed_items.sort(key=lambda x: x['ratio'], reverse=True)
    elif criterion == "min_weight":
        indexed_items.sort(key=lambda x: x['weight'])
        
    current_weight = 0
    total_value = 0
    chosen_items = []
    
    for item in indexed_items:
        if current_weight + item['weight'] <= capacity:
            current_weight += item['weight']
            total_value += item['value']
            chosen_items.append(item['name'])
            
    return chosen_items, current_weight, total_value

if __name__ == "__main__":
    items = ["Objeto A", "Objeto B", "Objeto C"]
    values = [100, 30, 30]
    weights = [40, 20, 20]
    capacity = 50

    chosen_vw, weight_vw, value_vw = greedy_knapsack(items, values, weights, capacity, criterion="value_weight")

    chosen_mw, weight_mw, value_mw = greedy_knapsack(items, values, weights, capacity, criterion="min_weight")

    print(f"{'Método Knapsack':<32} | {'Objetos':<15} | {'Capacidad':<10} | {'Valor Total':<12}")
    print("-" * 80)
    print(f"{'Valor / Peso (Estándar)':<32} | {str(chosen_vw):<15} | {weight_vw}/{capacity:<7} | {value_vw:<12}")
    print(f"{'Menor Peso Primero (Modificado)':<32} | {str(chosen_mw):<15} | {weight_mw}/{capacity:<7} | {value_mw:<12}")
    print("=" * 80)

    methods = ['Valor / Peso\n(Estándar)', 'Menor Peso Primero\n(Modificado)']
    total_values = [value_vw, value_mw]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(methods, total_values, color=['#2b5c8f', '#d9534f'], width=0.45)
    
    plt.title('Ejercicio 2: Comparativa de Valor Total en Greedy Knapsack', fontsize=12, fontweight='bold')
    plt.ylabel('Valor Total Obtenido', fontsize=10)
    plt.ylim(0, max(total_values) * 1.25)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f'Valor: {yval}', ha='center', va='bottom', fontweight='bold')

    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    os.makedirs('outputs/figures', exist_ok=True)
    
    plt.savefig('outputs/figures/ejercicio2_comparacion.png', dpi=300)
    print("Gráfica guardada exitosamente en 'outputs/figures/ejercicio2_comparacion.png'")
    plt.show()