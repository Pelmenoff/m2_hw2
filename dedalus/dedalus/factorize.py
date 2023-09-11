import multiprocessing


def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def parallel_factorize(numbers):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    result = pool.map(factorize, numbers)
    pool.close()
    pool.join()
    return result   


def main():

    a1, b1, c1, d1 = factorize(128), factorize(255), factorize(99999), factorize(10651060)

    print(f"Factorize: {a1} | {b1} | {c1} | {d1}")

    a2, b2, c2, d2 = parallel_factorize([128, 255, 99999, 10651060])

    print(f"Parralel: {a1} | {b1} | {c1} | {d1}")



if __name__ == "__main__":
    main()