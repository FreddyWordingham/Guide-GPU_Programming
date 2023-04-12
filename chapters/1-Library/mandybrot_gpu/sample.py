import numpy as np
import pyopencl as cl


def area_gpu(real, imag, width, height, scale, max_iters):
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

            //float x0 = start_real + ((float)i * delta_real);
            //float y0 = start_imag + ((float)j * delta_imag);

            //float x = 0.0;
            //float y = 0.0;
            //float x2 = 0.0;
            //float y2 = 0.0;
            //uint iteration = 0;

            //while (((x2 + y2) <= 4.0) && (iteration < max_iters)) {{
            //    y = (x + x) * y + y0;
            //    x = x2 - y2 + x0;
            //    x2 = x * x;
            //    y2 = y * y;
            //    iteration = iteration + 1;
            //}}

            //buffer[i + (j * width)] = (float)(iteration);
            buffer[i + (j * width)] = i;
        }
        """,
    ).build()

    # Copy data to GPU
    cpu_buffer = np.zeros((width, height)).astype(np.float32)
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


# def area_gpu(real, imag, width, height, scale, max_iters):
#     re = np.linspace(
#         real - 0.5 * scale * width, real + 0.5 * scale * width, width
#     ).astype(np.float32)
#     im = np.linspace(
#         imag - 0.5 * scale * height, imag + 0.5 * scale * height, height
#     ).astype(np.float32)

#     ctx = cl.create_some_context()
#     queue = cl.CommandQueue(ctx)

#     mf = cl.mem_flags
#     a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
#     b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)

#     prg = cl.Program(
#         ctx,
#         """
#     __kernel void sum(
#         __global const float *a_g, __global const float *b_g, __global float *res_g)
#     {
#     int gid = get_global_id(0);
#     res_g[gid] = a_g[gid] + b_g[gid];
#     }
#     """,
#     ).build()

#     res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
#     knl = prg.sum
#     knl(queue, a_np.shape, None, a_g, b_g, res_g)

#     res_np = np.empty_like(a_np)
#     cl.enqueue_copy(queue, res_np, res_g)

#     print(res_np - (a_np + b_np))
#     print(np.linalg.norm(res_np - (a_np + b_np)))

#     assert np.allclose(res_np, a_np + b_np)
