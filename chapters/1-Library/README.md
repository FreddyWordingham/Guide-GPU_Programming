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
def area(real, imag, width, height, scale, max_iters):
    """
    Sample a region of the Mandelbrot set.
    """

    # Setup OpenCL
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx)

    # Compile kernel
    kernel = cl.Program(
        ctx,
        """
        __kernel void mandelbrot(__global float* buffer, float start_real, float start_imag, uint width, float delta_real, float delta_imag, uint max_iters) {
            int i = get_global_id(0);
            int j = get_global_id(1);

            int n = (i * width) + j;

            float x0 = start_real + (j * delta_real);
            float y0 = start_imag + (i * delta_imag);

            float x = 0.0;
            float y = 0.0;
            float x2 = 0.0;
            float y2 = 0.0;
            uint iteration = 0;

            while (((x2 + y2) <= 4.0) && (iteration < max_iters)) {{
                y = (x + x) * y + y0;
                x = x2 - y2 + x0;
                x2 = x * x;
                y2 = y * y;
                iteration = iteration + 1;
            }}

            buffer[n] = (float)(iteration);
        }
        """,
    ).build()

    # Copy data to GPU
    cpu_buffer = np.zeros((height, width)).astype(np.float32)
    gpu_buffer = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, cpu_buffer.nbytes)

    # Run kernel
    aspect_ratio = width / height
    delta_real = scale / max((width - 1), 1)
    delta_imag = scale / (max((height - 1), 1) * aspect_ratio)
    start_real = real - (0.5 * scale)
    start_imag = imag - (0.5 * scale / aspect_ratio)

    kernel.mandelbrot(
        queue,
        cpu_buffer.shape,
        None,
        gpu_buffer,
        np.float32(start_real),
        np.float32(start_imag),
        np.uint32(width),
        np.float32(delta_real),
        np.float32(delta_imag),
        np.uint32(max_iters),
    )

    # Copy data back to CPU
    cl.enqueue_copy(queue, cpu_buffer, gpu_buffer)

    return cpu_buffer
```

## Script

Create a `scripts/` directory, and within it create a `run.py` file:

```shell
mkdir scripts
touch scripts/run.py
```

Add the following to [`run.py`](./scripts/run.py):

```python
import argparse
import os

import mandybrot_gpu as mandy

OUTPUT_DIR = "output"

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("real", type=float)
parser.add_argument("imag", type=float)
parser.add_argument("width", type=int)
parser.add_argument("height", type=int)
parser.add_argument("scale", type=float)
parser.add_argument("max_iters", type=int)
args = parser.parse_args()

# Create output directory
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Sample the region
data = mandy.sample.area_gpu(
    args.real, args.imag, args.width, args.height, args.scale, args.max_iters
)


def display(data):
    """
    Display the Mandelbrot set.
    """
    shape = data.shape
    buffer = ""
    for im in reversed(range(shape[0])):
        for re in range(shape[1]):
            buffer += f"{data[im, re]:4.0f}   "
        buffer += "\n"
    print(buffer)


display(data)
```

## Test it

Run the script:

```shell
poetry run python scripts/run.py -0.5 0.0 24 32 2.0 100
```

You should see a plot of the Mandelbrot set in the terminal:

```text
   1      1      2      2      2      2      2      2      2      2      2
   1      2      2      2      2      2      2      2      2      2      2
   2      2      3      3      3      3      4      4      3      2      2
   3      3      3      3      4      4      5     15      4      4      3
   3      3      3      4      4      6      8    100      7      5      3
   3      3      4      5      6    100    100    100    100     82      4
   4      7      7      7     13    100    100    100    100    100      5
   5      9    100    100    100    100    100    100    100    100      5
 100    100    100    100    100    100    100    100    100     12      5
   5      9    100    100    100    100    100    100    100    100      5
   4      7      7      7     13    100    100    100    100    100      5
   3      3      4      5      6    100    100    100    100     82      4
   3      3      3      4      4      6      8    100      7      5      3
   3      3      3      3      4      4      5     15      4      4      3
   2      2      3      3      3      3      4      4      3      2      2
   1      2      2      2      2      2      2      2      2      2      2
   1      1      2      2      2      2      2      2      2      2      2
```

## Return

[Return to the top-level README](./../../README.md)
