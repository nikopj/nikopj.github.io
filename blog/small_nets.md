+++
title = "How do black-box denoisers perform at the lower parameter-count regime, anyway?"
draft = false
date = Date(2022, 08, 14)
tags = ["deep learning"]
descr = """
So-called interpretably constructed deep neural networks often sell their
methods by showing near state-of-the-art performance for only a fraction of the
parameter count of black-box networks. However, can we consider these fair
comparisons when the number of learned parameter counts are not matched?
"""
+++


\uline{Published ...? This post is in progress.}
# {{ title }}

{{ descr }}

## Background
In this post, we're talking about DeNoising neural networks -- parameterized
functions $f_\Theta$ that take an image contaminated with random noise ex. AWGN,

$$y = x + \nu, ~ \nu \sim \mathcal{N}(0,\sigma^2),$$

and return an estimate of the underlying signal, $\hat{x} = f_\Theta(y)$. These
DNNs are often trained by adding noise to a dataset of natural images, for
example the Berkely Segmentation Dataset (BSD), and optimizing their parameters
$\Theta$ ("training") via stochastic gradient descent on the error (loss)
between the estimated clean image and the ground truth, $\mathcal{L}(x, \,
f_\Theta(y))$.

## What makes a fair comparison?
In a broad sense, the "free variables" of these experiments are 
- training scheme
    * dataset
    * learning rate
- network architecture (i.e. what operations are done inside $f_\Theta$)
    * functional form of layers (ex. $x^{(k+1)} = \sigma(Wx^{(k)} + b)$)
    * hyper-parameters (num. layers, num. filters, etc.)

In the papers cited below, the same dataset (BSD432) is used to train 
each network. Training schemes may differ, but it is generally assumed that 
each team has done their best to maximize the performance of their network.

Novel functional forms are almost always the meat of an image denoising paper's
proposed methods. The point is to demonstrate a "better" way of understanding 
denoising (via neural networks), or showing that a new tool can be used effectively.

A simple and convincing experiment to highlight this would be to ,
> show the same/better performance to previously published methods using a less/equal
> number of "X", 
where "X" is most commonly floating point operations (flops), unit of time,
or learned parameters. 

Flops and processing time are self explanatory benifits -- and may not be
equivalent due to parallelizability of the proposed method. Paying attention to
learned parameter counts has some tangible benefits in terms of physically
storing the neural network in memory, but it can also comment on the effectiveness
of the proposed architecture in an [Occam's Razor](https://en.wikipedia.org/wiki/Occam%27s_razor) 
sense. Here, we equate a low learned parameter count to "simplicity",
and look to methods with greater simplicity for insight. Beware that 
this connection is vague and should be put in context. 

## The Experiments
The our open access
[journal-paper](https://ieeexplore.ieee.org/document/9769957) where we propose
the [CDLNet](/projects/dcdl) architecture, we demonstrate a competitive[^1]
denoising performance to interpretably constructed neural networks,
distinguished by faster processing time. We consider this a "fair comparison"
as CDLNet is trained on the same dataset and has a roughly similar learned
parameter count (~64k). 

Ok, but state-of-the-art black-box DNNs (ex. DnCNN ~ 550k, FFDNet ~ 480k) have hundreds of
thousands of parameters. How do the interpretable networks perform in comparison?
**Worse**. But it's obviously not a fair comparison. And they don't have to be 
fair comparisons if they're exploring the proposed method from a unique perspective[^2] 
-- in this case the black-box methods serve not as competition but as a compass[^3].
Nonetheless, some authors do cite these experiements as justification for the 
merit of their proposed method. Perhaps they're implicitly saying, 

> It's amazing we got this close, with this simple of a model!

How close is close? To answer this, I shall fill in a missing piece of the
puzzle: **the performance of low learned parameter count black-box models**.
Specifally the most popular black-box denosing network, DnCNN.

- Table of performances
- appendix: table of DnCNN models


[^1]: better than some (but not all), in some (but not all) cases.
[^2]: novel methods **are** worth publishing even if they're not strictly "SOA". They may even lead to SOA methods if built upon further by other authors.
[^3]: not a compass to follow, simply to orient ourselves. A benchmark.

