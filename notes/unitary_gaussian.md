+++
title = "Note: Channel-wise Unitary Transform of an i.i.d. Normal Random Variable"
date = Date(2024, 01, 21)
hasmath = true
tags = ["notes", "optimization"]
draft = false
descr = "or, the Fourier Transform of a Gaussian R.V. is the same Gaussian R.V."
+++

\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\E}{\mathbb{E}}
\newcommand{\N}{\mathcal{N}}
\newcommand{\x}{\mathbf{x}}
\newcommand{\y}{\mathbf{y}}
\newcommand{\bOne}{\mathbf{1}}
\newcommand{\Cov}{\mathrm{Cov}}

# A Unitary Transform of an i.i.d. Normal Random Variable
Consider an independent identically distributed Normal random variable $\x$
with mean $\mu \in \C^C$ and covariance $\Sigma \in \C^{C \times C}$. Let $\x$
have $N$ vector-valued pixels, each with $C$ channels, i.e. $\x \in \R^{NC}$
and

$$
\x[i] \sim \N(\mu, ~ \Sigma) \quad \forall \quad 1 \leq i \leq N.
$$

Further, let $\x$ have the channel-wise vectorization $\x = [\x_1^T, \, \x_2^T,
\, \dots, \, \x_C^T]^T$. We can then write this via Kronecker product notation as 

$$
\x \sim \N(\mu \otimes \bOne_N, ~ \Sigma \otimes I_N).
$$

Now, consider a linear transformation $\y = A\x$. We know from linearity of expectation 
that $\E[A\x] = A\E[\x] = A(\mu \otimes \bOne_N)$ and that $\Cov(A\x) = A\Cov(\x)A^H$.

Further, consider a channel-wise unitary matrix, i.e. $A = (I_C \otimes Q)$ where 
$Q \in \C^{N\times N}$ is unitary. The Kronecker notation here means that $A$ is a block
diagonal matrix with $C$ blocks of $Q$ on its diagonal. So, the mean and covariance of our transformed 
variable are

$$
\E[A\x] = (I_C \otimes Q)(\mu \otimes \bOne_N) \qquad \Cov(A\x) = (I_C \otimes Q)(\Sigma \otimes I_N)(I_C \otimes Q)^H
$$

The [mixed-product property of Kronecker product](https://en.wikipedia.org/wiki/Kronecker_product) tells us 
that, for sensible matrix sizes, $(A \otimes B)(C \otimes D) = (AC \otimes BD)$. Thus,

$$
\E[A\x] = (\mu \otimes Q\bOne_N) \qquad \Cov(A\x) = (\Sigma \otimes I_N),
$$

as $QQ^H = I_N$. For zero-mean Normally distributed noise, this results in the 
channel-wise unitary transform of said noise having the exact same distribution as 
before the transformation. 

## Parallel MRI
This is a particularly useful result in MRI, where the measurement domain 
is a $C$-channel (coil) Fourier domain contaminated by 
zero-mean additive white Gaussian noise (AWGN), i.e. we model measurements ($\y
\in \C^{NC}$) of image ($\x \in \C^N$) with coil sensitivity operator $S \in
\C^{NC \times N}$ via

$$
\y = (I_C \otimes F_N)S\x + v, \quad v \sim \N(0, ~ (\Sigma \otimes I_N)).
$$

where $F_N$ is the N-dimensional DFT matrix.
Equivalently we can write $\y \sim \N((I_C \otimes F_N)S\x, ~ (\Sigma \otimes I_N))$.
As the DFT matrix is unitary, we know from the above discussion that the
(multi-coil) image domain signal is contaminated with noise from the same
distribution,
$$
(I_C \otimes F_N^H)\y \sim \N(S\x, ~ (\Sigma \otimes I_N)).
$$
