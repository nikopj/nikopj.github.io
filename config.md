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
\newcommand{\textsize}[2]{~~~<span style="font-size:!#1px">#2</span>~~~}
\newcommand{\textcolor}[2]{~~~<span style="color:!#1">!#2</span>~~~}
\newcommand{\texthighlight}[2]{~~~<span style="background-color:!#1">!#2</span>~~~}

\newcommand{\uline}[1]{~~~<u>!#1</u>~~~}

<!-- caption (optional), src, style (optional) -->
\newcommand{\figenv}[3]{
~~~
<figure style="text-align:center;">
<img src="!#2" style="padding:0;#3" alt="#1"/>
<figcaption>#1</figcaption>
</figure>
~~~
}

\newcommand{\hoverfig}[4]{
~~~
<figure style="text-align:center;">
<img 
    src="!#2" 
    style="padding:0;#4" 
    alt="#1"
    onmouseout="this.src='!#2';"
    onmouseover="this.src='!#3';"
>
<figcaption>#1</figcaption>
</figure>
~~~
}

\newcommand{\twofigenv}[5]{
~~~
<figure style="text-align:center;">
<img src="!#2" style="padding:0;!#3" alt="#1"/>
<img src="!#4" style="padding:0;!#5" alt="#1"/>
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

\newcommand{\example}[2]{
@@box-blue
	@@title
	**Example**: !#1
	@@
	@@content
	!#2
	@@
@@
}

\newcommand{\reference}[2]{
@@box-green
	@@title
	**Reference**: !#1
	@@
	@@content
	!#2
	@@
@@
}

\newcommand{\dropblue}[3]{
@@box-blue
~~~
<label class="showMore" for="!#1">
<div class="title">
!#2
<span style="font-size:10px">(click to show)</span> 
</div>
</label>
<input id="!#1" type="checkbox">
<div>
~~~
    @@content
    !#3
    @@
~~~
</div>
~~~
@@
}


\newcommand{\toggletext}[4]{
@@box-blue
~~~
    <label class="toggle-text" for="!#1">
    <div class="title">
    !#2
    <span style="font-size:10px">(click to toggle)</span> 
    </div>
    </label>
    <input type="checkbox" id="!#1" style="display: none">
    <div>
    <div class="content">
    <p class="toggle-text-A">
~~~
!#3
~~~
    </p>
    <p class="toggle-text-B">
~~~
!#4
~~~
    </p>
    </div>
    </div>
~~~
@@
}
