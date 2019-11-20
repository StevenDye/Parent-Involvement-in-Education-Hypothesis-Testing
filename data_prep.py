#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:52:48 2019
@author: Anil Onal & Steven Dye
FIS Module 3 Project
Cleaning of the National Household Education Survey data (2016)
pi_df is the clean dataframe
"""
import pandas as pd

df = pd.read_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/pfi_pu.csv')
# Features that measure student performance
perf_feats = ['SEENJOY', 'SEGRADES', 'SEABSNT', 'SEREPEAT', 'SESUSPIN']
# Features that measure parental involvement at school
# Some types of involvement are considered to respond to student performance
# All features are binary with the exception of one.
pi_pro_schl_feats = ['FSSPORTX', 'FSVOL', 'FSMTNG',
                     'FSPTMTNG', 'FSFUNDRS', 'FSCOMMTE']
pi_rea_schl_feats = ['FSATCNFN', 'FSCOUNSLR']
pi_freq_schl_feats = ['FSFREQ']
# Features that measure parental involvement at home
# Some types of involvement are considered to respond to student performance
# All features are binary with the exception of one.
pi_pro_hm_feats = ['FOSTORY2X', 'FOCRAFTS', 'FOGAMES', 'FOBUILDX',
                   'FOSPORT', 'FOHISTX', 'FOLIBRAYX', 'FOBOOKSTX',
                   'FOCONCRTX', 'FOMUSEUMX', 'FOZOOX', 'FOGROUPX',
                   'FOSPRTEVX']
pi_rea_hm_feats = ['FHCHECKX', 'FHHELP', 'FORESPON']
pi_freq_hm_feats = ['FODINNERX']
# Combine all the features into a single list
feats = perf_feats.copy()
for feat in [pi_pro_schl_feats, pi_rea_schl_feats, pi_freq_schl_feats, \
             pi_pro_hm_feats, pi_rea_hm_feats, pi_freq_hm_feats]:
    feats.extend(feat)
# Append full sample weights
feats.append('FPWT')
df_cp = df.copy()[feats]
# Drop observations with N/A values
for c in df_cp.columns:
    df_cp = df_cp.drop(df_cp.loc[df_cp[c] < 0].index)
    if c == 'SEGRADES':
        df_cp = df_cp.drop(df_cp.loc[df_cp[c] == 5].index)
# This function recodes binary parental involvement features so that
# 1 shows less involvement and 2 shows more
def feature_cleaning(features):
    for feat in features:
        i1 = df_cp.loc[df_cp[feat] == 1].index
        i2 = df_cp.loc[df_cp[feat] == 2].index
        df_cp.loc[i1, feat] = 2
        df_cp.loc[i2, feat] = 1
# Remove invalid entries from these features
for feat in [pi_pro_schl_feats, pi_rea_schl_feats, \
             pi_pro_hm_feats, pi_rea_hm_feats]:
    feature_cleaning(feat)
# Create composite indices for proactive parental involvement
df_cp['pi_pro_schl_feats_comp'] = df_cp[pi_pro_schl_feats].sum(axis=1)
df_cp['pi_pro_hm_feats_comp'] = df_cp[pi_pro_hm_feats].sum(axis=1)
pi_df = df_cp.copy()
pi_df.to_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/pi_df.csv', sep = ',')
