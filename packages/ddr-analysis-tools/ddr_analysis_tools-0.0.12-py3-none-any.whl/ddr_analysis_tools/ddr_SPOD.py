

import os
import sys
import numpy as np
import pandas as pd
import yaml

from typing import Optional

from .pyspod_local.spod.standard import Standard as spod_standard
from .pyspod_local.spod import utils as utils_spod
from .pyspod_local.utils import postproc as post



class spectral_POD(spod_standard):
    '''
    The class helps in implimenting pyspod code. This code is written for purpose of DAVIS data analysis.
    
    You may have to modify the code to use it for some other application.
    '''

    def __init__(
        self,
        params: dict|None = None,
        data: Optional[np.ndarray] = None,
        load_local: bool = False,
        local_data_foldpath: Optional[str] = None
        ) -> None:
        '''
        params: dict, optional
            These are parameters required in pyspod code. The details of these could be found on
            https://github.com/MathEXLab/PySPOD/blob/main/tutorials/tutorial1/tutorial1.ipynb

            This is the tutorial for implementing pyspod. In it you can find how to determine the params.

        data : np.ndarray, optional
            If spod has to be performed then provide the data.
            Data should be arranged such that the time dimention remains in the first axis of array.
            The matrix should be 3500 X 128 X 128, where ther are 3500 snapshots of 128 X 128 values each.
            The values can be anything, but SPOD mode will be of the shape of single snapshot data shape.

        load_local: bool, False
            If you just want to load the SPOD calculated previously then make this True

        local_data_foldpath
            If load_local is True, then code will search for modes and all in this directory.
            This directory is originally made by pyspod code.
        '''

        # loading parameter from local data if provided
        if load_local:
            with open(os.path.join(local_data_foldpath,'params_modes.yaml'),'r') as file1:
                params = yaml.load(file1, Loader=yaml.FullLoader)
        
        super().__init__(params=params)
        if load_local:
            self._savedir_sim = local_data_foldpath
            self._modes_dir = os.path.join(local_data_foldpath,'modes')
            
            # reading from zipped file
            f1 = np.load(os.path.join(local_data_foldpath,'eigs_freq.npz'))
            self._eigs = f1['eigs']
            self._freq = f1['freq']

        else:
            self = self.fit(data_list=data)


    def get_mode(self,freq_idx:int,n_mode:int=0)-> np.ndarray:
        '''
        freq_idx
            index of required frequency
        
        n_mode
            which mode is required

        Returns:
            The required mode at indexed frequency.
            The returned mode is complex.
        '''
        m1 = np.array(post.get_modes_at_freq(results_path=self.savedir_sim,freq_idx=freq_idx))
        m1 = np.squeeze(m1)
        return m1[...,n_mode]

    def get_block(self,freq_idx:int,n_mode:int=0)-> np.ndarray:
        '''
        freq_idx
            index of required frequency
        
        n_mode
            which mode is required

        Returns:
            The required mode at indexed frequency.
            The returned mode is complex.
        '''
        tmp_name = f'fft_block{n_mode:08d}_freq{freq_idx:08d}.npy'
        filepath = os.path.join(self.savedir_sim,'blocks', tmp_name)
        return np.load(filepath)






