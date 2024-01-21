+++
title = "Note: 2-set best approximation"
date = Date(2022, 05, 10)
hasmath = true
tags = ["notes", "optimization"]
draft = false
descr = ""
+++

# ADMM for a 2-set "*best approximation problem*"

The following comes from my own derivations, but the results can be see in [^1] equation (7).

Suppose we have a vector and want to project it onto to intersection of two sets $C_1 \cap C_2$.
This projection may not have a closed form, but if projection onto each set
separately is cheap/closed-form, we're in luck. We begin by converting our starting formulation
to something ADMM-able via indicator functions,

\begin{eqnarray}
	&\minimize{x \, \in \, C_1 \cap C_2} && \norm{x - a}_2^2 \\
	& \Leftrightarrow  && \\
	&\minimize{x,\, z} && \frac{1}{2}\norm{x-a}_2^2 + \iota_{C_1}(x) + \iota_{C_2}(z) \\
	&\subto && x-z = 0
\end{eqnarray}

Our [scaled-form](/notes/admm_scaled) augmented Lagrangian is then,
\begin{eqnarray}
L_{\rho}(x,z,u) &=& \frac{1}{2}\norm{x - a}_2^2 + \iota_{C_1}(x) + \iota_{C_2}(z) 
+ \frac{\rho}{2}\norm{x-z+u}_2^2 + \frac{\rho}{2}\norm{u}_2^2
\end{eqnarray}

with scaled dual variable $u$. From the Lagrangian we can see that our $z$-update is
straightforward[^2], but the $x$-update requires some manipulation. If we
complete the square w.r.t $x$,

\begin{eqnarray}
L_{\rho}(x,z,u) 
	&=& \frac{1}{2}(x^Tx -2x^Ta) + \iota_{C_1}(x)
	+ \frac{\rho}{2}( x^Tx -2x^T(z-u)) + \mathrm{const} \\
	&=& \frac{1+\rho}{2}\left( x^Tx -\frac{2}{1+\rho} x^T(a + \rho(z-u)) 
	+ \frac{1}{(1+\rho)^2}\norm{a + \rho(z-u)}_2^2\right) + \iota_{C_1}(x) + \mathrm{const} \\
	&=& \iota_{C_1}(x) + \frac{1+\rho}{2}\norm{ x - \frac{a + \rho(z-u)}{1+\rho}}_2^2 + \mathrm{const}
\end{eqnarray}
we see that its update is also a projection, with inputs scaled by the
step-size $\rho$ (note $\mathrm{const}$ is only a constant w.r.t $x$).

The resulting ADMM algorithm for the 2-set best approximation problem is as follows,
with $z^{(0)} = \mathrm{proj}_{C_2}(a)$, $u^{(0)}=0$,

\begin{eqnarray}
	x^{k+1} &\coloneqq& \mathrm{proj}_{C_1}\left(\frac{a + \rho(z^k-u^k)}{1+\rho}\right) \\
	z^{k+1} &\coloneqq& \mathrm{proj}_{C_2}(x^{k+1} + u^k) \\
	u^{k+1} &\coloneqq& u^k + x^{k+1} - z^{k+1}
\end{eqnarray}

This is reminiscent of [Dykstra's projection
algorithm](https://en.wikipedia.org/wiki/Dykstra%27s_projection_algorithm) and
[POCS](https://en.wikipedia.org/wiki/Projections_onto_convex_sets), but
different from Dykstra's we have a step-size $\rho$ to play with for
accelerated convergence.


[^1]: See [*"Dykstra's Algorithm, ADMM, and Coordinate Descent: Connections, Insights, and Extensions"*](https://api.semanticscholar.org/CorpusID:7703985) for further insights and extensions. Notably, the $d$-set best approximation problem.

[^2]: The proximal operator of indicator function of a set $C$ is orthogonal-projection onto $C$.

