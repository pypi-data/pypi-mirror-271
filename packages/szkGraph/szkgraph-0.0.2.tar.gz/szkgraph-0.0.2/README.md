# szkGraph - simple style formatter for matplotlib
This is a useful Python codes to simply modify the style of matplotlib for your presentation and academic papers.
Any type of suggestions, feedbacks, and upgrades are welcome.

# How to install?
Install using pip.
`python -m pip install -U szkGraph`

# How to use?
Call `szkGraph.prepare()` to initialize the figure. Use the returned `fig, ax` for plotting.
After plotting and modifying your figure, export the figure with `szkGraph.finalize()`. 

## `szkGraph.prepare(xtitle=None, ytitle=None, w=None, h=None, r=0.7, font="arial", fontsize=20)`
### Paramters
* **xtitle**: _str, optional_
    Title of x-axis.
* **ytitle**: _str, optional_
    Title of y-axis.
* **w**: _float or str, optional_
    Float for specifying the width in inches, str for specifying the width relative to powerpoint slide or academic paper.
    Use `pp1/X` for one-X-th of powerpoint slide (16:9), `ppX` for X times of powerpoint slide (16:9), and `1col` etc. for figures in academic paper.
* **h**: _float, optional_
    Height in inches.
* **r**: _float, optional_
    Ratio of height to width.
* **font**: _str, optional_
    Fontname. It should be either `arial` or `times`.
* **fontsize**: _int, optional_
    Fontsize in pt.

### Returns
* **fig**: _matplotlib.figure_
* **ax**: _matplotlib.axes_


## `finalize(fig, ax, fn_figout, lims=[None, None, None, None], dpi=300, comp={}, tight=True, pad=0.2, xspace=None, yspace=None)`
### Paramters
* **fig**: _matplotlib.figure_
* **ax**: _matplotlib.axes_
* **fn_figout**: _str_
    Name of the output figure file. It could also be in absolute or relative path.
* **lims**: _list of floats, optional_
    Range of axis in one list as `[xmin, xmax, ymin, ymax]`.
* **dpi**: _int, optional_
    Value of dpi.
* **pil_kwargs**: _dict, optional_
    Dictionary that will be directly passed to `PIL.Image.Image.save`.
* **tight**: _bool, optional_
    Whether to use [`matplotlib.pyplot.tight_layout()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tight_layout.html).
* **pad**: _float, optional_
    Padding for [`matplotlib.pyplot.tight_layout()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.tight_layout.html).
* **xspace**: _float or tuple of floats_
    Float for specifying x-tick spacing, tuple of floats for specyfing (x-tick spacing, offset). See [`matplotlib.ticker.MultipleLocator()`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.MultipleLocator).
* **yspace**: _float or tuple of floats_
    Float for specifying y-tick spacing, tuple of floats for specyfing (y-tick spacing, offset). See [`matplotlib.ticker.MultipleLocator()`](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.MultipleLocator).

### Returns
* **fig**: _matplotlib.figure_
* **ax**: _matplotlib.axes_


# License
szkGraph is available under MIT license. See the LICENSE file for more info.
