+++
title = "Note: ADMM in scaled form"
date = Date(2021, 05, 24)
hasmath = true
tags = ["notes", "optimization"]
descr = ""
+++

# Scaled form ADMM

The alternating direction method of multipliers (ADMM) algorithm[^1] solves problems
of the form,
\begin{eqnarray}
	&\minimize{} && f(x) + g(z) \\
	&\subto && Ax + Bz = c
\end{eqnarray}

The iterates of ADMM are defined by the augmented Lagrangian,

\begin{equation}
	L_{\rho}(x,z,y) = f(x) + g(z) + y^\top(Ax + Bz - c) +
	(\rho/2)\norm{Ax+Bz-c}_2^2,
\end{equation}

and consist of,

\begin{align}
	x^{k+1} &\coloneqq \argmin{x} L_{\rho}(x,z^k,y^k) \\
	z^{k+1} &\coloneqq \argmin{z} L_{\rho}(x^{k+1},z,y^k) \\
	y^{k+1} &\coloneqq y^k + \rho(Ax^{k+1} + Bz^{k+1} - c)
\end{align}

Note that the method of multipliers algorithm considers the update of $x,z$
jointly, whereas ADMM takes a Gauss-Seidel pass. An often more conveinient
*scaled form* may be obtained by completing the square with the dual
variable and residual ($r = Ax + Bz - c$), and defining the *\textcolor{blue}{scaled dual variable}* $u =
(1/\rho)y$.

\begin{eqnarray}
	y^\top r + (\rho/2) \norm{r}^2_2 &=& \frac{\rho}{2}\left[
	\frac{2}{\rho}y^\top r + r^\top r + \frac{1}{\rho^2}y^\top y 
	- \frac{1}{\rho^2}y^\top y 
	\right] \\
	&=& \frac{\rho}{2}\norm{r + u}_2^2 - \frac{\rho}{2}\norm{u}^2_2
\end{eqnarray}

With the scaled dual variable, our augmented Lagrangian is written as,
\begin{equation}
	L_{\rho}(x,z,u) = f(x) + g(z) + (\rho/2)\norm{Ax + Bz - c + u}_2^2 -
	(\rho/2)\norm{u}_2^2,
\end{equation}

and the ADMM iterates are expressed as,

@@algblock
**Scaled Form ADMM**
\begin{align}
	x^{k+1} &\coloneqq \argmin{x} f(x) + (\rho/2)\norm{Ax + Bz^k - c + u^k}_2^2\\
	z^{k+1} &\coloneqq \argmin{z} g(z) + (\rho/2)\norm{Ax^{k+1} + Bz - c + u^k}_2^2\\
	u^{k+1} &\coloneqq u^k + Ax^{k+1} + Bz^{k+1} - c
\end{align}
@@

The ADMM iterates written in scaled form are often more amenable to being
written with proximal operators.

[^1]: [For more information](https://stanford.edu/~boyd/admm.html).
