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
$ python3.6 watch_cpu.py \
>   --total-intervals 18 \
>   --filename-base profile-multiproc-2 \
>   --data-id multiprocessing:2 \
>   --script use_multiprocessing.py \
>            --num-procs 2 \
>            --pin-cpu
36028796884746240
36028796884746240
Saved profile-multiproc-2-077c2b2f-9683-42f3-9df1-25a065f9f8d8.png
```

![Using multiprocessing with 2 cores][multiproc2]

[multiproc2]: images/profile-multiproc-2-077c2b2f-9683-42f3-9df1-25a065f9f8d8.png

## `multiprocessing` with 4 processes

```
$ python3.6 watch_cpu.py \
>   --total-intervals 18 \
>   --filename-base profile-multiproc-4 \
>   --data-id multiprocessing:4 \
>   --script use_multiprocessing.py \
>            --num-procs 4 \
>            --pin-cpu
36028796884746240
36028796884746240
36028796884746240
36028796884746240
Saved profile-multiproc-4-063a462d-0dce-42d3-9fc6-2fcbfe9d48da.png
```

![Using multiprocessing with 4 cores][multiproc4]

[multiproc4]: images/profile-multiproc-4-063a462d-0dce-42d3-9fc6-2fcbfe9d48da.png

## `multiprocessing` with 8 processes

```
$ python3.6 watch_cpu.py \
>   --total-intervals 15 \
>   --interval 2 \
>   --filename-base profile-multiproc-8 \
>   --data-id multiprocessing:8 \
>   --script use_multiprocessing.py \
>            --num-procs 8 \
>            --pin-cpu
36028796884746240
36028796884746240
36028796884746240
36028796884746240
36028796884746240
36028796884746240
36028796884746240
36028796884746240
Saved profile-multiproc-8-e983a3c0-8c08-4fd8-82a6-ce64d31b6899.png
```

![Using multiprocessing with 8 cores][multiproc8]

[multiproc8]: images/profile-multiproc-8-e983a3c0-8c08-4fd8-82a6-ce64d31b6899.png

## `threading` with 2 threads

```
$ python3.6 watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-threading-2 \
>   --data-id threading:2 \
>   --script use_threading.py \
>            --num-threads 2 \
>            --pin-cpu
2251799780130816
2251799780130816
Saved profile-threading-2-f001349e-d02b-43d2-929d-15e55aca10ed.png
```

![Using threading with 2 threads][threading2]

[threading2]: images/profile-threading-2-f001349e-d02b-43d2-929d-15e55aca10ed.png

## `threading` with 4 threads

```
$ python3.6 watch_cpu.py \
>   --total-intervals 24 \
>   --filename-base profile-threading-4 \
>   --data-id threading:4 \
>   --script use_threading.py \
>            --num-threads 4 \
>            --pin-cpu
2251799780130816
2251799780130816
2251799780130816
2251799780130816
Saved profile-threading-4-efa9f722-d8f1-4f6c-b5ed-7f5a05a00292.png
```

![Using threading with 4 threads][threading4]

[threading4]: images/profile-threading-4-efa9f722-d8f1-4f6c-b5ed-7f5a05a00292.png

## `threading` with 8 threads

```
$ python3.6 watch_cpu.py \
>   --total-intervals 32 \
>   --filename-base profile-threading-8 \
>   --data-id threading:8 \
>   --script use_threading.py \
>            --num-threads 8 \
>            --pin-cpu
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
2251799780130816
Saved profile-threading-8-9756046c-cd1b-4190-a128-9e4ad8bf4cd4.png
```

![Using threading with 8 threads][threading8]

[threading8]: images/profile-threading-8-9756046c-cd1b-4190-a128-9e4ad8bf4cd4.png

## Non-Threaded

```
$ python3.6 watch_cpu.py \
>   --total-intervals 18 \
>   --filename-base profile-non-threaded \
>   --data-id non-threaded:1 \
>   --script non_threaded.py
36028796884746240
Saved profile-non-threaded-c3186a05-46b0-4b4e-95ac-5d602d882317.png
```

![Do the computation without threading][non-threaded]

[non-threaded]: images/profile-non-threaded-c3186a05-46b0-4b4e-95ac-5d602d882317.png

## Baseline

Here is my machine when no Python process is running (but any background
is acceptable):

```
$ python3.6 watch_cpu.py \
>   --total-intervals 12 \
>   --filename-base profile-nothing-running \
>   --data-id do-nothing \
>   --script do_nothing.py
Did nothing
Saved profile-nothing-running-2f52de95-ac0e-4c13-a773-5f41723671e2.png
```

![Nothing running][nothing]

[nothing]: images/profile-nothing-running-2f52de95-ac0e-4c13-a773-5f41723671e2.png

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
