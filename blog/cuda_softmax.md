+++
title = "An Efficient Softmax Kernel in CUDA.jl"
draft = true
date = Date(2023, 5, 28)
hasmath = true
hascode = true
tags = ["gpu", "cuda", "julia"]
mintoclevel = 2
maxtoclevel = 3
descr = """
Grid-stride loops, streams, warp and block reduce!
"""
+++

\newcommand{\sm}{\mathrm{sm}}
\newcommand{\x}{\mathbf{x}}
\newcommand{\y}{\mathbf{y}}
\newcommand{\z}{\mathbf{z}}
\newcommand{\bv}{\mathbf{v}}

\uline{Published {{ date }}}

\toc

# {{ title }}
In this post, we'll implement fast softmax CUDA kernels all in Julia's own CUDA.jl.
We'll compare three instances of the softmax 
operation, over vectors and matrices, on a CUDA device:
- a naive algorithm, using simple CUDA kernels under the hood. These kernels themselves are usually written in Julia.
- custom CUDA.jl kernels we'll write in Julia.
- cuDNN library kernels (CUDA C++), used under the hood by [NNlib.jl](https://github.com/FluxML/NNlib.jl).

The post is intended for:
1. those familiar with [the CUDA programming model](https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/)
   in terms of the thread-blocks, but not necessarily warps, reduction operations, and cooperative groups.
2. those who would like to see examples of these concepts in
   [CUDA.jl](https://juliagpu.org/cuda/), the Julia package for CUDA
   programming.

As a refresher, the CUDA heirarchy goes roughly as follows:
1. **Threads** are the fundamental unit of execution.
2. A **warp** is a collection of threads (usually 32) that execute in
   lock(-ish) step. Control-flow statements (eg. if statements) can cause
   threads within a warp to diverge, which is a source of slow-down. Threads
   within a warp can communicate with other very efficiently, though
   synchonization is needed because of possible divergence.
3. Warps are organized into **thread-blocks**. Threads within a thread-block
   may share memory via L1 cache (a.k.a, shared-memory, **shmem**). The number
   of threads per block is configurable at launch, and the max is generally 1024. 
   Threads within a block can be synchonized.
4. Blocks are organized into a **grid**.
   Blocks can communicate via global memory +
   synchronization when launched as a **cooperative-group**.
5. A **stream** is the abstraction of the launch of a grid to execute a kernel.
   Multiple streams can be executed in parallel/asynchronously on a single GPU. 

## The Softmax Operation
Let $\bv \in \R^N$ be our data vector. We define the softmax function as,

$$
\mathrm{sm} \left(\bv \right) [i] = \frac{\exp(\bv[i] - m)}{ \sum_{j} \exp(\bv[j] - m)}
$$

where $m = \max_i \bv[i]$ is the maximum of the input vector, used to avoid
under/overflow issues in the exponential.

A naive algorithm is given by passing over the vector once to find the maximum, 
passing over again to compute the denominator, and finally normalizing each component.
We can extend this to matrices by considering a softmax along the columsn (`dims=1`) 
or rows (`dims=2`). This naive softmax function is implemented below:

```julia
function sm_naive!(u, v; dims=1)
    m = maximum(v; dims=dims)
    @. u = exp(v - m)
    l = sum(u; dims=dims)
    @. u /= l
    return u
end
sm_naive!(v; kws...) = sm_naive!(v, v; kws...)
sm_naive(v; kws...) = sm_naive!(similar(v), v; kws...)
```

### Initial tests
For a $M\times N$ matrix, the softmax in either dimension has `5*M*N` reads/writes.
Below we benchmark the performance on a [NVIDIA Tesla V100 PCIe
GPU](https://www.techpowerup.com/gpu-specs/tesla-v100-pcie-16-gb.c2957), which
has a peak bandwidth of 900 GB/s.

```julia
julia> using CUDA, BenchmarkTools

julia> v = CUDA.randn(2^24);

julia> u = sm_naive!(similar(v), v); # warm-up

julia> b1 = @benchmark CUDA.@sync sm_naive!($u, $v)
BenchmarkTools.Trial: 7593 samples with 1 evaluation.
 Range (min … max):  610.550 μs …  60.810 ms  ┊ GC (min … max): 0.00% … 43.94%
 Time  (median):     640.211 μs               ┊ GC (median):    0.00%
 Time  (mean ± σ):   654.538 μs ± 691.394 μs  ┊ GC (mean ± σ):  0.54% ±  0.50%

     ▅█▅▁
  ▂▃▇████▅▃▃▂▂▃▄▆▇▇▇███▆▄▃▃▂▂▂▂▂▂▂▁▂▂▁▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▂▃▅▆▅▄▄▃▃ ▃
  611 μs           Histogram: frequency by time          732 μs <

 Memory estimate: 5.53 KiB, allocs estimate: 138.

julia> V = CUDA.randn(2^12, 2^16);

julia> U = sm_naive!(similar(V), V); # warm-up

julia> b2 = @benchmark CUDA.@sync sm_naive!($U, $V)
BenchmarkTools.Trial: 404 samples with 1 evaluation.
 Range (min … max):  12.137 ms … 12.538 ms  ┊ GC (min … max): 0.00% … 0.00%
 Time  (median):     12.368 ms              ┊ GC (median):    0.00%
 Time  (mean ± σ):   12.366 ms ± 77.932 μs  ┊ GC (mean ± σ):  0.00% ± 0.00%

                       ▄ █▁▄▂▆▃▆▁▂  ▁  ▂▇▂▂▅▃▂▄▄ ▆▃
  ▃▃▃▁▁▃▁▃▁▁▄▃▁▄▆▄▇▅▆▇▇█▇█████████▇▇█▇██████████▇██▇▇▇▇▄▅▆▄▅▃ ▅
  12.1 ms         Histogram: frequency by time        12.5 ms <

 Memory estimate: 6.86 KiB, allocs estimate: 131.
```

<!-- julia> bandwidth = 4*5*length(v) / median(b1).time  # GB/s -->
<!-- 524.1152057680983 -->
<!---->
<!-- julia> bandwidth = 4*5*(prod∘size)(V) / median(b2).time  # GB/s -->
<!-- 434.0915013232059 -->
<!---->
<!-- We calculate the above bandwidth of $\approx$ 500 GB/s as `sizeof(Float32)*5*length(v) / time_in_ns`. -->
<!-- We're well below  -->

We'll see if we can do any better with custom kernels.

\dropblue{juliaisms}{A couple Julia-isms to note:}{
- `!`: By convention, we end the function name with a `!` if it mutates its
  arguments (in most cases just the first arg).
- `@.`: The macro `@. u = exp(v)` expands to `u .= exp.(v)`, meaning that the
  exponential of `v` is evaluated element-wise and assigned element-wise to
  `u`. The use of the macro ensures that this happens in just one pass over `u`
  and `v` jointly, instead of one pass over `v` for the exponential and then
  one pass over `u` for the assignment.
- `similar`: We write an inplace version and non-mutating version of the algorithm using 
  multiple dispatch below the original algorithm. The function `similar` allocates 
  an vector of identical length and type.
- `CUDA.@sync`: It's always necessary to sync the GPU when benchmarking to get proper timing results.
}

## Fused Softmax
The following is a column-wise softmax implementation inspired by the OneFlow blog-post, 
["How to Implement an Efficient Softmax CUDA Kernel — OneFlow Performance Optimization"](https://oneflow2020.medium.com/how-to-implement-an-efficient-softmax-cuda-kernel-oneflow-performance-optimization-sharing-405ad56e9031) (2021).

### The Plan
We consider a $M\times N$ matrix with element-type $T$, and expect that,
- M is around 1024 to 4096, with `M * sizeof(T)` fitting in shmem.
- N is massive.
The V100 has 128 KB of L1 cache (shmem), so for `T=Float32` we can afford $M$ up to 32,000.

The plan is that **each thread-block computes the softmax of a column**:
- If the column is larger than a block, each block must be responsible for mulitiple rows (via a block-stride loop).
- If the number of columns is greater than the grid dimension, each block must be
  responsible for multiple columns (via a grid-stride loop).

As shown in the naive algorithm, the softmax requires multiple passes over the data vector.
In order to reduce accesses to global memory, we can initialize a shared-memory buffer to 
store our intermediate computations, reducing our `5N` read/writes of the naive algorithm to just `2N` (from global memory).

### The Kernel
We'll start by presenting the basic softmax kernel below. Note that we
initialize two different types of shared memory, static and dynamic. **Static
memory** is defined by its size being known at compile time (in this case simply
1), while **dynamic memory** does not have this requirement (its size needs
to be specified at kernel launch).

Each thread of a block then loads an element into the buffer and then sets its local maximum (`local_max`).
The `CUDA.reduce_block`[^1] call aggregates all the thread-local copies of `local_max` to thread-1 with the max operation.
Internally, this uses reductions over warp (see `CUDA.reduce_warp`[^1]).
After a reduction, the result can be broadcast from thread-1 to all other threads in the block simply by using 
the static piece of shared memory we initialized at the start of the kernel.
A similar process of thread-local ops, reduction, and broadcas, happens for
computing the column sum.

Below we show simple version of the kernel for easier reading, which assumes 
that the block-dim is $\leq M$, and the grid-dim is equal to $N$.
If you toggle the block, the complete version is given, which can handle $M \leq 2^{16}$ and 
arbitrary $N$.

\toggletext{kernel}{The Kernel}{
```julia
function kernel!(U, V, M, N)
    row = threadIdx().x
    col = blockIdx().x

    m = CuStaticSharedArray(T, 1)
    l = CuStaticSharedArray(T, 1)
    buf = CuDynamicSharedArray(T, blockDim().x)

    # -----------------------------------------------
    # -- load data into buffer and compute maximum --
    # -----------------------------------------------
    local_max = T(-Inf)
    buf[row] = row <= M ? V[row, col] : T(-Inf)
    local_max = max(local_max, buf[row])
    col_max = CUDA.reduce_block(max, local_max, T(-Inf), Val(true))

    # reduce_block gathers to thread-1,
    # so we use shared memory to scatter it.
    if threadIdx().x == 1i32
        m[] = col_max
    end
    sync_threads()
    col_max = m[]

    # -----------------
    # -- compute sum --
    # -----------------
    local_sum = zero(T)
    e = exp(buf[row] - col_max)
    buf[row] = e
    local_sum += e
    col_sum = CUDA.reduce_block(+, local_sum, zero(T), Val(true))

    if threadIdx().x == 1i32
        l[] = col_sum
    end
    sync_threads()
    col_sum = l[]

    # --------------------------------
    # -- normalize vector and write --
    # --------------------------------
    if row <= M
        U[row, col] = buf[row] / col_sum
    end
    return nothing
end
```
}{
```julia
function kernel!(U, V, M, N, col0)
    # number of rows/cols to process per block
    nrow = cld(M, blockDim().x)

    m = CuStaticSharedArray(T, 1)
    l = CuStaticSharedArray(T, 1)
    buf = CuDynamicSharedArray(T, nrow*blockDim().x)

    # grid-stride loop
    col = col0 + blockIdx().x - 1i32
    while col <= col0 + N - 1i32
        # -----------------------------------------------
        # -- load data into buffer and compute maximum --
        # -----------------------------------------------
        local_max = T(-Inf)

        # block-stride loop
        row = threadIdx().x
        while row <= M
            buf[row] = V[row, col]
            local_max = max(local_max, buf[row])
            row += blockDim().x
        end
        col_max = CUDA.reduce_block(max, local_max, T(-Inf), Val(true))

        # reduce_block gathers to thread-1,
        # so we use shared memory to scatter it.
        if threadIdx().x == 1i32
            m[] = col_max
        end
        sync_threads()
        col_max = m[]

        # -----------------
        # -- compute sum --
        # -----------------
        local_sum = zero(T)

        # block-stride loop
        row = threadIdx().x
        while row <= M
            e = exp(buf[row] - col_max)
            buf[row] = e
            local_sum += e
            row += blockDim().x
        end
        col_sum = CUDA.reduce_block(+, local_sum, zero(T), Val(true))

        if threadIdx().x == 1i32
            l[] = col_sum
        end
        sync_threads()
        col_sum = l[]

        # ----------------------
        # -- normalize vector --
        # ----------------------
        # block-stride loop
        row = threadIdx().x
        while row <= M
            U[row, col] = buf[row] / col_sum
            row += blockDim().x
        end

        col += gridDim().x
        sync_threads()
    end
    return nothing
end
```
}
Note that `xi32` is just a convienient syntax for `Int32(x)`, which you can use via 
`using CUDA: i32`. Using `i32`s is good practice for avoiding uncessary conversions from 
Julia's default Int64 to the CUDA native Int32 during integer arithmetic. For
example, `threadIdx().x` returns an Int32.

### Launch Configuration
We've alluded to the fact that we may need to account for block/grid-dims that
are not perfectly matching our data dimensions. Clearly this will happend for
`M > max_threads` (generally 1024). It is also good practice to query the
device for its availability, and so we may end up with less blocks then needed
(hence the grid-stride loop above).

In CUDA.jl, to get such information we can perform a `cuda` call with `launch=false`, 
and use the resulting `kernel` object to acutally launch the kernel with the recommended 
block and grid dimensions. We need to provide the launch config query with a function 
that computes our required shared memory (in bytes) given the number of threads in a block.
Because we're using warp-reductions under the hood in our `reduce_block` calls above, 
we make sure to always use/request a number of threads that is a multiple of the warpsize.

The below code-block shows the launch configuration for the above softmax kernel. 

\toggletext{launch}{The Launch Configuration}{
```julia
function fused_col_softmax!(U::AnyCuMatrix{T}, V::AnyCuMatrix{T}) where T
    function kernel!(U, V, M, N, col0)
        #= the kernel code from above (with grid-stride loop) =#
    end

    M, N = size(V)
    dev = device()
    wanted_threads = nextwarp(dev, M)
    function compute_threads(max_threads)
        if wanted_threads > max_threads
            prevwarp(dev, max_threads)
        else
            wanted_threads
        end
    end
    compute_shmem(threads) = sizeof(T)*cld(M, threads)*threads
    kernel  = @cuda launch=false kernel!(U, V, Int32(M), Int32(N), 1i32)

    config  = launch_configuration(kernel.fun; shmem=compute_shmem∘compute_threads)
    threads = compute_threads(config.threads)
    blocks  = N
    shmem   = compute_shmem(threads)
    kernel(U, V, Int32(M), Int32(N), 1i32; threads=threads, blocks=blocks, shmem=shmem)

    return U
end
```
}{
```julia
function fused_col_softmax!(U::AnyCuMatrix{T}, V::AnyCuMatrix{T}) where T
    function kernel!(U, V, M, N, col0)
        #= the kernel code from above (with grid-stride loop) =#
    end

    M, N = size(V)
    dev = device()
    wanted_threads = nextwarp(dev, M)
    function compute_threads(max_threads)
        if wanted_threads > max_threads
            prevwarp(dev, max_threads)
        else
            wanted_threads
        end
    end
    compute_shmem(threads) = sizeof(T)*cld(M, threads)*threads

    # when we have a large number of rows,
    # parallelize over streams as well.
    max_cols = 2^16
    num_streams = cld(N, max_cols)
    streams = [CuStream(; flags=CUDA.STREAM_NON_BLOCKING) for _ in 1:num_streams]
    kernel  = @cuda launch=false kernel!(U, V, Int32(M), Int32(N), 1i32)

    @unroll for s=1:num_streams
        col_range = ((s-1)*max_cols + 1):min(N, s*max_cols)
        Ns = length(col_range)

        config  = launch_configuration(kernel.fun; shmem=compute_shmem∘compute_threads)
        threads = compute_threads(config.threads)
        # blocks  = min(config.blocks, Ns)
        blocks  = Ns
        shmem   = compute_shmem(threads)
        kernel(U, V, Int32(M), Int32(Ns), Int32(col_range[1]);
               threads=threads, blocks=blocks, shmem=shmem, stream=streams[s])
    end
    for s in streams; CUDA.synchronize(s); end

    return U
end
```
}


### Stream Parallelism
When toggled, the above code-block shows a stream-parallelized version of the launch configuration. 
Though the written kernel allows for an arbitrary size of $N$ (num-columns), in practice we find that 
having a single block do more than 1-4 columns dramatically slows down performance. Hence, in the above launch configs 
we've ignored the devices recommended configuration and simply set `blocks=N`. However, for wide matrices, 
it's easy to hit the block limit of $2^{16}$. In such cases, we can turn to *stream-parallelism*, where we 
launch the kernel multiple times, with column offsets so that they tackle different columns subsets of the matrix.

## Runtime Experiments

[^1]: [https://github.com/JuliaGPU/CUDA.jl/blob/master/src/mapreduce.jl](https://github.com/JuliaGPU/CUDA.jl/blob/master/src/mapreduce.jl)
