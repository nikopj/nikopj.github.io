@def title = "Home"
@def date = Date(2023, 06, 07)

## About me
@@row
@@container
~~~
<img 
    class="left" 
    id=profpic
    src="assets/profilepic3.jpg"
    onmouseover="this.src='assets/profilepicQ.jpg';"
    onmouseout="this.src='assets/profilepic3.jpg';"
>
~~~

Hello. My name is Nikola Janjušević. I am a fourth year **PhD candidate in
Electrical Engineering** at *New York University* under the advisory of
Professor Yao Wang, [NYU VideoLab](https://wp.nyu.edu/videolab/). I
received my Bachelors in Electrical Engineering from *The Cooper Union for Advancement of
Science and Art* in 2019.

My current interests are in *interpretable deep-learning* models for solving
*inverse-problems* and low-level *computer-vision*/*image-processing* tasks. My
background is in *signal-processing* and *non-smooth, convex optimization*.
Outside of academia, I go biking and skateboarding with my friends.
@@
@@

## Updates
* October 2023: Presented poster at NYU CAI$^2$R [From Innovation to Implementation in Imaging (i2i) Workshop](https://cai2r.net/training/i2i-workshop/): ["SNAC-DL: Self-Supervised Network for Adaptive Convolutional Dictionary Learning of MRI Denoising"](/assets/research/i2i_poster_snacdl.pdf)
* October 2023: [*"Compressed sensing on displacement signals measured with optical coherence tomography"*](https://opg.optica.org/boe/fulltext.cfm?uri=boe-14-11-5539&id=540503) published in Biomedical Optics Express!
* August 2023: [*"Self-Supervised Low-Field MRI Denoising via Spatial Noise Adaptive CDLNet"*](assets/research/i2iabs_2023.pdf) abstract accepted to NYU CAI2R [i2i Workshop](https://cai2r.net/training/i2i-workshop/).
* August 2023: [SSIMLoss.jl](https://github.com/nikopj/SSIMLoss.jl),
  differentiable SSIM loss functions for neural network training, package
  published.
* June 2023: Joined NYU Langone Department of Radiology as a Non-Traditional
  Volunteer Intern, working on unsupervised learning for MRI denoising and
  CS-MRI reconstruction.
* June 2023: [*"Fast and Interpretable Nonlocal Neural Networks for Image Denoising via Group-Sparse Convolutional Dictionary Learning"*](https://arxiv.org/abs/2306.01950) submitted to IEEE Transactions
  on Image Processing. Preprint available on arxiv.

## Recent blog posts
{{recentposts blog}}
