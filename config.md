<!--
Add here global page variables to use throughout your website.
-->
+++
author = "Nikola Janjušević"
mintoclevel = 2

# Add here files or directories that should be ignored by Franklin, otherwise
# these files might be copied and, if markdown, processed by Franklin which
# you might not want. Indicate directories by ending the name with a `/`.
# Base files such as LICENSE.md and README.md are ignored by default.
ignore = ["node_modules/"]

# RSS (the website_{title, descr, url} must be defined to get RSS)
generate_rss = true
website_title = author
website_descr = "Nikola's Вебсајт"
website_url   = "https://nikopj.github.io"

# robots
generate_robots = true
+++

<!--
Add here global latex commands to use throughout your pages.
Use exclamation before Latex argument to avoid insertion of \b, ex. "!#1".
-->
\newcommand{\R}{\mathbb R}
\newcommand{\norm}[1]{\lVert !#1 \rVert}
\newcommand{\abs}[1]{\lvert !#1 \rvert}
\newcommand{\minimize}[1]{\underset{!#1}{\mathrm{minimize}\,}\,}
\newcommand{\argmin}[1]{\underset{!#1}{\mathrm{argmin}\,}\,}
\newcommand{\st}{\mathrm{s.t.}\,}
\newcommand{\subto}{\text{subject to}\,}
\newcommand{\prox}{\mathbf{prox}}
\newcommand{\herm}{\mathrm{H}}

\newcommand{\styletext}[2]{~~~<span style="!#1">#2</span>~~~}
\newcommand{\textcolor}[2]{~~~<span style="color:!#1">!#2</span>~~~}

<!-- caption (optional), src, style (optional) -->
\newcommand{\figenv}[3]{
~~~
<figure style="text-align:center;">
<img src="!#2" style="padding:0;#3" alt="#1"/>
<figcaption>#1</figcaption>
</figure>
~~~
}

<!-- display Github gist from ID number -->
\newcommand{\gist}[1]{
~~~
<script type="application/javascript" src="https://gist.github.com/!#1.js"></script>
~~~
}

<!-- banners -->
\newcommand{\note}[2]{
@@box-green
	@@title
	**Note**: !#1
	@@
	@@content
	!#2
	@@
@@
}

\newcommand{\warning}[2]{
@@box-red
	@@title
	**⚠Warning⚠**: !#1
	@@
	@@content
	!#2
	@@
@@
}
