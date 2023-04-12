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
    for im in reversed(range(shape[1])):
        for re in range(shape[0]):
            buffer += f"{data[re, im]:.0f}   "
        buffer += "\n"
    print(buffer)


display(data)
