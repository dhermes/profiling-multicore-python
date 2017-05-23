import multiprocessing

import shared


def main():
    num_procs = shared.get_num_workers(
        'Run multiprocessing test.', 'num_procs')
    pool = multiprocessing.Pool(processes=num_procs)
    to_sum = 2**28
    inputs = [to_sum] * num_procs
    result = pool.map(shared.sumrange, inputs)
    print(result)


if __name__ == '__main__':
    main()
