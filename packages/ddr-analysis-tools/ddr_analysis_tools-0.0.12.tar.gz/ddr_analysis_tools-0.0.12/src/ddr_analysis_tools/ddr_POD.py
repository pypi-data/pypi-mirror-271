"""
@author: Rathod Darshan D
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy
import os as os


def prep_UVs_for_POD(U, V):
    """
    prepares the matrix from U and V which can be supplied to POD code. The data is arranged in a way required in POD algorithm.
    """
    sh1 = U.shape
    U = U.reshape(sh1[0] * sh1[1], sh1[2]).T
    sh1 = V.shape
    V = V.reshape(sh1[0] * sh1[1], sh1[2]).T
    UVs = np.concatenate((U, V), axis=1)
    return UVs

def prep_UVWs_for_POD(U, V, W):
    """
    prepares the matrix from U, V and W which can be supplied to POD code. The data is arranged in a way required in POD algorithm.
    """
    sh1 = U.shape
    U = U.reshape(sh1[0] * sh1[1], sh1[2]).T
    sh1 = V.shape
    V = V.reshape(sh1[0] * sh1[1], sh1[2]).T
    sh1 = W.shape
    W = W.reshape(sh1[0] * sh1[1], sh1[2]).T
    UVWs = np.concatenate((U, V, W), axis=1)
    return UVWs

# give the row data without subtracting the mean
class POD:
    def __init__(self, data, *args, **kwargs):
        """
        do not subtract the mean in the data. Because this process is done by
        the code here.
        data should be arranged in 2D matrix. Samples are to be arranged in rows.
        Hence if single sample contains 10 data and there are shuch 20 samples then
        the data matrix should be of 20 X 10 shape.

        arrange the data in (N X M) matrix in such a way that element $A_{ij}$
        is the measurement of the $j^{th}$ velocity vector in $i^{th}$ frame.

        """

        self.data_mean = data.mean(axis=0)

        data1 = data - self.data_mean
        U, eps, V_T = np.linalg.svd(data1, full_matrices=False)

        self.U = U
        self.eps = eps
        self.V_T = V_T

    def mode(self, n=0):
        return self.V_T[n, :]

    def time_coeff(self, n=0):
        return self.U[:, n]

    def singular_value(self, n=0):
        return self.eps[n]

    def reconstruct_data(self, n_modes=10):
        return (
            self.U[:, :n_modes] @ np.diag(self.eps[:n_modes]) @ self.V_T[:n_modes, :]
        ) + self.data_mean


class snapshot_POD:
    def __init__(
        self,
        data: np.ndarray = None,
        load_local: bool = False,
        local_data_foldpath: str = None,
    ) -> None:
        """Performs Proper orthogonal decomposition of data using snapshot method.

        do not subtract the mean in the data. Because this process is done by the code here. 
        
        data should be arranged in 2D matrix. Samples are to be arranged in rows. Hence if single sample contains 10 data and there are shuch 20 samples then the data matrix should be of 20 X 10 shape. Single row signifies the data collected at multiple points at any given time. And single column signifies the data collected at single point at multiple time.

        arrange the data in (N X M) matrix in such a way that element $A_{ij}$ is the measurement of the $j^{th}$ point in space at $i^{th}$ time frame.

        Parameters
        ----------
        data : np.ndarray, optional
            (N X M) data matrix. by default None.
        load_local : bool, optional
            whether to load previously calculated and saved data, by default False
        local_data_foldpath : str, optional
            If folder path is given then the calculated POD will be saved there. If load_local is True then from this folder path, the POD modes are read. by default None
        """

        self.local_data_foldpath = local_data_foldpath
        self.load_local = load_local

        self._U = None
        self._V_T = None
        self._eps = None
        self._data_mean = None

        if load_local:
            pass
        else:
            self.fit(data)
                

        
    @property
    def U_filepath(self):
        return os.path.join(self.local_data_foldpath, "U.npy")

    @property
    def U(self)->np.ndarray:
        # if self.load_local:
        if self.local_data_foldpath is not None:
            return np.load(self.U_filepath)
        else:
            return self._U
    
    @U.setter
    def U(self, arr1:np.ndarray)->None:
        if self.local_data_foldpath is not None:
            np.save(file=self.U_filepath, arr=arr1)
        else:
            self._U = arr1
        return
    


    @property
    def V_T_filepath(self):
        return os.path.join(self.local_data_foldpath, "V_T.npy")

    @property
    def V_T(self)->np.ndarray:
        # if self.load_local:
        if self.local_data_foldpath is not None:
            return np.load(self.V_T_filepath)
        else:
            return self._V_T
    
    @V_T.setter
    def V_T(self, arr1:np.ndarray)->None:
        if self.local_data_foldpath is not None:
            np.save(file=self.V_T_filepath, arr=arr1)
        else:
            self._V_T = arr1
        return
    


    @property
    def eps_filepath(self):
        return os.path.join(self.local_data_foldpath, "eps.npy")

    @property
    def eps(self)->np.ndarray:
        # if self.load_local:
        if self.local_data_foldpath is not None:
            return np.load(self.eps_filepath)
        else:
            return self._eps
    
    @eps.setter
    def eps(self, arr1:np.ndarray)->None:
        if self.local_data_foldpath is not None:
            np.save(file=self.eps_filepath, arr=arr1)
        else:
            self._eps = arr1
        return
    
    
    
    @property
    def data_mean_filepath(self):
        return os.path.join(self.local_data_foldpath, "data_mean.npy")

    @property
    def data_mean(self)->np.ndarray:
        # if self.load_local:
        if self.local_data_foldpath is not None:
            return np.load(self.data_mean_filepath)
        else:
            return self._data_mean
    
    @data_mean.setter
    def data_mean(self, arr1:np.ndarray)->None:
        if self.local_data_foldpath is not None:
            np.save(file=self.data_mean_filepath, arr=arr1)
        else:
            self._data_mean = arr1
        return
    

    

    def fit(self, data: np.ndarray) -> None:
        """Calculates the POD modes from the data.

        Parameters
        ----------
        data : np.ndarray
            Data
        """
        self.data_mean = data.mean(axis=0)
        data1 = data - self.data_mean

        R = np.matmul(data1, data1.T)

        eigvel, eigvec = np.linalg.eig(R)
        idx = np.argsort(eigvel)[::-1]

        eigvel = np.abs(eigvel)
        eigvel = eigvel[idx]
        eigvel = eigvel ** 0.5
        eigvel = eigvel + 10 ** -18

        eigvec = eigvec[:, idx]

        self.V_T = (eigvec.T @ data1) / eigvel.reshape(-1, 1)
        self.U = eigvec
        self.eps = eigvel


    def mode(self, n=0):
        return self.V_T[n, :]

    def time_coeff(self, n=0):
        return self.U[:, n]

    def singular_value(self, n=0):
        return self.eps[n]

    def reconstruct_data(self, n_modes=10):
        return (
            self.U[:, :n_modes] @ np.diag(self.eps[:n_modes]) @ self.V_T[:n_modes, :]
        ) + self.data_mean





# class snapshot_POD:
#     def __init__(
#         self,
#         data: np.ndarray = None,
#         load_local: bool = False,
#         local_data_foldpath: str = None,
#     ) -> None:
#         """Performs Proper orthogonal decomposition of data using snapshot method.

#         do not subtract the mean in the data. Because this process is done by the code here. 
        
#         data should be arranged in 2D matrix. Samples are to be arranged in rows. Hence if single sample contains 10 data and there are shuch 20 samples then the data matrix should be of 20 X 10 shape. Single row signifies the data collected at multiple points at any given time. And single column signifies the data collected at single point at multiple time.

#         arrange the data in (N X M) matrix in such a way that element $A_{ij}$ is the measurement of the $j^{th}$ point in space at $i^{th}$ time frame.

#         Parameters
#         ----------
#         data : np.ndarray, optional
#             (N X M) data matrix. by default None.
#         load_local : bool, optional
#             whether to load previously calculated and saved data, by default False
#         local_data_foldpath : str, optional
#             If folder path is given then the calculated POD will be saved there. If load_local is True then from this folder path, the POD modes are read. by default None
#         """

#         self.local_data_foldpath = local_data_foldpath

#         if local_data_foldpath is not None:
#             self.data_mean_filepath = os.path.join(local_data_foldpath, "data_mean.npy")
#             self.V_T_filepath = os.path.join(local_data_foldpath, "V_T.npy")
#             self.U_filepath = os.path.join(local_data_foldpath, "U.npy")
#             self.eps_filepath = os.path.join(local_data_foldpath, "eps.npy")

#         if load_local:
#             self.data_mean = np.load(self.data_mean_filepath)
#             self.V_T = np.load(self.V_T_filepath)
#             self.U = np.load(self.U_filepath)
#             self.eps = np.load(self.eps_filepath)
#         else:
#             self.fit(data)
    

#     def fit(self, data: np.ndarray) -> None:
#         """Calculates the POD modes from the data.

#         Parameters
#         ----------
#         data : np.ndarray
#             Data
#         """
#         self.data_mean = data.mean(axis=0)
#         data1 = data - self.data_mean

#         R = np.matmul(data1, data1.T)

#         eigvel, eigvec = np.linalg.eig(R)
#         idx = np.argsort(eigvel)[::-1]

#         eigvel = np.abs(eigvel)
#         eigvel = eigvel[idx]
#         eigvel = eigvel ** 0.5
#         eigvel = eigvel + 10 ** -18

#         eigvec = eigvec[:, idx]

#         self.V_T = (eigvec.T @ data1) / eigvel.reshape(-1, 1)
#         self.U = eigvec
#         self.eps = eigvel

#         if self.local_data_foldpath is not None:
#             np.save(file=self.U_filepath, arr=self.U)
#             np.save(file=self.V_T_filepath, arr=self.V_T)
#             np.save(file=self.eps_filepath, arr=self.eps)
#             np.save(file=self.data_mean_filepath, arr=self.data_mean)

#     def mode(self, n=0):
#         return self.V_T[n, :]

#     def time_coeff(self, n=0):
#         return self.U[:, n]

#     def singular_value(self, n=0):
#         return self.eps[n]

#     def reconstruct_data(self, n_modes=10):
#         return (
#             self.U[:, :n_modes] @ np.diag(self.eps[:n_modes]) @ self.V_T[:n_modes, :]
#         ) + self.data_mean

