import collections.abc as abc

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


def prepare(
    xtitle=None,
    ytitle=None,
    w=None,  # width, float for inches, str for powerpoint page width, or str for paper width
    h=None,  # height, float for inches, this is optional
    r=0.7,  # ratio of height to width
    font="arial",
    fontsize=20,
):
    # reset current rcParams to default
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)

    # define width in inches
    if isinstance(w, float) or isinstance(w, int):
        pass
    elif w is None:  # fallback size
        w = 13 * 0.3  # almost one third of the 16:9 powerpoint presentation
    elif w == "1col":  # below are the sizes for journal figures
        w = 3.543
    elif w == "1.5col":
        w = 5.512
    elif w == "2col":
        w = 7.480
    elif w == "2col_1/4":
        w = 1.850
    elif w.startswith("pp1/"):  # division for powerpoint
        w = 13 / float(w.split("/")[1])
    elif w.startswith("pp"):  # multiplier for powerpoint
        w = 13 * float(w.split("pp")[1])
    elif h is not None:
        w = h / r

    # define height in inches
    if h == None:  # if height is not specified
        h = w * r

    # general graph styles
    plt.rcParams["axes.autolimit_mode"] = "round_numbers"
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["xtick.major.pad"] = 8
    plt.rcParams["ytick.major.pad"] = 8

    # font
    # print(plt.rcParams["font.sans-serif"]) # list available fonts for this PC
    if font == "arial":
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = ["Arial"]
    elif font == "times":
        rc = {"font.family": "serif", "mathtext.fontset": "stix"}
        plt.rcParams.update(rc)
        plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
    plt.rcParams["font.size"] = fontsize

    # legend
    plt.rcParams["legend.framealpha"] = 0
    plt.rcParams["legend.fancybox"] = False
    plt.rcParams["legend.fontsize"] = fontsize
    plt.rcParams["legend.borderpad"] = 0
    plt.rcParams["legend.labelspacing"] = 0.3
    plt.rcParams["legend.handlelength"] = 1.5
    plt.rcParams["legend.handletextpad"] = 0.4

    # initialize figure and axis
    fig, ax = plt.subplots(figsize=(w, h))

    # axis title
    if xtitle:
        ax.set_xlabel(xtitle)
    if ytitle:
        ax.set_ylabel(ytitle)

    # tick label format
    ax.ticklabel_format(
        axis="y",
        style="sci",
        scilimits=(-2, 3),
        useMathText=True,
    )

    return fig, ax


def finalize(
    fig,
    ax,
    fn_figout,
    lims=[None, None, None, None],  # [xmin, xmax, ymin, ymax]
    dpi=300,
    pil_kwargs={},
    tight=True,
    pad=0.2,  # padding for tight_layout
    xspace=None,  # float for spacing, tuple for spacing and offset
    yspace=None,  # float for spacing, tuple for spacing and offset
):
    # override limits
    ax.set_xlim(lims[0], lims[1])
    ax.set_ylim(lims[2], lims[3])

    # set major ticks
    if not xspace is None:  # for x-axis
        if isinstance(xspace, abc.Sequence) == True:  # spacing with specified offset
            ax.xaxis.set_major_locator(plticker.MultipleLocator(xspace[0], xspace[1]))
        else:  # spacing without offset
            ax.xaxis.set_major_locator(plticker.MultipleLocator(xspace))
    if not yspace is None:  # for y-axis
        if isinstance(yspace, abc.Sequence) == True:  # spacing with specified offset
            ax.yaxis.set_major_locator(
                plticker.MultipleLocator(base=yspace[0], offset=yspace[1])
            )
        else:  # spacing without offset
            ax.yaxis.set_major_locator(plticker.MultipleLocator(yspace))

    # save fig
    if tight:
        fig.tight_layout(pad=pad)
    fig.savefig(fn_figout, dpi=dpi, pil_kwargs=pil_kwargs)

    return fig, ax
