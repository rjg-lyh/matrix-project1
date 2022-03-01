import pandas as pd
import numpy as np
from .base import AoiInfo


class SinfInfo(AoiInfo):
    def __init__(self, sinf_info):
        self.sinf_info = sinf_info

    @property
    def setup_id(self) -> str:
        return self.sinf_info['setup_id']

    @property
    def lot_id(self) -> str:
        return self.sinf_info['lot_id']

    @property
    def wafer_id(self) -> str:
        return self.sinf_info['wafer_id']

    
    @property
    def label_map(self) -> np.ndarray:
        return self.sinf_info['label_map']


    @classmethod
    def from_sinf_path(cls, sinf_path):
        with open(sinf_path, 'r')as f:
            sinf_data = f.readlines()

        setupid = sinf_data[0].split(':')[-1].split('\n')[0]
        lotid   = sinf_data[1].split(':')[-1].split('\n')[0]
        waferid = sinf_data[2].split(':')[-1].split('\n')[0]
        core_sinf_data = sinf_data[12:]
        core_sinf_data = [i.replace('RowData:', '')  for i in core_sinf_data]
        core_sinf_data = [i.replace('\n', '')  for i in core_sinf_data]
        core_sinf_data = [i.split(' ') for i in core_sinf_data]

        core_sinf_array = cls.decode_core_sinf_data(core_sinf_data)

        sinf_info = dict(
            file_name = sinf_path,
            setup_id  = setupid,
            lot_id    = lotid,
            wafer_id  = waferid,
            label_map = core_sinf_array
        )
        return cls(sinf_info)


    @staticmethod
    def decode_core_sinf_data(core_sinf_data):
        sinf_data_map = pd.DataFrame(core_sinf_data)
        row, col = sinf_data_map.shape

        core_sinf_array = np.zeros([col, row], dtype='int64')
        for i in range(row):
            for j in range(col):
                sinf_value = sinf_data_map[j][i]
                if sinf_value == '__':
                    YIndex = row - (i + 1)
                    XIndex = j
                    core_sinf_array[XIndex][YIndex] = -1
                else:
                    YIndex = row - (i + 1)
                    XIndex = j
                    core_sinf_array[XIndex][YIndex] = int(sinf_value, 16)

        return core_sinf_array
