# UA colors for matplotlib

[![Pypi](https://img.shields.io/pypi/v/uastyle.svg)](https://pypi.org/project/uastyle/)
![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

`uastyle` - is a light Python package that provides blue-yellow styling for matplotlib.

## Install

Install `uastyle` using pip:

`pip install uastyle`

## How to use

### Explicit syntax

To use `uastyle`, import it and then call make_default_colors():

```
import uastyle
uastyle.make_default_colors()

colors = uastyle.colors
figsize = uastyle.M_width
```

### Simplified syntax

You can also import `apply_colors`, `colors`, and `M_width` directly:

```
from uastyle import apply_colors, colors, M_width
```

Importing `apply_colors` will apply changes to the default matplotlib colors.

If you want to avoid the "PylintW0611: unused-import" error, you can import from `apply_colors` directly:

```
from uastyle.apply_colors import colors, M_width
```
