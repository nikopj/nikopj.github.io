+++
title = "Staying organized while doing research (arxivmv)."
date = Date(2020, 10, 25)
hascode = false
rss = "arxivmv"
tags = ["productivity"]
descr = "I often find my downloads folder filling up with tons of research papers with nondescript (ID) names, such as \"1909.05742.pdf\". Keeping these PDFs open allows me to keep track of them, but once I close those windows they seem as good as lost. To remedy this, I've written a short Python script employing a [wrapper for the arXiv.org API](https://github.com/lukasschwab/arxiv.py)."
+++

# {{title}}

{{ descr }}
It looks at each PDF in my downloads folder that roughly looks like a paper
with an arXiv ID number as its name. It then searches the database, and if the
number is valid it renames the file to something more descriptive.
For example, the above mentioned file is turned into, 
["Elad\_RethinkingTheCsc\_1909.05742.pdf"](https://arxiv.org/abs/1909.05742).  

It's hard to over-emphasize the benefit of adding a little organization to your life. 
I hope the script below can be easily adapted to your setup, or inspire you to organize 
your own way.

\gist{nikopj/58316fa2380d2dbdcd856306962c187c}

### Future Work and Remarks:
- Perhaps there's an analogous way to interface with other organization's 
  databases, such as IEEE and SIAM?
- The arXiv API used seems to have "404 Errors" output upon invalid IDs requested.
  One could suppress these by wrapping ``arxivmv.py`` in another script that pipes 
  standard error to ``/dev/null``.
- One could have ``arxivmv.py`` running in the background for the automatic 
  organization of downloaded files.

