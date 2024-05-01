# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/CLI/ps.ipynb.

# %% auto 0
__all__ = ['amp_disp']

# %% ../../nbs/CLI/ps.ipynb 4
import logging
import zarr
import numpy as np

import dask
from dask import array as da
from dask import delayed
from dask.distributed import Client, LocalCluster, progress
from ..utils_ import is_cuda_available, get_array_module
if is_cuda_available():
    import cupy as cp
    from dask_cuda import LocalCUDACluster
import moraine as mr
from .logging import mc_logger

# %% ../../nbs/CLI/ps.ipynb 5
@mc_logger
def amp_disp(rslc:str, # rslc stack
             adi:str, #output, amplitude dispersion index
             chunks:tuple[int,int]=None, # output data chunk size, same as rslc by default
            ):
    '''calculation the amplitude dispersion index from SLC stack.'''
    rslc_path = rslc
    adi_path = adi
    logger = logging.getLogger(__name__)
    rslc_zarr = zarr.open(rslc_path,mode='r')
    logger.zarr_info(rslc_path,rslc_zarr)
    if chunks is None: chunks = rslc_zarr.chunks[:2]

    logger.info('starting dask CUDA local cluster.')
    with LocalCUDACluster() as cluster, Client(cluster) as client:
        logger.info('dask local CUDA cluster started.')

        cpu_rslc = da.from_array(rslc_zarr, chunks=(*chunks,*rslc_zarr.shape[2:]))
        logger.darr_info('rslc', cpu_rslc)
    
        logger.info(f'calculate amplitude dispersion index.')
        rslc = cpu_rslc.map_blocks(cp.asarray)
        rslc_delayed = rslc.to_delayed()
        adi_delayed = np.empty_like(rslc_delayed,dtype=object)
        with np.nditer(rslc_delayed,flags=['multi_index','refs_ok'], op_flags=['readwrite']) as it:
            for block in it:
                idx = it.multi_index
                adi_delayed[idx] = delayed(mr.amp_disp,pure=True,nout=1)(rslc_delayed[idx])
                adi_delayed[idx] =da.from_delayed(adi_delayed[idx],shape=rslc.blocks[idx].shape[0:2],meta=cp.array((),dtype=cp.float32))
        adi = da.block(adi_delayed[...,0].tolist())
        
        # cpu_adi = adi.map_blocks(cp.asnumpy)
        logger.info(f'got amplitude dispersion index.')
        logger.darr_info('adi', adi)

        logger.info('saving adi.')
        cpu_adi = adi.map_blocks(cp.asnumpy)
        _adi = da.to_zarr(cpu_adi,adi_path,compute=False,overwrite=True)
        # adi_zarr = kvikio.zarr.open_cupy_array(adi_path,'w',shape=adi.shape, chunks=adi.chunksize, dtype=adi.dtype,compressor=kvikio.zarr.CompatCompressor.lz4())
        # _adi = da.store(adi,adi_zarr,compute=False,lock=False)

        logger.info('computing graph setted. doing all the computing.')
        futures = client.persist(_adi)
        progress(futures,notebook=False)
        da.compute(futures)
        logger.info('computing finished.')
    logger.info('dask cluster closed.')
