#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:48:36 2019
@author: Anil Onal
FIS Module 3 Project
Testing for the effects of parental involvement on student performance
using the National Household Education Survey data (2016)
Uses pi_df as the clean dataframe
"""
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import itertools
pi_df.describe().T
# Reduce dimensions of composite parental involvement indocators to two groups
pi_df['schl_comp'] = 'Low'
pi_df['hm_comp'] = 'Low'
i1 = pi_df.loc[pi_df.pi_pro_schl_feats_comp > \
               np.mean(pi_df.pi_pro_schl_feats_comp)].index
pi_df.loc[i1, 'schl_comp'] = 'High'
i2 = pi_df.loc[pi_df.pi_pro_hm_feats_comp > \
               np.mean(pi_df.pi_pro_hm_feats_comp)].index
pi_df.loc[i2, 'hm_comp'] = 'High'
# Identify high school - low home involvement, and
# low school - high home involvement groups
i1 = pi_df.loc[(pi_df.schl_comp == 'High') & (pi_df.hm_comp == 'Low')].index
i2 = pi_df.loc[(pi_df.schl_comp == 'Low') & (pi_df.hm_comp == 'High')].index
pi_df.loc[i1, 'schl_hm_comp'] = 'More involved at school'
pi_df.loc[i2, 'schl_hm_comp'] = 'More involved at home'
# Reduce dimensions in grades to 2
i1 = pi_df.loc[pi_df.SEGRADES <= 2].index
i2 = pi_df.loc[pi_df.SEGRADES >= 3].index
pi_df.loc[i1, 'grades_comp'] = 'A or B'
pi_df.loc[i2, 'grades_comp'] = 'C or lower'
# Test if grade distribution is independent between two groups
contingency_table = sm.stats.Table.from_data(pi_df[['schl_hm_comp', 'grades_comp']])    
rslt = contingency_table.test_nominal_association()
print(rslt.pvalue)
print(contingency_table.chi2_contribs)

      
pi_pro_schl_feats = ['FSSPORTX', 'FSVOL', 'FSMTNG', \
                     'FSPTMTNG', 'FSFUNDRS', 'FSCOMMTE']
pi_pro_hm_feats = ['FOSTORY2X', 'FOCRAFTS', 'FOGAMES', 'FOBUILDX', \
                   'FOSPORT', 'FOHISTX', 'FOLIBRAYX', 'FOBOOKSTX', \
                   'FOCONCRTX', 'FOMUSEUMX', 'FOZOOX', 'FOGROUPX', \
                   'FOSPRTEVX']
schl_feat_combins = list(itertools.combinations(pi_pro_schl_feats, 2))
# Proactive at-school parental involvement features show dependence. However,
# implications are less clear. Should we use one of them instead of all?
for combin in schl_feat_combins:
    contingency_table = sm.stats.Table.from_data(pi_df[[combin[0],combin[1]]])
    print(contingency_table.test_ordinal_association().pvalue, \
          contingency_table.test_ordinal_association().pvalue > 0.05)
    print(combin, contingency_table.chi2_contribs)
hm_feat_combins = list(itertools.combinations(pi_pro_hm_feats, 2))
# Proactive at-home parental involvement features also show dependence. However,
# implications are less clear. Should we use one of them instead of all?
for combin in hm_feat_combins:
    contingency_table = sm.stats.Table.from_data(pi_df[[combin[0],combin[1]]])
    print(contingency_table.test_ordinal_association().pvalue, \
          contingency_table.test_ordinal_association().pvalue > 0.05)
    print(combin, contingency_table.chi2_contribs)
