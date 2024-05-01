# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/API/utils_.ipynb.

# %% auto 0
__all__ = ['ngjit', 'ngpjit', 'is_cuda_available', 'get_array_module']

# %% ../nbs/API/utils_.ipynb 2
# Adapted from spatialpandas at https://github.com/holoviz/spatialpandas under BSD-2-Clause license.

# %% ../nbs/API/utils_.ipynb 4
import numpy as np
from numba import jit
import os

# %% ../nbs/API/utils_.ipynb 5
ngjit = jit(nopython=True, nogil=True)
ngpjit = jit(nopython=True, nogil=True, parallel=True)

# %% ../nbs/API/utils_.ipynb 6
def is_cuda_available():
    if 'CUDA_VISIBLE_DEVICES' in os.environ:
        return True
    else:
        return False

# %% ../nbs/API/utils_.ipynb 7
def get_array_module(array):
    if is_cuda_available():
        try:
            import cupy
            return cupy.get_array_module(array)
        except:
            return np
    else:
        return np
