This is a simple hack to illustrate Python's use of cores.

There are two files `use_multiprocessing.py` and
`use_threading.py`, which will be traced using `dstat`. Then
the output will be mangled into colored HTML to indicate the
usage of each core.

This was done on a 4-core machine with 8 virtual cores. Output was captured
via:

```
$ # 2 cores
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 12" dstat-multiproc-2.txt
$ # 4 cores
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 12" dstat-multiproc-4.txt
$ # 8 cores
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 16" dstat-multiproc-8.txt
```

You'll notice that 8 cores takes twice as long as 4 cores (i.e. there is no
speedup, the virtual cores are "fake").

During each of those captures, another shell was running:

```
$ # 2 cores
$ time python use_multiprocessing.py --num-procs 2
[36028796884746240, 36028796884746240]

real    0m6.236s
user    0m12.172s
sys     0m0.028s
$ # 4 cores
$ time python use_multiprocessing.py --num-procs 4
[36028796884746240, 36028796884746240, ...]

real    0m6.970s
user    0m25.728s
sys     0m0.048s
$ # 8 cores
$ time python use_multiprocessing.py --num-procs 8
[36028796884746240, 36028796884746240, ...]

real    0m12.169s
user    1m33.904s
sys     0m0.040s
```

## Output

![Using multiprocessing with 2 cores][multiproc2]

![Using multiprocessing with 4 cores][multiproc4]

![Using multiprocessing with 8 cores][multiproc8]

[multiproc2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-multiproc-2.png
[multiproc4]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-multiproc-4.png
[multiproc8]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-multiproc-8.png
