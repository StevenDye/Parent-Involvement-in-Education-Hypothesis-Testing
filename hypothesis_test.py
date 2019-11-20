#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:48:36 2019
@author: Anil Onal & Steven Dye
FIS Module 3 Project
Testing for the effects of parental involvement on student performance
using the National Household Education Survey data (2016)
Uses df_pi as the clean dataframe with constructed features
To produce this data, run data_prep.py and visualizations.py files, in the
given order.
"""
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import itertools
df_pi = pd.read_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/df_pi.csv')
df_pi.describe().T
# Get means and standard deviations of FSFREQ for high and low performing students
df_pi[['grades_comp', 'FSFREQ']].groupby('grades_comp').describe()
# Mann-Whitney U test for FSFREQ - parent's number of hours at school
# H0 : The distributions of FSFREQ for high and low performing students
# came from the same population  
high_students_pi = df_pi.loc[df_pi.grades_comp == 'A or B'].FSFREQ
low_students_pi = df_pi.loc[df_pi.grades_comp == 'C or lower'].FSFREQ
print(stats.mannwhitneyu(high_students_pi, low_students_pi, \
	                     use_continuity=False, alternative=None))
# Use chi-2 test to find out if the distribution of each composite parental
# involvemet index is related with the student performance being high or low
# H0: Student performance is not related with the distributions of parental
# involvement 
# At-school involvement
contingency_table = sm.stats.Table.from_data(df_pi[['grades_comp', \
                                                    'pi_pro_schl_feats_comp']])    
print(contingency_table.test_nominal_association())
print(contingency_table.chi2_contribs)
# Same chi-2 test for at-home involvement
contingency_table = sm.stats.Table.from_data(df_pi[['grades_comp', \
                                                    'pi_pro_hm_feats_comp']])    
print(contingency_table.test_nominal_association())
print(contingency_table.chi2_contribs)
# Use chi-2 test to find out if the type of parental involvement is related
# with the occurances of high and low performing students
# H0: No relation.
contingency_table = sm.stats.Table.from_data(df_pi[['schl_hm_comp', 'grades_comp']])    
print(contingency_table.test_nominal_association())
# Test for relation of parental involvement features
# This section is for future analysis
pi_pro_schl_feats = ['FSSPORTX', 'FSVOL', 'FSMTNG',
                     'FSPTMTNG', 'FSFUNDRS', 'FSCOMMTE']
schl_feat_combins = list(itertools.combinations(pi_pro_schl_feats, 2))
# Proactive at-school parental involvement features show dependence. However,
# implications are less clear. Should we use one of them instead of all?
for combin in schl_feat_combins:
    contingency_table = sm.stats.Table.from_data(df_pi[[combin[0],combin[1]]])
    print(contingency_table.test_ordinal_association().pvalue, \
          contingency_table.test_ordinal_association().pvalue > 0.05)
    print(combin, contingency_table.chi2_contribs)
pi_pro_hm_feats = ['FOSTORY2X', 'FOCRAFTS', 'FOGAMES', 'FOBUILDX',
                   'FOSPORT', 'FOHISTX', 'FOLIBRAYX', 'FOBOOKSTX',
                   'FOCONCRTX', 'FOMUSEUMX', 'FOZOOX', 'FOGROUPX',
                   'FOSPRTEVX']
hm_feat_combins = list(itertools.combinations(pi_pro_hm_feats, 2))
# Proactive at-home parental involvement features also show dependence. However,
# implications are less clear. Should we use one of them instead of all?
for combin in hm_feat_combins:
    contingency_table = sm.stats.Table.from_data(df_pi[[combin[0],combin[1]]])
    print(contingency_table.test_ordinal_association().pvalue, \
          contingency_table.test_ordinal_association().pvalue > 0.05)
    print(combin, contingency_table.chi2_contribs)