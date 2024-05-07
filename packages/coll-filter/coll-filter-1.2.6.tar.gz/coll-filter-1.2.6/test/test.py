import os
import numpy as np
from typing import Generic, TypeVar

# print(os.cpu_count())

p = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
])
print(p)
print(p[:, 0])  # 第一列 [1 5 9]
print(p[:, 1])  # 第二列 [ 2  6 10]
print(p[0, :])  # 第一行
