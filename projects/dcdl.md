+++
title = "Deep Convolutional Dictionary Learning"
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

# {{title}}

\figenv{CDLNet Block Diagram.}{/assets/dcdl/cdlnet_blockdiagram2.png}{width:100%}

### Latest Update:
December 2021: Journal article preprint, 
*"CDLNet: Noise-Adaptive Convolutional Dictionary Learning Network for Blind Denoising and Demosaicing"*, avilable: [https://arxiv.org/abs/2112.00913](https://arxiv.org/abs/2112.00913).

\toc

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
task-driven fashion, amenable to any linear inverse-problem. Interpretability of
such networks allow us to further extend the framework for the specific signal
class and generalization requirements at hand.

### Participants
- Yao Wang, Advising Professor, [Lab Page](https://wp.nyu.edu/videolab/)
- [Nikola Janjušević](https://nikopj.github.io), Ph.D. student
- [Amir Khalilian](https://amirhkhalilian.github.io/), Ph.D. student

## Highlight: Generalization in Denoising
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
models either fail or introduce articfacts.

\figenv{CDLNet is able to generalize outside its training noise-level range,
whereas black-box neural networks fail.}{/assets/dcdl/gray_generalize_plot.png}{width:65%}
\figenv{}{/assets/dcdl/gray_visual.png}{width:100%}

This generalization characteristic is further demonstrated for the CDLNet
architecture extended to color image denoising,
joint-denoising-and-demosiacing, and unsupervised learning of denoising.

### Joint Denoising and Demosaicing
CDLNet extended to the JDD task is able to achieve state-of-the-art results with a single model, out-performing black box neural networks.
\figenv{PSNR Comparison against state-of-the-art JDD models on the Urban100/MIT moire datasets}{/assets/dcdl/JDD_table.png}{width:90%}

The results of this section are detailed in, [*"CDLNet: Noise-Adaptive Convolutional Dictionary Learning Network for Blind Denoising and Demosaicing"*](https://arxiv.org/abs/2112.00913).

## Progress
- *In December 2021*, we published a journal paper style preprint where we've improved our 
  network's denoising generalization results and extended them to the tasks of joint-denoising-and-demosaicing (JDD) 
  and unsupervised learning. Notably, our network obtains state-of-the-art results in JDD with a single model.
  The article is available on Arxiv: [*"CDLNet: Noise-Adaptive Convolutional Dictionary Learning Network for Blind Denoising and Demosaicing"*](https://arxiv.org/abs/2112.00913).
- *In March 2021*, we published a conference paper style preprint where we demonstrate
  that CDLNet's interpretable construction may be leveraged to yeild denoising robustness
  in noise-level mismatch between training and inference. The article is available on Arxiv: 
  [*"CDLNet: Robust and Interpretable Denoising Through Deep Convolutional Dictionary Learning"*](https://arxiv.org/abs/2103.04779).
- *In January 2021*, we presented updated results regarding 
  competitive denoising performance against state-of-the-art deep-learning
  models and leveraging the interpretability of CDLNet to improve generalization in
  blind denoising. Our poster is available
  [here](/assets/dcdl/CDLNetPosterWireless21.pdf).
- *In April 2020*, we presented some preliminary results at the NYU Wireless
  Industrial Affiliates Board Meeting. Check out our poster
  [here](/assets/dcdl/CDLNetPosterWireless20.pdf).

