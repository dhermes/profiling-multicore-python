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
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename profile-multiproc-2.png \
>   --script use_multiprocessing.py \
>   --num-procs 2 \
>   --data-id multiprocessing:2
[36028796884746240, 36028796884746240]
Saved profile-multiproc-2.png
```

![Using multiprocessing with 2 cores][multiproc2]

[multiproc2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-multiproc-2.png

## `multiprocessing` with 4 processes

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename profile-multiproc-4.png \
>   --script use_multiprocessing.py \
>   --num-procs 4 \
>   --data-id multiprocessing:4
[36028796884746240, 36028796884746240, 36028796884746240, 36028796884746240]
Saved profile-multiproc-4.png
```

![Using multiprocessing with 4 cores][multiproc4]

[multiproc4]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-multiproc-4.png

## `multiprocessing` with 8 processes

```
$ python watch_cpu.py \
>   --total-intervals 19 \
>   --filename profile-multiproc-8.png \
>   --script use_multiprocessing.py \
>   --num-procs 8 \
>   --data-id multiprocessing:8
[36028796884746240, 36028796884746240, ...]
Saved profile-multiproc-8.png
```

![Using multiprocessing with 8 cores][multiproc8]

[multiproc8]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-multiproc-8.png

## `threading` with 2 threads

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename profile-threading-2.png \
>   --script use_threading.py \
>   --num-threads 2 \
>   --data-id threading:2
2251799780130816
2251799780130816
Saved profile-threading-2.png
```

![Using threading with 2 threads][threading2]

[threading2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-threading-2.png

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
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename profile-non-threaded.png \
>   --script non_threaded.py \
>   --data-id non-threaded:1
36028796884746240
Saved profile-non-threaded.png
```

![Do the computation without threading][non-threaded]

[non-threaded]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-non-threaded.png

## Baseline

Here is my machine when no Python process is running (but any background
is acceptable):

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename profile-nothing-running.png \
>   --script do_nothing.py \
>   --data-id do-nothing
Did nothing
Saved profile-nothing-running.png
```

![Nothing running][nothing]

[nothing]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-nothing-running.png

## Discussion

With `multiprocessing`, there is near-perfect scaling until 4 cores. Then
8 cores takes twice as long as 4 cores (i.e. there is no speedup, the
virtual cores are "fake").

With `threading`, I am still not sure what I'm looking at. It seems (from
[StackOverflow][1] and a [blog post][2] from a respected community member)
that the answer is the threads are **actually** at the OS level, so they
do use multiple cores. However, they are still bound by the shared global
state of the GIL. Quoth Jesse Noller:

> CPython uses what's called "operating system" threads under the covers,
> which is to say each time a request to make a new thread is made, the
> interpreter actually calls into the operating system's libraries and
> kernel to generate a new thread.

[1]: https://stackoverflow.com/a/4496918/1068170
[2]: http://jessenoller.com/2009/02/01/python-threads-and-the-global-interpreter-lock/
