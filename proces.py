import time
import multiprocessing

def factorize(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors

def factorize_parallel(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.map(factorize, numbers)
    return result

if __name__ == "__main__":
    input_numbers = [128, 255, 99999, 10651060]


    start_time_single = time.time()
    factors_list_single = [factorize(num) for num in input_numbers]
    end_time_single = time.time()

    for i, num in enumerate(input_numbers):
        print(f"Factors of {num} (single): {factors_list_single[i]}")

    elapsed_time_single = end_time_single - start_time_single
    print(f"Total time taken (single): {elapsed_time_single:.6f} seconds")

  
    start_time_parallel = time.time()
    factors_list_parallel = factorize_parallel(input_numbers)
    end_time_parallel = time.time()

    for i, num in enumerate(input_numbers):
        print(f"Factors of {num} (parallel): {factors_list_parallel[i]}")

    elapsed_time_parallel = end_time_parallel - start_time_parallel
    print(f"Total time taken (parallel): {elapsed_time_parallel:.6f} seconds")
