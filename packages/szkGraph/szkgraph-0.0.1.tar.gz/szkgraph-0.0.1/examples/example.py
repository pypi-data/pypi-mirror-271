import sys

# when importing the module from different directory, we need to add the directory to the path
# uncomment the below two lines and change the path to the directory of szkGraph
# dir_szkGraph = r"C:\USERNAME\Documents\Git\szk-graph"
# sys.path.append(dir_szkGraph)
import szkGraph


# example 1: plot a simple graph
def example1():
    # preparation
    fig, ax = szkGraph.prepare(
        xtitle="This is x-axis",
        ytitle="This is y-axis",
        w=6,
        h=5,
        font="arial",
    )

    # plotting scatter
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]
    ax.scatter(x, y)

    # output the graph
    fn_out = "example1.png"
    szkGraph.finalize(fig, ax, fn_out)


# example 2: modify figure size
def example2():
    # figure size can be set with width and height, or width and ratio
    # width can be float value in inches, or portion of paper width, or portion of powerpoint page width
    # number of pixels are determined by inches*dpi. default dpi is 300, which is common value for printing.

    # preparation
    fig, ax = szkGraph.prepare(
        xtitle="This is x-axis",
        ytitle="This is y-axis",
        w="pp0.3",  # 0.3 of the powerpoint page width
        r=0.7,  # ratio of height to width
        font="arial",
    )

    # plotting scatter
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]
    ax.scatter(x, y)

    # output the graph
    fn_out = "example2.png"
    szkGraph.finalize(fig, ax, fn_out)


# example 3: modify axis range and tick interval
def example3():
    # preparation
    fig, ax = szkGraph.prepare(
        xtitle="This is x-axis",
        ytitle="This is y-axis",
        w=6,
        h=5,
        font="arial",
    )

    # plotting scatter
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]
    ax.scatter(x, y)

    # axis range can bw set with lims, where [xmin, xmax, ymin, ymax]
    # tick interval can be set with xspace and yspace, where float for spacing and tuple for (spacing, offset)

    # output the graph
    fn_out = "example3.png"
    szkGraph.finalize(
        fig, ax, fn_out, lims=[-0.5, 5.5, -1, 26], xspace=(1, 0), yspace=(5, 0)
    )


### EXECUTION ###
example1()
example2()
example3()
