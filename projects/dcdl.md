+++
title = "Deep Convolutional Dictionary Learning"
date = Date(2021, 03, 08)
hascode = false
rss = "CDLNet"
tags = ["research"]
descr = """![](/assets/dcdl/cdlnet_blockdiagram.png)

In this project, we explore an interpretable Deep Learning architecture for
image restoration based on an unrolled convolutional dictionary learning model.
More specifically, we leverage the LISTA framework to obtain approximate
convolutional sparse codes, followed by a synthesis from a convolutional
dictionary. We call this architecture **CDLNet**. 
"""
+++

# {{title}}

\figenv{CDLNet Block Diagram.}{/assets/dcdl/cdlnet_blockdiagram.png}{width:100%}

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

## Participants
- Yao Wang, Advising Professor, [Lab Page](https://wp.nyu.edu/videolab/)
- [Nikola Janjušević](https://nikopj.github.io), Ph.D. student
- [Amir Khalilian](https://amirhkhalilian.github.io/), Ph.D. student

## Recent Progress
- *In March 2021*, we published a preprint version of our, where we demonstrate
  that CDLNet's interpretable construction may be leveraged to yeild denoising robustness
  in noise-level mismatch between training and inference. The article is available on Arxiv: 
  [https://arxiv.org/abs/2103.04779](https://arxiv.org/abs/2103.04779).
- *In January 2021*, we presented updated results regarding 
  competitive denoising performance against state-of-the-art deep-learning
  models and leveraging the interpretability of CDLNet to improve generalization in
  blind denoising. Our poster is available
  [here](/assets/dcdl/CDLNetPosterWireless21.pdf).
- *In April 2020*, we presented some preliminary results at the NYU Wireless
  Industrial Affiliates Board Meeting. Check out our poster
  [here](/assets/dcdl/CDLNetPosterWireless20.pdf).

