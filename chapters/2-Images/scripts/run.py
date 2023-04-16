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
parser.add_argument("cmap", nargs="+", type=str)
args = parser.parse_args()

# Create output directory
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Build the colour map
cmap = mandy.colour.build_colour_map(args.cmap, 256)

# Sample the region
data = mandy.sample.area(
    args.real, args.imag, args.width, args.height, args.scale, args.max_iters
)

# Convert to an image
img = mandy.colour.image(data, args.max_iters, cmap)
mandy.colour.encode(img).save(os.path.join(OUTPUT_DIR, "mandybrot.png"))
