+++
title = "How to think of Conv-Layers in Neural Networks"
draft = false
date = Date(2022, 12, 11)
tags = ["deep learning"]
hasmath = true
descr = """
Convolutional Neural Networks' building blocks aren't just performing the convolution you learned in DSP.
In my opinion, the best way to think of these layers is as a channel-wise matrix-vector multiplication of convolutions.
~~~
<img alt="convolution blocks" src="/assets/conv/conv_blocks.svg" style="width:50%" class="center" />
~~~
"""
+++


\newcommand{\R}{\mathbb{R}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\n}{\mathbf{n}}
\newcommand{\m}{\mathbf{m}}
\newcommand{\x}{\mathbf{x}}
\newcommand{\y}{\mathbf{y}}
\newcommand{\z}{\mathbf{z}}
\newcommand{\b}{\mathbf{b}}
\newcommand{\h}{\mathbf{h}}
\newcommand{\H}{\mathbf{H}}


\uline{Published {{ date }}}
# {{ title }}
Convolutional Neural Networks' building blocks aren't just performing the
convolution you learned in digital signal processing class.
In my opinion, the best way to think of these layers is as a channel-wise
matrix-vector multiplication of convolutions.


## Notation 
Denote our discrete signals (time-series, images, videos, etc.) as 
vectors in $\R^{CN}$, where $N$ is the total number of pixels in our
spatio-temporal dimensions (1, 2, 3, for time, space, space-time resp.), and we
consider our signal to be _vector-valued_ at each pixel location. Notationally,
we write

- $\x \in \R^{CN}$, our $N$-pixel, $C$-vector-valued, d-dimensional signal 
- $\x[\n] \in \R^C$, a __pixel__ of our signal $\x$, indexed at location $\n \in \Z^d$
- $\x_i \in \R^N$, the d-dimensional $i$-th __channel__ of signal $\x$, of length $N$
- $\x_i[\n] \in \R$, the value of the $i$-th channel of $\x$ at pixel $\n$.

For images in particular, we often refer to $\x_i$ as a __feature-map__.
When $C=1$, we refer to $\x$ as a _scalar-valued_ signal. Mono-channel audio and grayscale 
images/videos are all scalar-valued signals. 
Stereo-audio ($C=2$) and color images/videos ($C=3$) are vector-valued signals. More exotic channel numbers arise in many 
scientific instruments, such as EEG where every electrode may be considered channel of a brain time-series signal, 
and Multi-coil MRI where each RF-coil contributes a channel to the vector valued image.

Using our notation, familiar discrete time/space convolution for scalar-valued signals can be written as

$$
(\x \ast \h)[\n] = \sum_{\m \in \Z^d} \h[\m]\,\x[\n-\m], \quad \x \in \R^{N_x}, \, \h \in \R^{N_h}, \, \n \in \Z^d,
$$

where $\x$ and $\h$ may be of different sizes $N_x$ and $N_h$, and our output may be of various sizes
based on choices of padding and dimension of the signals $d$. Without loss of
generality, we will ignore the relationship between spatio-temporal sizes and
instead focus on channels.

## Conv-layers

The [documentation of popular Deep-Learning libraries such as
PyTorch](https://pytorch.org/docs/1.13/generated/torch.nn.Conv2d.html?highlight=conv2d#torch.nn.Conv2d)
describe a __conv-layer__ as follows,

$$
\y_i = \b_i + \sum_{j=1}^{C_{\mathrm{in}}} \h_{ij} \ast \x_j, \quad \x \in \R^{C_{\mathrm{in}}N_x}, \,
\h \in \R^{C_{\mathrm{in}}C_{\mathrm{out}}N_h}, \,
\y \in \R^{C_{\mathrm{out}}N_y}, \,
\b \in \R^{C_{\mathrm{out}}},
$$

where $\x, \h, \b, \y$ are our input, conv-kernel weights, conv-bias weights, and output respectively. 
Clearly, a deep-learning conv-layer involves potentially more than just scalar convolution.
We can see that our input and output signals have a differing number of channels ($C_{\mathrm{in}}$ and
$C_{\mathrm{out}}$), and __our conv-kernel $\h$ is a matrix of $C_{\mathrm{in}} \times C_{\mathrm{out}}$ scalar kernels__, 
each of spatio-temporal size $N_h$. Indeed, the indexing in the above equation looks very reminiscent of 
matrix-vector (mat-vec) multiplication. However, instead of indexing multiplying scalars, _the conv-layer equation indexs
convolves channels._ We can write this mat-vec interpretation of the conv-layer as follows,

\begin{eqnarray}
\begin{bmatrix}
\y_1 \\ \y_2 \\ \vdots \\ \y_{C_{\mathrm{out}}}
\end{bmatrix}

&=&

\begin{bmatrix}
b_1 \\ b_2 \\ \vdots \\ b_{C_{\mathrm{out}}}
\end{bmatrix}

+

\begin{bmatrix}
\h_{11} & \h_{12} & \cdots & \h_{1C_{\mathrm{in}}} \\
\h_{21} & \h_{22} & \cdots &  \h_{2C_{\mathrm{in}}} \\
\vdots & \vdots & \ddots & \vdots \\
\h_{C_{\mathrm{out}}1} &  \h_{C_{\mathrm{out}}2} & \cdots &  \h_{C_{\mathrm{out}}C_{\mathrm{in}}} 
\end{bmatrix}

\begin{bmatrix}
\x_1 \\ \x_2 \\ \vdots \\ \x_{C_{\mathrm{in}}}
\end{bmatrix} 
,
\end{eqnarray}

where the usual multiplication and addition is replaced with convolution and addition.
A more colorful representation is given below, where squares represent feature-maps and the colored circles 
represent scalars. Note that $\H_{ij} = \h_{ij}$.

\figenv{"Channel-wise mat-vec convolution" of standard deep-learning Conv-layer.}{/assets/conv/conv_blocks.svg}{width:60%}

### Groups
Its now standard for libraries to have a `groups` parameter. Our channel-wise 
mat-vec visual makes understanding this parameter much easier. By default, `groups=1`
and we have our standard conv layer as above. In general, when groups$=G$, we divide the rows 
and columns of our kernel matrix $\H$ into $G$ rows and columns and only allow a single 
group of kernels in each division of $\H$. The figure below shows an example of this.

\figenv{Varying the groups parameter of a 4x4 channel conv kernel matrix.}{/assets/conv/conv_groups.svg}{width:75%}

This is equivalent to dividing our input signal into $G$ groups of channel-size $C_{\mathrm{in}}/G$, 
passing it through a conv-layer of size $C_{\mathrm{out}}/G \times C_{\mathrm{in}}/G$, and concatenating 
the results channel-wise. Hence, it is required that $\H$ is divisible by $G$ in row and columns.

####
I hope this makes starting out with convolutional neural networks a little easier.
In a later post, I'll go over deep-learning's conv-transposed layers, which require 
us to look at the matrix representation of convolution to understand them best.

