+++
title = "Introduction to Julia by TV denoising"
date = Date(2021, 06, 05)
hasmath = true
hascode = true
tags = ["optimization", "signal processing"]
mintoclevel = 2
maxtoclevel = 3
descr = """
Welcome to an attempt at *simultaneous learning*, where I learn to separate
skills (Julia programming and TV denoising) without prior knowledge of either!
Starring Fabio, and Masa. 
![](/assets/tvd/exfabio.png)
"""
+++

\newcommand{\D}{\mathbf{D}}
\newcommand{\d}{\mathbf{d}}
\newcommand{\x}{\mathbf{x}}
\newcommand{\y}{\mathbf{y}}
\newcommand{\z}{\mathbf{z}}
\newcommand{\u}{\mathbf{u}}

# {{ title }}

In this post, we implement a naive version of color-image TV denoising in the
Julia programming language.

\toc

## Total Variation Color Image Denoising
The TV-denoising model can be motivated by wanting to approximate a clean image
as piecewise constant. As such, the desired image will have a sparse gradient,
$\nabla \x$. We can approximate the gradient to first order by a finite
difference scheme, $\nabla \x \approx \D\x$, with $(\D\x)[i] =
\x[i]-\x[i-1]$.


We then formulate the TV-denoising problem as

\begin{equation}
	\minimize{\x} \tfrac{1}{2}\norm{\x-\y}_2^2 + \lambda \norm{\D\x}_1,
\end{equation}

and which we can reformulate with a constraint equation to be amenable to ADMM,

\begin{eqnarray}
	\minimize{\x}& \tfrac{1}{2}\norm{\x-\y}_2^2 + \lambda \norm{\z}_1 \\
	\st &           \D\x - \z = \mathbf{0}
\end{eqnarray}

We now derive [our iterates in scaled form](/notes/admm_scaled/)
\begin{eqnarray} \label{eq:tv_xit}
	\x^{k+1} &\coloneqq& \argmin{\x} (1/2)\norm{\x-\y}_2^2 +
	(\rho/2)\norm{\D\x - \z^k + \u^k}_2^2 \\
	\mathbf{0} &=& (\x^{k+1}-\y) + \rho\D^\top (\D\x^{k+1} - \z^{k} + \u^k) \\
	 \x^{k+1} &=& (I + \rho \D^\top\D)^{-1}(\y + \rho\D^\top(\z^k - \u^k))
\end{eqnarray}

The above $\x$ iterate involves solving a tridiagonal system, which is fast. As
the LHS of the system is static, we can store its Cholesky factor for faster
subsequent solves. However, if we further employ the TV operator with *circular
convolution*, the system is diagonalized in the Fourier domain as $\D =
\mathcal{F}^\herm \Lambda \mathcal{F}$. Our $x$ update then is then,

\begin{equation} \label{eq:tv_xit_fft}
	 \x^{k+1} = \mathcal{F}^\herm (I + \rho \abs{\Lambda}^2)^{-1}\mathcal{F}(\y + \rho\D^\top(\z^k - \u^k))
\end{equation}

In this case, we can precompute and store the diagonal Fourier coefficients,
${C = 1/(1 + \rho \abs{\Lambda}^2)}$. Our $z$-update is an element-wise
soft-thresholding[^1]

\begin{eqnarray}
	\z^{k+1} &\coloneqq& \argmin{\z} \lambda\norm{\z}_1 +
	(\rho/2)\norm{\D\x^{k+1} - \z + \u^k}_2^2 \\
	&=& \mathrm{ST}\left(\D\x^{k+1} + \u^k,\, \lambda/\rho \right)
\end{eqnarray}


Lastly, we have the scaled dual ascent, $\u^{k+1} = \u^k + \D\x^{k+1} -
\z^{k+1}$.

In the case of 2D signals (i.e. an image), a simple option
for an approximation to the gradient would be a finite difference scheme in both
$x$ and $y$ directions[^3],

\begin{equation}
	\D\x = \begin{bmatrix} \D_x\x \\ \D_y\x \end{bmatrix} = 
	\begin{bmatrix} \d_x \ast \x \\ \d_y \ast \x \end{bmatrix}, \quad
	\begin{matrix}
	(\d_x \x)[i,j] = \x[i,j] - \x[i,j-1] \\
	(\d_y \x)[i,j] = \x[i,j] - \x[i-1,j]
	\end{matrix}
\end{equation}

Our $x$-update can still be computed in the Fourier domain via diagonalizing
$\D^\top\D$,

\begin{eqnarray} \label{eq:tv_eigen_gram}
	\D^\top\D &=& \D_x^\top\D_x + \D_y^\top \D_y\\
	&=&\mathcal{F}^\herm (\abs{\Lambda_x}^2 + \abs{\Lambda_y}^2 ) \mathcal{F}
\end{eqnarray}

to yeild the update,

\begin{equation} \label{eq:tv_fourier_xupdate}
	\x^{k+1} = \mathcal{F}^\herm (I + \rho (\abs{\Lambda_x}^2 + \abs{\Lambda_y}^2))^{-1}\mathcal{F}(\y + \rho\D^\top(\z^k - \u^k))
\end{equation}

We can further extend this to RGB images (or any other multi-feature image) by
separately taking $x$ and $y$ derivatives in each channel. 
For $\x =[\x_R ; \x_G ; \x_B]$,

\begin{equation}
	\D_3\x = \begin{bmatrix} \D_x \x_R \\ \D_y \x_R \\
							   \D_x \x_G \\ \D_y \x_G \\
							   \D_x \x_B \\ \D_y \x_B 
			   \end{bmatrix}
	= \Big( I_3 \otimes \underbrace{\begin{bmatrix} \D_x & 0 \\ 0 & \D_y
	\end{bmatrix}}_{\D} \Big) \x
\end{equation}

Where $\otimes$ is the Kronecker product. By the nature of Kronecker products,
transposition is distributive and $(A \otimes B)(C \otimes D) = AC\otimes BD$.
Therefore, 

\begin{equation}
\D_3^\top\D_3 = I_3 \otimes \D^\top\D,
\end{equation}

and our x-update involves dividing by Fourier domain factor $C$ (in 
\eqref{eq:tv_fourier_xupdate}) channel-wise.

## Julia Implementation
I've implemented a TV image denoising package, [TVDenoise.jl](https://github.com/nikopj/TVDenoise.jl). 
Below I walk through the source code in more detail and how I've learned to program in Julia.

### Julia Workflow
Julia is most easily interfaced with via the
[REPL](https://docs.julialang.org/en/v1/stdlib/REPL/) (read-eval-print-loop).
There are 5 modes: Julian (default), Shell (`;`), Help (`?`), Package (`]`), Search (`^r`/`^s`).
This is pretty similar to Matlab except you can't clear your workspace variables.

#### Packages
- [NNlib](https://github.com/FluxML/NNlib.jl): from the
  [Flux](https://fluxml.ai/Flux.jl/stable/) machine/deep learning library for our
  convolutions. Flux follows the convention of placing channel and batch dimension
  last, i.e. `(H,W,C,B)`. Unfortunately, right now it doesn't have a circular
  padding function.
- [FFTW](https://github.com/JuliaMath/FFTW.jl): Fastest Fourier Transform in the West, conforming to Julia's 
  [AbstractFFT.jl API](https://juliamath.github.io/AbstractFFTs.jl/stable/api/#Public-Interface-1).
- [SparseArrays](https://docs.julialang.org/en/v1/stdlib/SparseArrays/) for sparse linear system solving.
- [Printf](https://docs.julialang.org/en/v1/stdlib/Printf/) gives the `@printf` macro for C-like printing.
 
Package `pkg` can be installed via `] add pkg` in the REPL.
You can start using package `pkg` in two different ways:
- `import pkg`: Allows you to call functions defined in `pkg` via `pkg.function()`.
- `using pkg`: Same as `import pkg` but also brings a few specific functions specified by the package into the default namespace.

#### Workflow
- **Quick scripting**: You can run scripts as executables with the shebang
  `#!/usr/bin/env julia`, however keeping the REPL open means you don't
  have to recompile packges everytime you run the script. Run your script in
  the REPL via `include("/path/to/script.jl")`.

- **Projects**: I followed the [guide by Thibaut
  Leinart](https://tlienart.github.io/pub/julia/dev-pkg.html) for creating a
  package. This allows you to have your main functions included via `Using
  TVDenoise` in a separate testing code (`test/example.jl`).
  [Revise.jl](https://timholy.github.io/Revise.jl/stable/) allows the Julia
  REPL to track our project as we write to it, so that code updates to your
  codebase are taken into account without re-including the code or restarting
  the REPL. I recommend [including Revise in your `startup.jl`](https://timholy.github.io/Revise.jl/stable/config/).

### The Sparse Way
We can write scalar soft-thresholding function in one line:

```julia:scalar_ST
ST(x,τ) = sign(x)*max(abs(x)-τ, 0)
ST(1,0.5)
```
\show{scalar_ST}

To apply `ST` (or any scalar function) element-wise we use dot-syntax (and `'`
to turn the resulting column-vector into a row-vector for display purposes),

```julia:vector_ST
x = -1:0.2:1
y = ST.(x,0.2)'
```
\show{vector_ST}

\warning{}{
**All variables are passed by reference**, not value -- if you augment a
variable inside a function it will change outside of it too. Functions that
mutate their inputs are post-fixed by `!` by convention, ex. `push!(v)`.
}

We can always implement the ADMM described above directly with **sparse linear
solves**. First, we need to generate the sparse first-order derivative matrix. 
```julia
function FDmat(N::Int)::SparseMatrixCSC
	spdiagm(0 => -1*ones(N), 1 => ones(N))[1:N-1,1:N];
end
```
Here we specify the input as an integer and output as a `SparseMatrixCSC`. By
default, Julia functions return the return of their last statement.
Therefore, the return keyword is not needed in this function definition (though
it could be used). `FDmat(N)` returns $D \in \R^{N-1\times N}$ and imposes no
boundary conditions. 

The 2D TV operator is formed by stacking the horizontal and vertical first-order
derivative matrices on top of each other. These operators need to act on the
vectorized image. Using the fact that **Julia stores matrices column-major**,
you should be able to understand why our 2D and 3D functions are implemented as
follows,

```julia
function FDmat(M::Int, N::Int)::SparseMatrixCSC
	# vertical derivative
	S = spdiagm(N-1, N, ones(N-1));
	T = FDmat(M);
	Dy = kron(S,T);
	# horizontal derivative
	S = FDmat(N);
	T = spdiagm(M-1, M, ones(M-1));
	Dx = kron(S,T);
	return [Dx; Dy];
end

function FDmat(M::Int, N::Int, C::Int)::SparseMatrixCSC
	kron(I(C),FDmat(M,N))
end
```

This definition of `FDmat()` shows off Julia's "multiple dispatch", which is
basically function overloading. 

\note{}{
Type decorating of function arguments is really only necessary
for multiple dispatching, and doesn't affect performance.
}

With this, we can implement the ADMM TVD solver `tvd()`,

```julia
function tvd(y::AbstractVector, D::AbstractMatrix, λ, ρ, maxit, tol, verbose)
	M, N = size(D);
	objfun(x,Dx) = 0.5*sum((x-y).^2) + λ*norm(Dx, 1);
	x = y;
	z = zeros(M);
	u = zeros(M);
	F = zeros(maxit); # objective fun,
	r = zeros(maxit); # primal residual
	s = zeros(maxit); # dual residual

	C = cholesky(I + ρ*D'*D);

	k = 0; 
	while k == 0 || k < maxit && r[k] > tol
		x = C\(y + ρ*D'*(z - u)); # x-update
		Dx = D*x;
		zᵏ = z;
		z = ST.(Dx + u, λ/ρ);     # z-update
		u = u + Dx - z;           # dual ascent
		r[k+1] = norm(Dx - z);
		s[k+1] = ρ*norm(D'*(z - zᵏ));
		F[k+1] = objfun(x,Dx);
		k += 1;
		if verbose
			@printf "k: %3d | F= %.3e | r= %.3e | s= %.3e \n" k F[k] r[k] s[k] ;
		end
	end
	return x, (k=k, obj=F[1:k], pres=r[1:k], dres=s[1:k])
end
```

In `tvd()` we precompute our Cholesky factor to have fast $x$ updates. `C` is a
special object ready for solving linear systems via backslash `\ `.  As the
above `tvd()` is defined only for vector inputs, we can overload to define a
`tvd()` function for 2D and 3D inputs.

```julia
function tvd(y::AbstractArray, λ, ρ=1; maxit=100, tol=1e-6, verbose=true)
	sz = size(y);
	D = FDmat(sz...);
	x, hist = tvd(vec(y), D, λ, ρ, maxit, tol, verbose);
	return reshape(x, sz...), hist
end
```

This has turned out so clean because we've already overloaded `FDmat()` to return the
correct TV operators. Note that the "splat" operator (`...`) unpacks tuples and
more (see `? ...`). 

### The Fast (Fourier Transform) Way
The assumption of periodicity allows us to diagonalize our linear system in the Fourier domain and solve much faster. We first need to create our own circular convolution function, as circular padding isn't implemented in NNlib.jl.

\label{pad_circular}
```julia
function pad_circular(A::Array{<:Number,4}, pad::NTuple{4,Int})
	M, N = size(A)[1:2]
	if any(pad .> M) || any(pad .> N)
		error("padding larger than original matrix!")
	end
	# allocate array
	B = pad_constant(A, pad, dims=(1,2))
	t, b, l, r = pad
	f(p,L) = L-p+1:L
	# top-left lorner
	B[1:t, 1:l, :, :]               = A[f(t,M), f(l,N), :, :]
	# top-middle
	B[1:t, l+1:l+N, :, :]           = A[f(t,M), :, :, :]
	# top-right
	B[1:t, f(r,N+l+r), :, :]        = A[f(t,M), 1:r, :, :]
	# left-middle
	B[t+1:t+M, 1:l, :, :]           = A[:, f(l,N), :, :]
	# right-middle
	B[t+1:t+M, f(r,N+l+r), :, :]    = A[:, 1:r, :, :]
	# bottom-left
	B[f(b,M+b+t), 1:l, :, :]        = A[1:b, f(l,N), :, :]
	# bottom-middle
	B[f(b,M+t+b), l+1:l+N, :, :]    = A[1:b, :, :, :]
	# bottom-right
	B[f(b,M+t+b), f(r,N+l+r), :, :] = A[1:b, 1:r, :, :]
	return B
end
```

The definition of `pad_circular()` gives an example of how to discriminate Array inputs 
based on the number of dimension. The crucial part is defining the element-type
to allow any subtype of `Number` via the subtype operator `<:`. Also note that
`NTuple{4,Int}` is short for `Tuple{Int,Int,Int,Int}`. A good way to check if
your arguments are labeled as desired is using `isa()`,

```julia:isa
A = reshape(collect(1:9), 3,3);
println(isa(A, Array{Number, 2}))
isa(A, Array{<:Number, 2})
```
\show{isa}

Use `typeof()` and `eltype()` to get the type of an array and its elements respectively.

We now can write the ADMM Fourier domain solver.

```julia
function tvd_fft(y::Array{<:Real,4}, λ, ρ=1; maxit=100, tol=1e-6, verbose=true)
	M, N, P = size(y)[1:3]
	# move channels to batch dimension
	y = permutedims(y, (1,2,4,3))
	τ = λ/ρ;

	# precompute C for x-update
	Λx = rfft([1 -1 zeros(N-2)'; zeros(M-1,N)]);
	Λy = rfft([[1; -1; zeros(M-2)] zeros(M,N-1)])
	C = 1 ./ ( 1 .+ ρ.*(abs2.(Λx) .+ abs2.(Λy)) );

	# real Fourier xfrm in image dimension.
	# Must specify length of first dimension for inverse.
	Q  = plan_rfft(y,(1,2));
	Qᴴ = plan_irfft(rfft(y),M,(1,2));

    # conv kernel
	W = Float64.(zeros(2,2,1,2));
	W[:,:,1,1] = [1 -1; 0 0];          # dx
	W[:,:,1,2] = [1  0;-1 0];          # dy
	Wᵀ = reverse(permutedims(W, (2,1,4,3)), dims=:);

	# Circular convolution
	D(x) = conv(pad_circular(x, (1,0,1,0)), W);
	Dᵀ(x)= conv(pad_circular(x, (0,1,0,1)), Wᵀ);

	objfun(x,Dx) = 0.5*sum(abs2.(x-y)) + λ*norm(Dx, 1);

	# initialization
	z = zeros(M,N,2,P);
	u = zeros(M,N,2,P);
	F = zeros(maxit); # store objective fun
	r = zeros(maxit); # store primal residual
	s = zeros(maxit); # store dual   residual

	k = 0;
	while k == 0 || k < maxit && r[k] > tol && s[k] > tol
		x = Qᴴ*(C.*(Q*( y + ρ*Dᵀ(z-u) ))); # x update
		Dxᵏ = D(x);
		zᵏ  = z;
		z = ST.(Dxᵏ+u, τ);                 # z update
		u = u + Dxᵏ - z;                   # dual ascent
		r[k+1] = norm(Dxᵏ-z);
		s[k+1] = norm(z-zᵏ);
		F[k+1] = objfun(x,Dxᵏ);
		k += 1;
		if verbose
			@printf "k: %3d | F= %.3e | r= %.3e | s= %.3e \n" k F[k] r[k] s[k];
		end
	end
	x = permutedims(x, (1,2,4,3));
	return x, (k=k, obj=F[1:k], pres=r[1:k], dres=s[1:k])
end
```

Circular convolution is implemented by our [circular padding](#pad_circular)
followed by NNlib's `conv`. 

\note{NNlib's convolution function}{
`conv` implements **valid convolution, not correlation**. Correlation can
be run instead by using the kwarg `flipped=true`. The supplied kernel `W`
is given by height, width, in-channels, and out-channels as
$[H,W,C_{\mathrm{in}},C_{\mathrm{out}}]$.  1D, 2D, 3D signals all use the
same `conv` function. The expression for `Wᵀ` is especially insightful --
filters must be spatially reversed and have their ordering reversed.
}

To perform $x$ and $y$ gradient calculations in the same conv function we have
to pay attention to padding. Our horizontal filter shouldn't touch our top
padding and our vertical filter shouldn't touch the left padding. Therefore, by
also taking into account that convolution is a flip and slide, we write the
kernel $W$'s two filters (in output dimension) as,

$$
W[:,:,1,1] = \begin{bmatrix} 1 & -1 \\ 0 & 0 \end{bmatrix} \quad 
W[:,:,1,2] = \begin{bmatrix} 1 &  0 \\-1 & 0 \end{bmatrix}.
$$

To precompute our Fourier factor $C$, we pad our filters to yeild the
$N$-dimensional transform domain representations. We can use `rfft` to exploit
the conjugate symmetry of our real-valued filters and only compute half the coefficients.

Our last point of interest is the use of planned FFTs. These return operators that use matrix multiplication syntax, but are not performing dense matrix-vector multiplications. The benefit in doing so is that the butterfly network used to compute our FFT is saved in memory for faster computation. The first argument of each plan function above is meant to give the size and data-type of inputs we'll use in the loop.

### Comparison
A full demo code can be found in [the repository](https://github.com/nikopj/TVDenoise.jl/blob/main/examples/example.jl). Code shown below is *not* given in the repository.

We demonstrate our working TV denoising on the example Fabio image with AWGN,
$\sigma_n = 25$ (on a 0-255 scale).

\figenv{The two methods acheive similar PSNR results.}{/assets/tvd/exfabio.png}{width:100%}

The similarity of results is to be expected because their solving almost exactly the same problem. Where we'll find gains is in our run times. 

I ran some rudimentary timing tests on different versions of the Fabio image and hard-coded results in the visualization script below. The FFT version is seriously fast in comparison. 

```julia
using Plots, StatsPlots
t1 = [3.3, 14.2, 24.5, 101.0] # tvd times
t2 = [0.5, 1.6,  2.8,  10.8]  # tvd_fft times
name = repeat(["Gray 256", "Color 256", "Gray 512", "Color 512"], outer=2)
group= repeat(["Sparse", "FFT"], inner=4)
groupedbar(name, [t1;t2], group=group)
ylabel!("time (s)")
savefig("timebar.svg")
```
\figenv{FFT vs. sparse-array timing comparison.}{/assets/tvd/timebar.svg}{width:80%}

As a last example, I'll demonstrate that TV denoising is not just a trick for
synthetically generated noisy images. Below is a real noisy photo of Masa.

\figenv{}{/assets/tvd/masa.png}{width:100%}

```julia
using TVDenoise, FileIO
img = load("masa.png")
img = imresize(img, ratio=1/4) # hide
x, _ = tvd_fft(img, 0.02, 5)
save("tvdmasa.png", x)
```

Our TV denoising is able to clean it up nicely.
\figenv{}{/assets/tvd/tvdmasa.png}{width:100%}

One question that persists throughout this demos is, "Is there a different set of filters that are better tailored to regularizing the denoising problem?". We can formulate our problem as also being a minimization over $\D$, known as the Analysis Convolutional Dictionary Learning problem. Special care has to be taken to ensure that $\D$ is not degenerate. A Julia implementation for another post!

[^1]: See [*{{ fill title blog/understanding-ista.md }}*](/blog/understanding-ista/#derivation_of_the_proximal_operator_for_the_ell_1-norm) for a derivation of soft-thresholding.
