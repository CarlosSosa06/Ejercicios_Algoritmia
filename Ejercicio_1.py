import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt

def monte_carlo_pi_chunk(num_samples):
    inside = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1.0:
            inside += 1
    return inside

def estimate_pi_parallel(total_samples, num_processes):
    chunk_size = total_samples // num_processes
    start_time = time.time()
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(monte_carlo_pi_chunk, [chunk_size] * num_processes)
        
    total_inside = sum(results)
    elapsed_time = time.time() - start_time
    pi_estimate = 4 * total_inside / total_samples
    return pi_estimate, elapsed_time

if __name__ == '__main__':
    total_samples = 10000000
    processes_list = [1, 2, 4, 8]
    
    speedups = []
    baseline_time = None
    
    print("--- Resultados: Aceleración Paralela (Monte Carlo Pi) ---")
    for p in processes_list:
        pi_val, elapsed = estimate_pi_parallel(total_samples, p)
        
        if p == 1:
            baseline_time = elapsed 
            
        speedup = baseline_time / elapsed
        speedups.append(speedup)
        
        print(f"[{p} proceso(s)] Tiempo: {elapsed:.4f} s | Pi: {pi_val:.5f} | Speedup: {speedup:.2f}x")

    plt.figure(figsize=(8, 5))
    plt.plot(processes_list, speedups, marker='o', label='Speedup Real', color='royalblue', linewidth=2)
    plt.plot(processes_list, processes_list, linestyle='--', color='gray', label='Speedup Ideal (y = x)')
    
    plt.title('Ejercicio 1: Aceleración Paralela (Monte Carlo Pi)')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Speedup (S = T1 / TN)')
    plt.xticks(processes_list)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()