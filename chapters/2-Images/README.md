# Library

## Dependencies

We're going to use the following libraries:

```shell
poetry add numpy
poetry add pillow
poetry add pyopencl
```

## Colour

Create a new file called [`colour.py`](./mandybrot_gpu/colour.py) in the `mandybrot_gpu` directory:

```shell
touch mandybrot_gpu/colour.py
```

Link this file to the [`__init__.py`](./mandybrot_gpu/__init__.py) file:

```python
from .colour import *
```

## Sample to RGB

We're going to need to convert the sampled values to RGB values.
Add the following to [`colour.py`](./mandybrot_gpu/colour.py):

```python
def build_colour_map(rgb_list: list, n: int=256):
    """
    Build a list of linearly interpolates between a list of RGB tuples.
    """

    if len(rgb_list) == 1:
        return rgb_list * n

    splits = [int(n / (len(rgb_list) - 1))] * (len(rgb_list) - 1)
    for i in range(n - sum(splits)):
        splits[i] += 1
    print(f"SPLITS  : {splits}")
    print(f"TOTAL   : {sum(splits)}")

    cmap = []
    for i, split in enumerate(splits):
        r1, g1, b1 = rgb_list[i]
        r2, g2, b2 = rgb_list[i+1]

        r_step = (r2 - r1) / max(1, split - 1)
        g_step = (g2 - g1) / max(1, split - 1)
        b_step = (b2 - b1) / max(1, split - 1)

        for n in range(split):
            r = int(r1 + (n * r_step))
            g = int(g1 + (n * g_step))
            b = int(b1 + (n * b_step))

            cmap.append((r, g, b))

    return cmap
```

## RGB to Image

Now we need to convert the RGB values to an image.

Add the following to [`colour.py`](./mandybrot_gpu/colour.py):

```python
from PIL import Image

def rgb_to_image(rgb, width, height):
    """
    Convert an RGB colour to an image.
    """

    image = Image.new("RGB", (width, height))
    image.putdata(rgb)
    return image
```

## Hex to RGB

It will be easier for the user to specify colours in hex format.
So, inside [`colour.py`](./mandybrot_gpu/colour.py) add the following:

```python
def hex_to_rgb(hex):
    """
    Convert a hex colour to an RGB colour.
    """
    hex = hex.lstrip("#")
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
```

which will convert a hex colour to an RGB colour.

## Script

Now edit the [`run.py`](./scripts/run.py) script to accept the colour arguments, and use the image function:

```python

```

## Test it

Run the script:

```shell
poetry run python scripts/run.py -0.5 0.0 24 32 2.0 100
```

## Return

[Return to the top-level README](./../../README.md)
