# Fico
Fico (from Latin _ficus_, "fig") assists in creating consistent Matplotlib figures with easy scaling and styling groups of figures.

## Overview

Figures are organized into several substructures that are combined to form a figure tree:

1. The highest level is the `FigureContainer` - a figure tree will have one of these at the root.
2. The `FigureContainer` consists of several `FigureCollection`s - these will always be direct descendants of a `FigureContainer`.
3. Each `FigureCollection` contains different subclasses of `Figure` - likewise, these are always direct descendants of a `FigureCollection`.

The top-level `FigureContainer` defines global styling and handles top-level building. All child `Figure`s inherit the styles from the parent container, unless specifically overwritten in the figure-definition. Each instance of `FigureCollection` corresponds to a single folder in the final build and thus their main purpose is to group a related collection of figures. Each instance of `Figure` corresponds to a single diagram, and thus a single file when built.

The default export format for figures is pdf.

## Running a build

You can run a build locally by running the following script in a terminal

```bash
fico build
```

this will rebuild all figures in publication quality. If instead you want a faster build, you can use draft mode. This will only build those figures initialized with `@collection.plot_figure(..., only_build_this=True)`. Keep in mind that if no figure has this flag set, draft mode is completely equivalent to the standard build mode, and all figures will be built.

```bash
fico build -d
```

### Specifying which container to build
By default, `fico build` builds the container defined in the module `index` exported as `container`. This can be overwritten such that no particular project-structure is enforced. Say for example, you have defined a root container in a variable called `root` in a package-structure like `package_name/module_name`. This container is then built by specifying the location of the container to the build command:

```bash
fico build --container package_name.module_name:root
```

_Note_: The path of invokation of Fico is added to `sys.path`, so the container path should be relative to this point.


## Defining figures

### The top-level `FigureContainer`

As shown above, a figure container is passed to the Fico build command, and acts as the root of the figure tree. As such, you'll always need to define at least one `FigureContainer` to build figures.

```python
from fico import FigureContainer

### Code that instantiates/imports FigureCollections ###

collection = FigureContainer([col1, col2, ...])
```

#### Overwriting the default figure builder
A figure builder traverses the entire figure tree, applies global styling to the figures, and outputs them in a directory-structure that directly maps to the structure of the figure tree. A default builder is defined in Fico that is used if it isn't explicitly overwritten when defining the `FigureContainer`. 

```python
# Using SciencePlots to style figures
from fico import FigureContainer, FigureBuilder
import scienceplots

### Code that instantiates/imports FigureCollections ###

collection = FigureContainer([col1, col2, ...], builder=FigureBuilder(style="ieee"))
```

### The grouping `FigureCollection`
A figure collection just needs a name.

```python
from fico import FigureCollection

collection = FigureCollection("my_collection")
```

### The figures themselves `Figure`

When you've defined an appropriate `FigureCollection`, you can start registering figure functions in the collection

```python
import matplotlib.pyplot as plt
import numpy as np


@collection.plot_figure()
def figure1():
    # Some example data to display
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x**2)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("A single plot")

    return fig
```

#### Scaling figures
By default, the width of a figure is equal to the width of an A4 page with 2.54 cm margins (453pt). The height is automatically calculated such that the ratio between the width and height is the golden ratio. The default settings, equivalent to omitting both the `height` and `width` settings are
```python
@collection.plot_figure(width=1.0, height=1.0)
def figure1(fig, ax):
```

There are a couple options when you want to scale a figure. Both `width` and `height` can be specified as a float, in which case the size is relative to the default size. Note that the `height` scaling is always applied _after_ the figure height has been calculated to conform to the golden ratio, i.e. when `height=1.0` the ratio between the width and the height is the golden ratio.

For example, setting the width of a figure to half of a standard page (omitting the height setting, such that it is automatically calculated)
```python
@collection.plot_figure(width=0.5)
def figure1(fig, ax):
```

Setting the width of a figure to half of a standard page, and cutting the height in half
```python
@collection.plot_figure(width=0.5, height=0.5)
def figure1(fig, ax):
```

If the relative sizing and the automatic calculation are prohibitive to what you're trying to achieve, both dimensions can be specified absolutely in a string. The supported units are `mm`, `cm`, `pt` and `in`:
```python
@collection.plot_figure(width="3cm", height="30mm")
def figure1(fig, ax):
```


