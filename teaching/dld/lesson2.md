+++
title = "Lesson 2"
date = Date(2022, 08, 14)
hasmath = true
tags = ["dld"]
draft = true
descr = "Logic Gates and Boolean Algebra"
mintoclevel = 2
maxtoclevel = 2
+++

\newcommand{\not}{\overline}

# [ECE 150 Digital Logic Design](/teaching/dld): {{ title }}

Table of Contents:
\toc

## Logic Gates
Logic gates are our tools of binary decision making. Given a set of binary 
inputs, desired outputs can be expressed via a combination of the below fundamental gates.

\figenv{}{/assets/dld/imgs/logic_symbols2.png}{width:80%}
```
 NOT           OR             AND            XOR            NOR            NAND
-----        -------        -------        -------        -------        -------
A | Z        A B | Z        A B | Z        A B | Z        A B | Z        A B | Z
=====        =======        =======        =======        =======        =======
0 | 1        0 0 | 0        0 0 | 0        0 0 | 0        0 0 | 1        0 0 | 1
1 | 0        0 1 | 1        0 1 | 0        0 1 | 1        0 1 | 0        0 1 | 1
             1 0 | 1        1 0 | 0        1 0 | 1        1 0 | 0        1 0 | 1
             1 1 | 1        1 1 | 1        1 1 | 0        1 1 | 0        1 1 | 0
```
\figenv{}{/assets/dld/imgs/logic_symbols1.png}{width:80%}

Each gate has an associated **logic symbol** and **truth-table**, and
**algebraic representation**. They represent both mathematical operations and
idealized circuit elements.

\example{Example logic diagram with two inputs (A, B) and two outputs (S, C)}{
<!-- \hoverfig{}{/assets/dld/imgs/ex_logic_diagram1.png}{/assets/dld/imgs/ex_logic_diagram2.png}{width:80%} -->
\figenv{}{/assets/dld/imgs/logic_diagram.png}{width:100%}
}

We call NANDs and NORs **universal gates** as all others can be built exclusively using 
either NANDs or NORs. This can have the benefit of simplifying chip design, or 
ensuring equal **propagation delay** between all gates. 

## Boolean Algebra
Here we introduce how to manipulate and simplify boolean expressions symbolically.
We start with our assumed rules (postulates) concerning the NOT, AND, and OR operations.

\reference{Postulates of Boolean Algebra}{
\begin{align}
A + 0 &= A,       &\quad A1 &= A \qquad &\text{identity} \\
A + \not{A} &= 1, &\quad A\not{A} &= 0 \qquad &\text{complement} \\
A + B &= B + A,   &\quad AB &= BA \qquad &\text{commutative} \\
A + (B + C) &= (A+B) + C, &\quad A(BC) &= (AB)C \qquad &\text{associative} \\
A + BC &= (A+B)(A+C), &\quad A(B+C) &= AB + BC \qquad & \text{distributive}
\end{align}
}

From these postulates, the following theorems can be derived.

\reference{(some) Theorems of Boolean Algebra}{
\begin{align}
A + A &= A, &\qquad AA &= A \qquad &\text{(1)}\\
A + 1 &= 1, &\qquad A0 &= 0 \qquad &\text{(2)}\\
A + AB &= A, &\qquad A(A + B) &= A \qquad                  &\text{(3)}\\
A + \not{A}B &= A + B, &\qquad A(\not{A} + B) &= AB \qquad &\text{(4)}\\
AB + \not{A}C + BC &= AB + \not{A}C, &\qquad & &\text{(5)} \\
\not{A + B} &= \not{A}~\not{B}, &\qquad \not{AB} &= \not{A} + \not{B} &\text{(de Morgan's)}
\end{align}
}

These theorems can be proved easily via truth tables, but it is 
good excersice to become comfortable with symbolic manipulation
for simplifying expressions.

Proofs:
```
(1)                           (2) 
A | A+A       A | AA          A | A+1       A | A0
=========     ========        =========     ========
0 | 0+0=0     0 | 00=0        0 | 0+1=1     0 | 00=0
1 | 1+1=1     1 | 11=1        1 | 1+1=1     1 | 10=0 
<=> A+A = A   <=> AA = A      <=> A+1 = 1   <=> A0 = 0
```

(3a)
\begin{align}
A + AB &= A1 + AB &&\text{identity} \\
&= A( 1 + B) &&\text{distributive} \\
&= A1  &&\text{thm (2)} \\
&= A &&\text{identity}
\end{align}

(3b)
\begin{align}
A(A+B) &= AA + AB && \text{distributive} \\
&= A + AB && \text{thm (1)} \\
&= A && \text{thm (3a)}
\end{align}

(4a)
\begin{align}
A + \not{A}B &= A + AB + \not{A}B && \text{thm (3a)} \\
&= A + (A +\not{A})B && \text{distributive} \\
&= A + B && \text{complement}
\end{align}

(4b)
\begin{align}
A(\not{A}+B) &= A\not{A} + AB && \text{distributive} \\
&= AB && \text{complement}
\end{align}

(5)
\begin{align}
AB + \not{A}C + BC &= AB + \not{A}C + (A+\not{A})BC \\
&= A(B + BC) + \not{A}(C + BC) \\
&= AB + \not{A}C && \text{thm (3a)}
\end{align}

(de Morgan's)
```
(a)                           (b)
A B | !(A+B) | !A!B           A B | !(AB) | !A+!B
====================          ===================
0 0 |   1    |  1             0 0 |   1   |  1
0 1 |   0    |  0             0 1 |   1   |  1
1 0 |   0    |  0             1 0 |   1   |  1
1 1 |   0    |  0             1 1 |   0   |  0
<=> !(A+B) = !A!B             <=> !(AB) = !A+!B
```

An easy way to remember de Morgan's theorem is that NOT distributes over (or
factors out of) AND/OR by replacing with OR/AND.

With these theorems, we can now simplify the expression from the example circuit above.

\begin{align}
Z &= AB + \not{B(\not{A}\oplus C)} && \\
&= AB + \not{B(\not{A}~\not{C} + AC)} && \text{def. of XOR} \\
&= AB + \not{B} + \not{(\not{A}~\not{C} + AC)} && \text{de Morgan's} \\
&= A + \not{B} + \not{(\not{A}~\not{C} + AC)} && \text{thm. 4a} \\
&= A + \not{B} + \not{(\not{A}~\not{C})}~\not{(AC)} && \text{de Morgan's} \\
&= A + \not{B} + (A + C)(\not{A} + \not{C}) && \text{de Morgan's} \\
&= A + \not{B} + A\not{C} + \not{A}C && \text{distributive + complement} \\
&= A(1+\not{C}) + \not{B} + \not{A}C && \text{distributive} \\
&= A + \not{A}C + \not{B} && \text{thm. 2a} \\
&= A + \not{B} + C && \text{thm. 4a}
\end{align}

Using boolean algebra, we've gone from a 5 gates to 3, and obtained a much 
more simple expression.

### Karnaugh Maps
**K-maps** are a graphical tool used for boolean expression simplification.
The output of a K-map simplification is a **sum-of-products** expression, 
i.e. and OR of ANDS, ex. $Z = \not{A}BC + A\not{C} + AB$.

K-maps work off the property that $A + \not{A} = 1$ and **gray-code** -- enumerating 
your inputs by only changing one symbol at a time.

To simplify an expression
1. create a 2D grid of cells of inputs in rows and columns by gray-code
2. fill in cells with output values (0/1) or dont-cares (X)
3. group adjacent 1-cells in largest powers of 2 until all 1s are part of a
   group. Overlap is fine, and don't-cares can be part of a group. Grouping
   with wrap-around is possible.
4. Write output expression as a SOP where each term corresponds to a group, including inputs 
which do not change within the group.

\example{7-segment display decoder}{

}



- min/max terms, sop/pos
- gray code
- example
- powers of 2, don't care
- think of kmap as torus



