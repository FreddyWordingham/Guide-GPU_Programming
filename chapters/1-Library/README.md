# Library

## Dependencies

We're going to use the following libraries:

```shell
poetry add numpy
poetry add pillow
poetry add pyopencl
```

## Sample

Create a new file called [`sample.py`](./mandybrot_gpu/sample.py) in the `mandybrot_gpu` directory:

```shell
touch mandybrot_gpu/sample.py
```

Link this file to the [`__init__.py`](./mandybrot_gpu/__init__.py) file:

```python
from .sample import *
```

## Area

Add the following to [`sample.py`](./mandybrot_gpu/sample.py):

```python
import numpy as np
import pyopencl as cl

...
```

## Return

[Return to the top-level README](./../../README.md)
