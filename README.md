This is a simple hack to illustrate Python's use of cores
with concurrent / parallel code. (The code here is CPU
intensive, not I/O intensive.)

There are two files `use_multiprocessing.py` and
`use_threading.py`, which will be traced using `dstat`. Then
the output will be mangled into colored HTML to indicate the
usage of each core.

This was done on a 4-core machine with 8 virtual cores.

## `multiprocessing` with 2 processes

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 12" dstat-multiproc-2.txt
```

![Using multiprocessing with 2 cores][multiproc2]

```
$ # Actual computation
$ time python2.7 use_multiprocessing.py --num-procs 2
[36028796884746240, 36028796884746240]

real    0m6.236s
user    0m12.172s
sys     0m0.028s
```

[multiproc2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-multiproc-2.png

## `multiprocessing` with 4 processes

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 12" dstat-multiproc-4.txt
```

![Using multiprocessing with 4 cores][multiproc4]

```
$ # Actual computation
$ time python2.7 use_multiprocessing.py --num-procs 4
[36028796884746240, 36028796884746240, ...]

real    0m6.970s
user    0m25.728s
sys     0m0.048s
```

[multiproc4]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-multiproc-4.png

## `multiprocessing` with 8 processes

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 16" dstat-multiproc-8.txt
```

![Using multiprocessing with 8 cores][multiproc8]

```
$ # Actual computation
$ time python2.7 use_multiprocessing.py --num-procs 8
[36028796884746240, 36028796884746240, ...]

real    0m12.169s
user    1m33.904s
sys     0m0.040s
```

[multiproc8]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-multiproc-8.png

## `threading` with 2 threads

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 10" dstat-threading-2.txt
```

![Using threading with 2 threads][threading2]

```
$ # Actual computation
$ time python2.7 use_threading.py --num-threads 2
2251799780130816
2251799780130816

real    0m5.586s
user    0m5.980s
sys     0m2.944s
```

[threading2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-threading-2.png

## `threading` with 4 threads

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 18" dstat-threading-4.txt
```

![Using threading with 4 threads][threading4]

```
$ # Actual computation
$ time python2.7 use_threading.py --num-threads 4
2251799780130816
2251799780130816
2251799780130816
2251799780130816

real    0m14.600s
user    0m20.820s
sys     0m13.280s
```

[threading4]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-threading-4.png

## `threading` with 8 threads

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 32" dstat-threading-8.txt
```

![Using threading with 8 threads][threading8]

```
$ # Actual computation
$ time python2.7 use_threading.py --num-threads 8
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816

real    0m27.663s
user    0m39.132s
sys     0m26.920s
```

[threading8]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-threading-8.png

## Non-Threaded

```
$ # Capture output
$ script -q -c "dstat -t -c -s -C 0,1,2,3,4,5,6,7 1 10" dstat-non-threaded.txt
```

![Do the computation without threading][non-threaded]

```
$ # Actual computation
$ time python non_threaded.py
36028796884746240

real    0m5.866s
user    0m5.792s
sys     0m0.024s
```

[non-threaded]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-non-threaded.png

## Baseline

Here is my machine when no Python process is running (but any background
is acceptable):

![Nothing running][nothing]

[nothing]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/dstat-nothing-running.png

## Discussion

With `multiprocessing`, there is near-perfect scaling until 4 cores. Then
8 cores takes twice as long as 4 cores (i.e. there is no speedup, the
virtual cores are "fake").

With `threading`, I am still not sure what I'm looking at.
