#!/usr/bin/python3
import pyopencl as cl
from pyopencl import array
import numpy as np
import depth

def run(symbol1, symbol2, quantity):
    a_np = depth.getDepth(symbol1, symbol2, quantity)
    #Define OpenCL kernel
    source = """
    __kernel void getLocalID(__global const float4 *a_g, __global float4 *res_g)
    {
        //TODO: compute the price, store in local memory and perform divison by price, then mult. by 100
        wg_size = get_local_size(0);
        int gid = get_global_id(0);
        int lid = get_local_id(0);
        res_g[gid] = a_g[gid];
    }
    """
    #OpenCL initialization using first GPU
    platforms = cl.get_platforms()
    gpus = platforms[0].get_devices(cl.device_type.ALL)
    device = gpus[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    #Create input and output buffers
    a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a_np)
    res_np = np.empty_like(a_np)
    res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
    #Compile OpenCL program
    prg = cl.Program(ctx, source).build()
    #Execute OpenCL program
    ker = prg.getLocalID
    ker.set_arg(0, a_g)
    ker.set_arg(1, res_g)
    launch = cl.enqueue_nd_range_kernel(queue, ker, a_np.shape, (quantity,))
    launch.wait()
    #create array to store output
    ev = cl.enqueue_copy(queue, res_np, res_g)
    ev.wait()
    splitPrint(res_np, quantity)

def splitPrint(arr, splitNum):
    for i in range(0, arr.size):
        print(arr[i])
        if (i+1) % splitNum == 0:
            print()
