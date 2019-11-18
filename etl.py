#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:52:48 2019
@author: Anil Onal
FIS Module 3 Project

"""
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import itertools
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/pfi_pu.csv')
perf_feats = ['SEENJOY', 'SEGRADES', 'SEABSNT', 'SEREPEAT', 'SESUSPIN']
pi_pro_schl_feats = ['FSSPORTX', 'FSVOL', 'FSMTNG', \
                     'FSPTMTNG', 'FSFUNDRS', 'FSCOMMTE']
pi_rea_schl_feats = ['FSATCNFN', 'FSCOUNSLR']
pi_freq_schl_feats = ['FSFREQ']
pi_pro_hm_feats = ['FOSTORY2X', 'FOCRAFTS', 'FOGAMES', 'FOBUILDX', \
                   'FOSPORT', 'FOHISTX', 'FOLIBRAYX', 'FOBOOKSTX', \
                   'FOCONCRTX', 'FOMUSEUMX', 'FOZOOX', 'FOGROUPX', \
                   'FOSPRTEVX']
pi_rea_hm_feats = ['FHCHECKX', 'FHHELP', 'FORESPON']
pi_freq_hm_feats = ['FODINNERX']
feats = perf_feats.copy()
feats.extend(pi_pro_schl_feats)
feats.extend(pi_rea_schl_feats)
feats.extend(pi_freq_schl_feats)
feats.extend(pi_pro_hm_feats)
feats.extend(pi_rea_hm_feats)
feats.extend(pi_freq_hm_feats)
df_cp = df.copy()[feats]
for c in df_cp.columns:
    df_cp = df_cp.drop(df_cp.loc[df_cp[c] < 0].index)  
    if c == 'SEGRADES':
        df_cp = df_cp.drop(df_cp.loc[df_cp[c] == 5].index)
for feat in pi_pro_schl_feats:
    i1 = df_cp.loc[df_cp[feat] == 1].index
    i2 = df_cp.loc[df_cp[feat] == 2].index
    df_cp.loc[i1, feat] = 'More involved'
    df_cp.loc[i2, feat] = 'Less involved'
df_cp['pi_pro_schl_feats_comp'] = df_cp[pi_pro_schl_feats].sum(axis = 1)

i1 = df_cp.loc[df_cp.SEGRADES == 1].index
i2 = df_cp.loc[df_cp.SEGRADES == 2].index
i3 = df_cp.loc[df_cp.SEGRADES == 3].index
i4 = df_cp.loc[df_cp.SEGRADES == 4].index
df_cp.loc[i1, 'SEGRADES'] = 'A'
df_cp.loc[i2, 'SEGRADES'] = 'B'
df_cp.loc[i3, 'SEGRADES'] = 'C'
df_cp.loc[i4, 'SEGRADES'] = 'D or lower'
    
schl_feat_combins = list(itertools.combinations(pi_pro_schl_feats, 2))
pi_schl_feats_corr = []
for combin in schl_feat_combins:
    data = df_cp[[combin[0],combin[1]]]
    contingency_table = sm.stats.Table.from_data(data)
    rslt = contingency_table.test_nominal_association()
    print(rslt.pvalue)
    print(contingency_table.chi2_contribs)

contingency_table = sm.stats.Table.from_data(df_cp[['FSVOL', 'SEGRADES']])    
rslt = contingency_table.test_nominal_association()
print(rslt.pvalue)
print(contingency_table.chi2_contribs)

from statsmodels.graphics.mosaicplot import mosaic
props = lambda key: {'color': 'r' if 'Less involved' in key else 'g'}

mosaic(df_cp[['FSVOL', 'SEGRADES']], index = ['FSVOL', 'SEGRADES'], \
       title = 'Relationship Between Parental Involvement and Grades', \
       properties = props, gap=0.025)

contingency_table = sm.stats.Table.from_data(df_cp[['FSVOL', 'SEREPEAT']])    
rslt = contingency_table.test_nominal_association()
print(rslt.pvalue)
print(contingency_table.chi2_contribs)
    
 = [] 
for feat in pi_pro_schl_feats:
    d = pd.DataFrame({feat: list(Counter(df_cp[feat]).values())}, index = list(Counter(df_cp[feat]).keys()))
    contingency_table.append(d)
contingency_table = pd.concat(contingency_table, axis = 1)    

pi_schl_feats_corr = [stats.chi2_contingency(contingency_table[[i[0],i[1]]]) for i in schl_feat_combins]




sns.distplot(df_cp.loc[df_cp.SEGRADES == 1].pi_pro_schl_feats_comp, bins = 20)
sns.distplot(df_cp.loc[df_cp.SEGRADES == 4].pi_pro_schl_feats_comp, bins = 20)
stats.ttest_ind(df_cp.loc[df_cp.SEGRADES == 1].pi_pro_schl_feats_comp, df_cp.loc[df_cp.SEGRADES == 4].pi_pro_schl_feats_comp, equal_var = False)

sns.distplot(df_cp.loc[df_cp.SESUSPIN == 1].pi_pro_schl_feats_comp, bins = 20)
sns.distplot(df_cp.loc[df_cp.SESUSPIN == 2].pi_pro_schl_feats_comp, bins = 20)
stats.ttest_ind(df_cp.loc[df_cp.SESUSPIN == 1].pi_pro_schl_feats_comp, df_cp.loc[df_cp.SESUSPIN == 2].pi_pro_schl_feats_comp, equal_var = False)

for feat in pi_pro_hm_feats:
    i1 = df_cp.loc[df_cp[feat] == 1].index
    i2 = df_cp.loc[df_cp[feat] == 2].index
    df_cp.loc[i1, feat] = 2
    df_cp.loc[i2, feat] = 1
df_cp['pi_pro_hm_feats_comp'] = df_cp[pi_pro_hm_feats].sum(axis = 1)
sns.distplot(df_cp.loc[df_cp.SEGRADES == 1].pi_pro_hm_feats_comp, bins = 20)
sns.distplot(df_cp.loc[df_cp.SEGRADES == 4].pi_pro_hm_feats_comp, bins = 20)
stats.ttest_ind(df_cp.loc[df_cp.SEGRADES == 1].pi_pro_hm_feats_comp, df_cp.loc[df_cp.SEGRADES == 4].pi_pro_hm_feats_comp, equal_var = False)

sns.distplot(df_cp.loc[df_cp.SESUSPIN == 1].pi_pro_hm_feats_comp, bins = 10)
sns.distplot(df_cp.loc[df_cp.SESUSPIN == 2].pi_pro_hm_feats_comp, bins = 10)
stats.ttest_ind(df_cp.loc[df_cp.SESUSPIN == 1].pi_pro_hm_feats_comp, df_cp.loc[df_cp.SESUSPIN == 2].pi_pro_hm_feats_comp, equal_var = False)

sns.distplot(df_cp.loc[df_cp.SEGRADES == 1].hm_composite_feat)
sns.distplot(df_cp.loc[df_cp.SEGRADES == 4].hm_composite_feat)

sns.distplot(df_cp.loc[df_cp.FSVOL == 1].SEGRADES, bins = 20)
sns.distplot(df_cp.loc[df_cp.FSVOL == 2].SEGRADES, bins = 20)
stats.ttest_ind(df_cp.loc[df_cp.FSVOL == 1].SEGRADES, df_cp.loc[df_cp.FSVOL == 2].SEGRADES, equal_var = False)



