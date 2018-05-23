#!/usr/bin/python3
import pyopencl as cl
from pyopencl import array
import numpy as np
import depth

def run(symbol1, symbol2, debug):
    depthData = depth.getDepth(symbol1, symbol2, debug)
    depthData = depthData.flatten()
    print(depthData)
    dest = np.empty_like(depthData.shape)
    computed_data = np.empty((3,1))
    platforms = cl.get_platforms()
    gpus = platforms[0].get_devices(cl.device_type.ALL)
    device = gpus[0]
    context = cl.Context([device])
    program = cl.Program(context, """
    __kernel void percentage_price(__global const float *input, __global float *computed_data, __global float *output)
    {
        __local float tmp[80];
        __local float tmp_computed_data[3];
        int gid = get_global_id(0);
        int lid = get_local_id(0);
        barrier(CLK_LOCAL_MEM_FENCE);
        tmp[lid] = input[gid];
        tmp_computed_data[0] = ((tmp[0] + tmp[40]) / 2.0);      // Price computed using highest bid and lowest ask
        tmp[lid] = ((tmp[lid] / tmp_computed_data[0]) * 100.0); // store the bid or ask as a percentage of the computed price
        barrier(CLK_GLOBAL_MEM_FENCE);
        for(int i=0; i<80; i++) {
            output[i] = tmp[i];
        }
        for(int i=0; i<3; i++) {
            computed_data[i] = tmp_computed_data[i];
        }
        barrier(CLK_LOCAL_MEM_FENCE);
    }
    """).build()
    queue = cl.CommandQueue(context)
    mem_flags = cl.mem_flags
    depth_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf = depthData)
    computed_data_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, computed_data.nbytes)
    dest_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, dest.nbytes)
    program.percentage_price(queue, (80,), None, depth_buf, computed_data_buf, dest_buf)
    cl.enqueue_copy(queue, dest, dest_buf)
    cl.enqueue_copy(queue, computed_data, computed_data_buf)
    print(computed_data)
    print(dest)
    print(depthData[0])
    print(depthData[40])
