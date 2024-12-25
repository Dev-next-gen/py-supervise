# app/utils.py

import psutil
import cupy as cp

def monitor_resources():
    gpu_free, gpu_total = 0, 0
    try:
        gpu_free, gpu_total = cp.cuda.runtime.memGetInfo()
    except Exception:
        pass
    return {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "gpu_memory_free": gpu_free,
        "gpu_memory_total": gpu_total,
    }
