+++
title = "The Convolutional Dictionary Learning Network"
date = Date(2021, 03, 08)
hascode = false
rss = "CDLNet"
tags = ["research"]
hasmath = true
mintoclevel=2
maxtoclevel=2
descr = """![](/assets/dcdl/cdlnet_blockdiagram2.png)
In this project, we explore an interpretable Deep Learning architecture for
image restoration based on an unrolled convolutional dictionary learning model.
More specifically, we leverage the LISTA framework to obtain approximate
convolutional sparse codes, followed by a synthesis from a convolutional
dictionary. We call this architecture **CDLNet**. 
"""
+++

\newcommand{\x}{\mathbf{x}}

# {{title}}

\figenv{CDLNet Block Diagram.}{/assets/dcdl/cdlnet_blockdiagram2.png}{width:100%}

\toc

### Latest Updates:
April 2022: 
- [*CDLNet*](https://ieeexplore.ieee.org/document/9769957) accepted into the
  \uline{IEEE Open Journal of Signal Processing}!
- Preprint published: [*"Gabor is Enough: Interpretable Deep Denoising with a Gabor Synthesis Dictionary Prior"*](https://arxiv.org/abs/2204.11146). 

## Project Overview
Sparse representation is a proven and powerful prior for natural images and
restoration tasks (such as denoising, deblurring, in-painting, etc.) involving
them. More than simply finding these representations, learning an over-complete
dictionary for sparse signal representation from degraded signals have been
shown to be effective models. Furthermore, the convolutional dictionary learning
(CDL) model seeks to represent the global signal via a translated local
dictionary. This offers a more holistic approach for natural image
representation compared to inherently suboptimal patch-processing methods. The
dictionary learning problem is traditionally solved by iteratively compute
spare-codes (representations) for a fixed dictionary, and subsequently updating
the dictionary accordingly. 

In this project, **we explore an interpretable Deep
Learning architecture for image restoration based on an unrolled CDL model**. More
specifically, we leverage the LISTA framework to obtain approximate
convolutional sparse codes, followed by a synthesis from a convolutional
dictionary. We call this architecture **CDLNet**. The network is trained in a
task-driven fashion, amenable to any linear inverse-problem. We believe that interpretable 
network construction will yield greater insight and novel capabilities.

### Participants
- Yao Wang, Advising Professor, [Lab Page](https://wp.nyu.edu/videolab/)
- [Nikola Janjušević](https://nikopj.github.io), Ph.D. student
- [Amir Khalilian](https://amirhkhalilian.github.io/), Ph.D. student

## Generalization in Denoising
The derivation of the CDLNet architecture allows us to understand the subband
thresholds, $\tau^{(k)} \in \R_+^M$, of the soft-thresholding operator as
implicitly being a function of the input noise-level $\sigma$. We thus propose an affine parameterization,

\begin{equation}
\tau^{(k)} = \tau_0^{(k)} + \tau_1^{(k)}\sigma
\end{equation}

to *explicitly model noise-level adaptivity within each layer of the network*.
This is in stark contrast to the *implicitly defined noise-level adaptivity of
common black-box neural networks*, which either account for noise only via
training on a noise range (ex. DnCNN), or additionally presented the estimated
input noise-level as an input to the network (ex. FFDNet). As shown in the
figures below, CDLNet's explicitly defined noise-level adaptivity allows for
near-perfect generalization outside its training range, whereas the black box
models either fail or introduce artifacts.

\figenv{CDLNet is able to generalize outside its training noise-level range,
whereas black-box neural networks fail.}{/assets/dcdl/gray_generalize_plot.png}{width:65%}
\figenv{}{/assets/dcdl/gray_visual.png}{width:100%}

This generalization characteristic is further demonstrated for the CDLNet
architecture extended to color image denoising,
joint-denoising-and-demosaicing, and unsupervised learning of denoising.

### Joint Denoising and Demosaicing
CDLNet extended to the JDD task is able to achieve state-of-the-art results with a single model, out-performing black box neural networks.
\figenv{PSNR comparison against state-of-the-art JDD models on the Urban100/MIT moire datasets}{/assets/dcdl/JDD_table.png}{width:90%}

The results of this section are detailed in, [*"CDLNet: Noise-Adaptive Convolutional Dictionary Learning Network for Blind Denoising and Demosaicing"*](https://arxiv.org/abs/2112.00913).

See our [supplementary material](/notes/cdlnet_supp) with animations of filters, thresholds, and sparse codes across layers.

## Gabor is Enough!
\figenv{The GDLNet architecture with Mixture of Gabor filters.}{/assets/dcdl/GDLNet.png}{width:100%}

Gabor filters (Gaussian $\times$ cosine) have a long history neural networks.
Cat eye-cells have been shown to have Gabor-like frequency responses, and the
learned filters at the early stages of the AlexNet classifier are noted to be
Gabor-like as well. We noticed that the trained filters of CDLNet also appear
Gabor-like and wondered, "Can Gabor-like be replaced with Gabor?". And so we
parameterized *each and every* filter of CDLNet as a 2D real Gabor function, 

\begin{equation}
g(\x; \phi) = \alpha e^{-\norm{\mathbf{a} \circ \x}_2^2} \cos(\mathbf{\omega}_0^T \x + \psi),
\end{equation}

with $\phi = (\alpha, \mathbf{a}, \mathbf{\omega}_0, \psi) \in \R^6$ as learnable parameters.
We also considered *mixture of Gabor* (MoG) filters, i.e. each filter as sum of Gabor filters. 
We call this network GDLNet. Surprisingly, with just MoG=1, GDLNet can achieve
competitive results with state-of-the-art CNN denoisers (see table below).

\figenv{PSNR comparison against grayscale denoisers on BSD68 testset.}{/assets/dcdl/gdlnet_table.png}{width:70%}

Our results suggest that the mechanisms behind low-level image processing neural networks need not 
be more complex than real Gabor filterbanks. Check out our preprint, [*"Gabor is Enough:
Interpretable Deep Denoising with a Gabor Synthesis Dictionary
Prior"*](https://arxiv.org/abs/2204.11146), for more results and information.

## Timeline
- *In April 2022*, *CDLNet* was accpeted into [IEEE Open Journal of Signal
  Processing](https://ieeexplore.ieee.org/document/9769957). We also published a
  preprint on parameterizing the filters of CDLNet with 2D real Gabor
  functions, [*"Gabor is Enough: Interpretable Deep Denoising with a Gabor
  Synthesis Dictionary Prior"*](https://arxiv.org/abs/2204.11146). 
- *In December 2021*, we published a journal paper style preprint where we've improved our 
  network's denoising generalization results and extended them to the tasks of joint-denoising-and-demosaicing (JDD) 
  and unsupervised learning. Notably, our network obtains state-of-the-art results in JDD with a single model.
  The article is available on arxiv: [*"CDLNet: Noise-Adaptive Convolutional Dictionary Learning Network for Blind Denoising and Demosaicing"*](https://arxiv.org/abs/2112.00913).
- *In March 2021*, we published a conference paper style preprint where we demonstrate
  that CDLNet's interpretable construction may be leveraged to yield denoising robustness
  in noise-level mismatch between training and inference. The article is available on arxiv: 
  [*"CDLNet: Robust and Interpretable Denoising Through Deep Convolutional Dictionary Learning"*](https://arxiv.org/abs/2103.04779).
- *In January 2021*, we presented updated results regarding 
  competitive denoising performance against state-of-the-art deep-learning
  models and leveraging the interpretability of CDLNet to improve generalization in
  blind denoising. Our poster is available
  [here](/assets/dcdl/CDLNetPosterWireless21.pdf).
- *In April 2020*, we presented some preliminary results at the NYU Wireless
  Industrial Affiliates Board Meeting. Check out our poster
  [here](/assets/dcdl/CDLNetPosterWireless20.pdf).

