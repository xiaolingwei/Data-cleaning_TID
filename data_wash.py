# -*- coding: utf-8 -*-
"""
Created on Wed May  5 12:25:51 2021

@author: MYM
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


# 将不同行业的样本分类

# 读入样本数据
data = pd.read_csv('附件2.csv')
# 读取不同行业的代码
code = pd.read_excel('附件1.xlsx')

#所属行业的集合
area_set = set(code.所属行业)
data_dict = dict()
code_dict = dict()
for x in area_set:
     code_dict.update({x:code[code.所属行业 == x].股票代码})  
     df1 = data.drop(data.index)
     for y in code_dict[x]:  # 逐个取某行业的股票代码
         y = round(y)
         df1 = df1.append(data.loc[data['TICKER_SYMBOL']== y], ignore_index = True)
     data_dict.update({x:df1})
     df1.to_csv( x +'.csv')







# data_profect = data.dropna(axis=0)  #全部数据都存在丢失情况
# data_base = data.dropna(how = 'all')  # 没有全部缺失的数据


# 数据筛除与填充
for x in area_set:
    data = pd.read_csv( x +'.csv')
    num = len(data)
    #  删除FLAG不知道的
    df = data.drop(data[pd.isnull(data.FLAG)].index)
    #筛选参数
    data_para = df.dropna(axis = 1 ,thresh = round(0.2*num)) #  几成的公司有这项参数的留下
    #筛选公司
    data_company = data_para.dropna(axis = 0,thresh= 30)    # 每个公司至少有多少项参数的留下
    df_out = data_company
    #  删除参数不变的
    df_out = df_out.drop(labels = ['REPORT_TYPE','FISCAL_PERIOD','MERGED_FLAG','ACCOUTING_STANDARDS','CURRENCY_CD'], axis = 1)
    # 插值
    imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')  # 实例化，均值填充
    df_mean = imp_mean.fit_transform(df_out)     #  fit_transform一步完成调取结果
    df_out.iloc[:,:] = df_mean
    df_out.to_csv('清洗后_' + x + '.csv')










