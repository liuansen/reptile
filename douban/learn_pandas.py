# _*_ coding: utf-8 _*_
__author__ = 'Anson'

import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(6, 3))    # 创建随机值并保存为DataFrame结构
print(df.head())
df.to_csv('numpppy.csv')
