import pyopencl as cl
from pyopencl import array
import numpy as np
import asyncio
import depth
import time


async def run(symbol1, symbol2, quantity, iterations, delay):
    #Define OpenCL kernel
    source = """
    // outputs bid and ask prices as a percentage of the computed price at
    // their given exchange as well as the amount available at that price
    __kernel void depthPercentage(__global const float4 *a_g, __global const float *b_g, __global float4 *res_g)
    {
        int gid = get_global_id(0);
        int groupid = get_group_id(0);
        float price = b_g[groupid];
        float4 vec = a_g[gid];
        float scalar = (1.0/price) * 100;
        vec.x *= scalar;
        vec.z *= scalar;
        res_g[gid] = vec;

    }
    """
    #OpenCL initialization using first GPU
    platforms = cl.get_platforms()
    gpus = platforms[0].get_devices(cl.device_type.ALL)
    device = gpus[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    #Compile OpenCL program
    prg = cl.Program(ctx, source).build()
    #Create input and output buffers
    forever = False
    if iterations == -1:
        forever = True
    while forever or iterations > 0:
        a_np, b_np, exchanges = await depth.getDepth(symbol1, symbol2, quantity)
        a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a_np)
        b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = b_np)
        res_np = np.empty_like(a_np)
        res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
       #Execute OpenCL program
        ker = prg.depthPercentage
        ker.set_arg(0, a_g)
        ker.set_arg(1, b_g)
        ker.set_arg(2, res_g)
        launch = cl.enqueue_nd_range_kernel(queue, ker, a_np.shape, (quantity,))
        launch.wait()
        #create array to store output
        ev = cl.enqueue_copy(queue, res_np, res_g)
        ev.wait()
        print(await splitPrint(res_np, quantity, exchanges))
        time.sleep(delay)
        iterations -= 1

async def splitPrint(arr, quantity, exchanges):
    print(exchanges)
    count = 0;
    depth = ""
    for i in range(0, arr.size):
        print(arr[i])
        if i % quantity == 0:
            depth += exchanges[count] + ": Highest Bid: " + str(arr[count*quantity][0]) + ", Lowest Ask: " + str(arr[count*quantity][2]) + "\r\n"
            count += 1
    print(depth)
