+++
title = "Lesson 2"
date = Date(2022, 08, 14)
hasmath = true
tags = ["dld"]
draft = false
descr = "Logic Gates, Boolean Algebra, and Combinatorial Circuits"
mintoclevel = 2
maxtoclevel = 2
+++

\newcommand{\not}{\overline}

The following lecture notes are adapted from 
those of Karol Wadolowski (CU EE'19).
# [ECE 150 Digital Logic Design](/teaching/dld): {{ title }}

Table of Contents:
\toc

#### Remark
This lecture differs from [the previous](/teachign/dld/lesson1) in that we are 
interpreting $0$ and $1$ as **boolean values**: **false** and **true**, not
inherently values indicating quantity. We will show that boolean algebra forms 
a very general framework, and circuits dervied from boolean expressions 
can be used to implement numerical arithmetic if we choose to interpret 
circuit inputs and outputs as belonging to the binary number system.

## Logic Gates
Logic gates are our tools of binary (True/False, Yes/No) decision making. Given
a set of binary inputs, desired outputs can be expressed via a combination of
the below fundamental gates.

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
either NANDs or NORs. This can have the benefit of simplifying chip design, 
ensuring equal **propagation delay** between all gates, or simplying using your entire chip!

## Boolean Algebra
Here we introduce how to manipulate and simplify boolean expressions symbolically.
We start with our assumed rules (postulates) concerning the NOT, AND, and OR operations.

\reference{Postulates of Boolean Algebra[^1]}{
\begin{align}
A + 0 &= A,       &\quad A1 &= A \qquad &\text{identity} \\
A + \not{A} &= 1, &\quad A\not{A} &= 0 \qquad &\text{complement} \\
A + B &= B + A,   &\quad AB &= BA \qquad &\text{commutative} \\
A + (B + C) &= (A+B) + C, &\quad A(BC) &= (AB)C \qquad &\text{associative} \\
A + BC &= (A+B)(A+C), &\quad A(B+C) &= AB + BC \qquad & \text{distributive}
\end{align}
}

From these postulates, the following theorems can be derived.

\reference{(some) Theorems of Boolean Algebra[^1]}{
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

To simplify an expression:
1. create a 2D grid of cells of inputs in rows and columns by gray-code
2. fill in cells with output values (0/1) or dont-cares (X)
3. group adjacent 1-cells in largest powers of 2 until all 1s are part of a
   group. Overlap is fine, and don't-cares can be part of a group. Grouping
   with wrap-around is possible.
4. Write output expression as a SOP where each term corresponds to a group, including inputs 
   which do not change within the group.

K-maps are best understood by examples. Here is a primer from the textbook:
\example{Textbook ex. 5-28}{
Simplify the sum-of-products expression,
$$ X = \not{A}B + \not{A}~\not{B}~\not{C} + AB\not{C} + A\not{B}~\not{C} $$
using both a K-map, and then again via boolean algebra rules.

**solution**: first, we can form the truth-table for the expression.
This can be done by brute force, or, more easily, by noting that each term in 
the SOP expression contributes to one-or-more "1s", with the remaining rows being zero.

Once we have a truth-table, forming the K-map is a simple rearrangement. 
Due to the gray-coding of the K-map, it's useful to do this by labeling which
cells correspond to which states.
\figenv{}{/assets/dld/imgs/txtbook_kmap.jpg}{width:100%}

Once the K-map is filled in, we follow the above steps. And group "1s" in 
the largest powers of 2. The final expression,
$$
X = \not{C} + \not{A}B,
$$
is far simplier, as intended.

We now verify that boolean algebra rules achieve the same result:
\begin{align}
X &= \not{A}B + \not{A}~\not{B}~\not{C} + AB\not{C} + A\not{B}~\not{C}  \\
&= \not{A}(B + \not{B}~\not{C}) + A\not{C}(B + \not{B}) & \text{distributive law} \\
&= \not{A}(B + \not{C}) + A\not{C} & \text{thm 4a} \\
&= \not{A}B + \not{C}(A + \not{A}) & \text{asccosiative + distributive laws} \\
&= \not{A}B + \not{C} & \text{complement law}
\end{align}

Clearly, both methods achieve the same results, though K-maps are a powerful 
graphical tool which may save time and headaches!
}

The next example illustrates two addtional concepts **don't-cares** and 
**K-map wrap-around**.

\example{7-segment display decoder}{
A **7-segment display** is 7 LEDs arranged to allow easy display of decimal symbols (and other 
symbols if you're tricky!). Below we show these 7 LEDs indexed, $a,b,\dots,g$, along 
with the decimal symbols $0-9$ as we wish to display them. Our goal for this
example is to is to obtain simplified boolean expressions for each LED given a
4-bit binary coded decimal (BCD) input, $ABCD$.

Below we show how to obtain expressions for $a$ and $b$ via K-maps. The
remaining LEDs are left as excercises.
\figenv{}{/assets/dld/imgs/7segment_kmap.jpg}{width:100%}

- Upon placing the truth-table values for a single output column (ex. $a$ or $b$) 
  into their K-map cells, we notice that not all states are accounted for. 
  For this example, we consider these states invalid, and thus label them as **don't-care** 
  states. When circling groups in our K-maps, we can include dont-care if it is advantagous in reducing the expression, or we can ignore them if they do not aid in circling "1s".

- The gray-coding used simply encodes the property that adjacent cells may only change 
  by one input. The **K-map wrap-around** property comes from the fact that the first and last rows/columns are only changing by one input, and hence should also be considered as *adjacent*. Geometrically, you can think of a K-map as [a grid on a torus](https://en.wikipedia.org/wiki/Karnaugh_map#/media/File:Karnaugh_map_torus.svg).
}

#### Remarks
- **products-of-sums** are the alternative to SOPs. They are equivalent by de Morgan's 
  theorem, but not as intuitive

## Combinatorial Circuits
With some familiarty of boolean algebra and logic diagrams, we can 
understand common combinatorial circuits used throughout digital systems.

### Half Adders, Full Adders
Adder circuits perform addition of numbers (e.x. [lesson 1](/teaching/dld/lesson1)). 
This generally involves interpreting two sets of boolean inputs $A = A_{N-1}\cdots A_1A_0$ and
$B = B_{N-1}\cdots B_1B_0$ as belonging to some number system, and passing them
through a set of logic circuits whose output can be interpreted as the sum of
those two inputs with respect to the number system.

The most fundamental of these circuits are those of *unsigned binary addition*,
from which addtion for other number systems can be built. [Recall](/teaching/dld/lesson1/#arithmetic), 
similar to decimal, addition of 2 bits can result in *carrying* a "1" to the next position.
A **Half-Adder** circuit takes into account this possibility, implementing the following 
truth table,

\figenv{}{/assets/dld/imgs/half_adder.jpg}{width:100%}

Intermediate symbol positions in addition can not only cause a carry operation
but they can recieve a carry symbol. We call a **Full-Adder** circuit one that 
is able to both accept and pass on a carry bit, implementing the following truth table.
As the name suggests, the full-adder circuit can be implemented via two half-adders.

\figenv{}{/assets/dld/imgs/full_adder.jpg}{width:100%}

An **N-bit Full-Adder** circuit, which performs unsigned binary addition of two N-bit binary numbers,
can be constructed using $N$ full-adder circuits as follows.

\figenv{}{/assets/dld/imgs/nbit_full_adder.jpg}{width:100%}

**Warning**: The above circuit incurs a **propagation delay** that is proportional to the number of bits in 
the circuit. This is due to the chaining of carry-out's to carry-in's. 
A [Carry Look-Ahead Adder](https://en.wikibooks.org/wiki/Digital_Circuits/Adders) can reduce this 
to a constant or logartihmic propagation delay via some extra logic concerning the carry bits.

### Multiplexers (Mux/Demux)
(*coming soon*)

#### Remarks:
- **Comparators** are circuits that take in binary numbers 
  and produce one of three outputs: greater-than, equality, or less-than. As an excercise, 
  derive a boolean expression for this circuit. 

- **Arithmetic Logic Unit (ALU)**: ALUs are the computational core of CPUs. They are able
  to perform several different combinatorial operations (addition, subtraction, bit shifting, etc.)
  in which additional selection inputs decide which of these operations is being used. 

#### References
[^1]: Santa-Clara University ELEN 021 ["Postulates and Theorems of Boolean Algebra"](http://www.ee.scu.edu/classes/1999winter/elen021/supp/BooleanAlgebra.html), 1999.

