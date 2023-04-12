+++
title = "On using the multi-dimensional chain-rule correctly."
draft = false
date = Date(2023, 4, 12)
tags = ["deep learning"]
hasmath = true
descr = """
TLDR: employing the multi-dimensional chain-rule means writing matrix-multiplication.
"""
+++

\newcommand{\R}{\mathbb{R}}
\newcommand{\n}{\mathbf{n}}
\newcommand{\m}{\mathbf{m}}
\newcommand{\x}{\mathbf{x}}
\newcommand{\y}{\mathbf{y}}
\newcommand{\z}{\mathbf{z}}
\newcommand{\w}{\mathbf{w}}
\newcommand{\h}{\mathbf{h}}
\newcommand{\g}{\mathbf{g}}

\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\pdp}[2]{\left(\frac{\partial #1}{\partial #2}\right)}
\newcommand{\grad}[1]{\nabla_{#1}}
\newcommand{\gradL}[1]{\nabla_{#1}\mathcal{L}}
\newcommand{\L}{\mathcal{L}}
\newcommand{\yhat}{\hat{\y}}

\uline{Published {{ date }}}
# {{ title }}

I've recently seem some graduate students have confusion about partial derivatives and
applying the chain rule. The following is a quiz I've written for my PhD
advisor's Image and Video Processing students. I will use it to illustrate the
proper application of the multi-dimensional chain-rule. The quiz question is as follows,

@@box-pink
@@content
Consider the following loss function, with input $\x[n]$, $1 \leq n \leq N$, and target $\y[n]$, $1\leq n \leq N$,

$$
\L(\y, \, \x; \, \h) = \frac{1}{2}\norm{\y - \h \ast \x}_2^2.
$$
where, $\h[m], ~ -M \leq 1 \leq M$ is a learnable 1D filter and $\ast$ denotes 1D convolution with zero-padding, i.e.,
$$
\h \ast \x \quad \Leftrightarrow \quad (\h \ast \x)[n] = \sum_{m=-M}^M \h[m] \x[n-m], \quad  1 \leq n \leq N.
$$
where $\x[n < 1] \equiv 0$ and $\x[n > N] \equiv 0$.

\uline{Derive the partial derivative},
$$
\pd{\L}{\h[m]} , \quad \text{ for } -M \leq m \leq M.
$$
@@
@@

Below is a solution that I would expect students to arrive at. It makes use of the scalar chain rule and 
doesn't worry about deriving Jacobians, as the course does not emphasize this perspective heavily.

\dropblue{solution1}{Solution:}{
    Let $\yhat = \h \ast \x$. Then,

    $$
    \begin{aligned}
        \pd{\L}{\h[m]} &= \pd{}{\h[m]} \left( \frac{1}{2}\sum_{i=1}^N \left( \y[i] - \yhat[i] \right)^2 \right)  \\
                      &= \sum_{i=1}^N \pd{\yhat[i]}{\h[m]} \left(\yhat[i] - \y[i] \right) \\
                      &= \sum_{i=1}^N \x[i-m] \left(\yhat[i] - \y[i] \right) \\
                      &= \sum_{i=1}^N \x[i-m] \left((\h \ast \x)[i] - \y[i] \right), \quad \text{for } -M \leq m \leq M.
    \end{aligned}
    $$

    Note that this may be interpreted as a convolution of a flipped version of
    $\x[n]$ with $(\yhat-\y)[n]$. To see this, let $\vec{\x}[n] = \x[-n]$. Then, 

    $$
    \begin{aligned}
    \pd{\L}{\h[m]} &= \sum_{i=1}^N \vec{\x}[m-i] \left(\yhat[i] - \y[i] \right),
    \quad \text{ for } -M \leq m \leq M \\
                  & \Leftrightarrow \\
    \left(\pd{\L}{\h}\right)[m] &= \left((\yhat - \y) \ast \vec{\x} \right)[m], 
    \quad \text{ for } -M \leq m \leq M 
    \end{aligned}
    $$

    Again, we assume zero-padding for $\y$ and $\yhat$.
}

## On using the multi-dimensional chain-rule
There are two distinct approaches to deriving this partial derivative: the Jacobian way or the scalar way.
I see many students tripping themselves up because they're aware of these two
methods but not fully aware on their distinction.

From preschool we are all familiar with the standard scalar chain rule of calculus. For
differentiable $f: \R \rightarrow \R$ and $g: \R \rightarrow \R$,
$$
\pd{(f\circ g)}{x} = f^\prime(g(x)) g^\prime(x) = \pd{f}{g}\Bigm\lvert_{g(x)} \pd{g}{x} \Bigm\lvert_{x}.
$$
It's this rule above that we directly employ in the above solution, by expanding the loss function in terms of 
its scalar variables, $\yhat[n]$ and $\y[n]$.

However, students also learn that a similar chain rule exists for vector input/output mappings. Namely,
for differentiable mappings $f: \R^K \rightarrow \R^M$ and $g: \R^N \rightarrow \R^K$,
\begin{equation} \label{eq:vec_chain}
\pd{(f\circ g)}{x} = \pd{f}{g}\Bigm\lvert_{g(x)} \pd{g}{x} \Bigm\lvert_{x},
\end{equation}

where $\pd{f}{g} \in \R^{M \times K}$ is the Jacobian matrix of $f$, defined element-wise as
$$
\pdp{f}{g}_{ij} = \pd{f_i}{g_j}, \quad 1 \leq i \leq M, \quad 1 \leq j \leq K,
$$
and an analagous definition for $\pd{g}{x} \in \R^{K \times N}$. As a sanity check, observe that 
the shapes of the matrix multiplication in \eqref{eq:vec_chain} work out, and that the Jacobian 
of $f \circ g$ is an $M \times N$ matrix.

Trouble then arises when students derive the elements of the Jacobian matrices in \eqref{eq:vec_chain} separately
and then forget to compose them using matrix multiplication, i.e.,

\begin{equation}
\pdp{f}{x}_{ij} = \sum_{k=1}^K \pdp{f}{g}_{ik} \pdp{g}{x}_{kj} = \sum_{k=1}^K \pd{f_i}{g_k} \pd{g_k}{x_j}.
\end{equation}

Students who have trouble will often try to do element-wise multiplication of
$\pd{f}{g}$ and $\pd{g}{x}$, even when the shapes don't make sense.

\dropblue{solution2}{Solution: the Jacobian way}{
    Let $\yhat = \h \ast \x$. Then,

    $$
    \pd{\L}{\h} = \pd{\L}{\yhat}\pd{\yhat}{\h},
    $$
    where $\pd{\L}{\h} \in \R^{1 \times (2M+1)}$, $\pd{\L}{\yhat} \in \R^{1 \times N}$, and 
    $\pd{\yhat}{\h} \in \R^{N \times (2M+1)}$.

    The Jacobian of the loss w.r.t $\yhat$ is,
    $$
    \begin{aligned}
    \pd{\L}{\yhat[j]} &= \yhat[j] - \y[j], \quad \text{for } 1 \leq j \leq N.
    \end{aligned}
    $$

    And the Jacobian of convolution w.r.t the kernel is,
    $$
    \begin{aligned}
    \pd{\yhat[i]}{\h[j]} &= \x[i-j], \quad \text{for } 1 \leq i \leq N, ~ -M \leq j \leq M.
    \end{aligned}
    $$

    Combining them using matrix multiplication we get,
    $$
    \begin{aligned}
    \pd{\L}{\h[m]} &= \sum_{i=1}^N \pd{\L}{\yhat[i]}\pd{\yhat[i]}{\h[m]} \\
        &= \sum_{i=1}^N \x[i-m](\yhat[i] - \y[i]), \quad \text{for } -M \leq m \leq M.
    \end{aligned}
    $$
}


