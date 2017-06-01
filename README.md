This is a simple hack to illustrate Python's use of cores
with concurrent / parallel code. (The code here is CPU
intensive, not I/O intensive.)

There are two files `use_multiprocessing.py` and
`use_threading.py`, which will be traced using:

```python
psutil.cpu_times_percent(interval, percpu=True)
```

This was done on a 4-core machine with 8 virtual cores.

## `multiprocessing` with 2 processes

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-multiproc-2 \
>   --script use_multiprocessing.py \
>   --num-procs 2 \
>   --data-id multiprocessing:2
[36028796884746240, 36028796884746240]
Saved profile-multiproc-2-c5a1dc52-9107-45ae-8fe3-5e304dfca960.png
```

![Using multiprocessing with 2 cores][multiproc2]

[multiproc2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-multiproc-2-c5a1dc52-9107-45ae-8fe3-5e304dfca960.png

## `multiprocessing` with 4 processes

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-multiproc-4 \
>   --script use_multiprocessing.py \
>   --num-procs 4 \
>   --data-id multiprocessing:4
[36028796884746240, 36028796884746240, 36028796884746240, 36028796884746240]
Saved profile-multiproc-4-64ad3a08-28c2-4a68-adee-121d67ab43b1.png
```

![Using multiprocessing with 4 cores][multiproc4]

[multiproc4]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-multiproc-4-64ad3a08-28c2-4a68-adee-121d67ab43b1.png

## `multiprocessing` with 8 processes

```
$ python watch_cpu.py \
>   --total-intervals 19 \
>   --filename-base profile-multiproc-8 \
>   --script use_multiprocessing.py \
>   --num-procs 8 \
>   --data-id multiprocessing:8
[36028796884746240, 36028796884746240, ...]
Saved profile-multiproc-8-8fdcf2e7-8665-4e8a-8a68-8135151b9e5f.png
```

![Using multiprocessing with 8 cores][multiproc8]

[multiproc8]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-multiproc-8-8fdcf2e7-8665-4e8a-8a68-8135151b9e5f.png

## `threading` with 2 threads

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-threading-2 \
>   --script use_threading.py \
>   --num-threads 2 \
>   --data-id threading:2
2251799780130816
2251799780130816
Saved profile-threading-2-bb37639e-2c7a-4654-bd52-58610b9c60fd.png
```

![Using threading with 2 threads][threading2]

[threading2]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-threading-2-bb37639e-2c7a-4654-bd52-58610b9c60fd.png

## `threading` with 4 threads

```
$ python watch_cpu.py \
>   --total-intervals 19 \
>   --filename-base profile-threading-4 \
>   --script use_threading.py \
>   --num-threads 4 \
>   --data-id threading:4
2251799780130816
2251799780130816
2251799780130816
2251799780130816
Saved profile-threading-4-cba8b645-e29a-4f69-8aa3-fc07a7420080.png
```

![Using threading with 4 threads][threading4]

[threading4]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-threading-4-cba8b645-e29a-4f69-8aa3-fc07a7420080.png

## `threading` with 8 threads

```
$ python watch_cpu.py \
>   --total-intervals 32 \
>   --filename-base profile-threading-8 \
>   --script use_threading.py \
>   --num-threads 8 \
>   --data-id threading:8
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
Saved profile-threading-8-56dda57f-eaa2-46f3-87f2-aa9b456682c3.png
```

![Using threading with 8 threads][threading8]

[threading8]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-threading-8-56dda57f-eaa2-46f3-87f2-aa9b456682c3.png

## Non-Threaded

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-non-threaded \
>   --script non_threaded.py \
>   --data-id non-threaded:1
36028796884746240
Saved profile-non-threaded-a9f9dbae-c138-4eae-8b76-baf2e054d31f.png
```

![Do the computation without threading][non-threaded]

[non-threaded]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-non-threaded-a9f9dbae-c138-4eae-8b76-baf2e054d31f.png

## Baseline

Here is my machine when no Python process is running (but any background
is acceptable):

```
$ python watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-nothing-running \
>   --script do_nothing.py \
>   --data-id do-nothing
Did nothing
Saved profile-nothing-running-2f52de95-ac0e-4c13-a773-5f41723671e2.png
```

![Nothing running][nothing]

[nothing]: https://gist.githubusercontent.com/dhermes/9c92cb6468ed39c51213b5e0a6176fb4/raw/profile-nothing-running-2f52de95-ac0e-4c13-a773-5f41723671e2.png

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
