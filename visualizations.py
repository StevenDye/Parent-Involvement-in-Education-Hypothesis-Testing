#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 10:43:10 2019
@author: Anil Onal & Steven Dye
FIS Module 3 Project
Data visualizations including descriptive stats
Run this file after data_prep.py, which produces input data for this file
"""
import numpy as np
import pandas as pd
from statsmodels.graphics.mosaicplot import mosaic
import seaborn as sns
import matplotlib.pyplot as plt
df_pi = pd.read_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/pi_df.csv')
# Recode SEGRADES to convert [1, 2, 3, 4] to ['A', 'B', 'C', 'D']
i1 = df_pi.loc[df_pi.SEGRADES == 1].index
i2 = df_pi.loc[df_pi.SEGRADES == 2].index
i3 = df_pi.loc[df_pi.SEGRADES == 3].index
i4 = df_pi.loc[df_pi.SEGRADES == 4].index
df_pi.loc[i1, 'grades'] = 'A'
df_pi.loc[i2, 'grades'] = 'B'
df_pi.loc[i3, 'grades'] = 'C'
df_pi.loc[i4, 'grades'] = 'D or lower'
# As a part of descriptive stats, distribution of grades, the main student
# performance feature
y = df_pi.grades.value_counts()
x = df_pi.grades.unique()
fig = plt.figure(figsize=(4, 5))
ax = sns.barplot(x, y, color='dodgerblue')
ax.set_title('Distribution of Student Grades')
ax.set_ylabel('Number of students')
# The distribution of the first parental involvement indicator, FSFREQ.
fig = plt.figure(figsize=(6, 4))
ax = sns.distplot(df_pi.FSFREQ, color='orange', kde=False, hist_kws={'alpha': 1})
ax.set_title('Distribution of Parental Involvement at School')
ax.set_ylabel('Number of parents')
ax.set_xlabel("Parent's participation hours at child's school")
# Break the students into a high performing group and a low performing group
i1 = df_pi.loc[df_pi.SEGRADES <= 2].index
i2 = df_pi.loc[df_pi.SEGRADES >= 3].index
df_pi.loc[i1, 'grades_comp'] = 'A or B'
df_pi.loc[i2, 'grades_comp'] = 'C or lower'
# FSFREQ distributions for high and low performing students
fig = plt.figure(figsize=(8, 4))
ax1 = sns.distplot(df_pi.loc[df_pi.grades_comp == 'A or B'].FSFREQ,
                   color='orange', norm_hist=True, hist_kws={'alpha': 0.8},
                   kde=False, label='A or B')
sns.distplot(df_pi.loc[df_pi.grades_comp == 'C or lower'].FSFREQ, ax=ax1,
             color='dodgerblue', norm_hist=True, hist_kws={'alpha': 0.8},
             kde=False, label='C or lower')
ax1.set_title('Relationship Between Student Grades and \nDistribution of Parental Involvement at School')
ax1.set_ylabel('Probability')
ax1.set_xlabel("Parent's participation hours at child's school")
plt.legend()
# Distributions of the composite at-school parental involvement indicator for
# high and low performing students
fig = plt.figure(figsize=(4, 4))
ax1 = sns.distplot(df_pi.loc[df_pi.grades_comp == 'A or B'].pi_pro_schl_feats_comp,
                   color='orange', bins=6,
                   norm_hist=True, hist_kws={'alpha': 0.8}, kde=False, label='A or B')
sns.distplot(df_pi.loc[df_pi.grades_comp == 'C or lower'].pi_pro_schl_feats_comp,
             ax=ax1, color='dodgerblue', bins=6, norm_hist=True,
             kde=False, hist_kws={'alpha': 0.8}, label='C or lower')
ax1.set_title('Relationship Between Student Grades and \nDistribution of Parental Involvement at School')
ax1.set_ylabel('Probability')
ax1.set_xlabel("Composite index for parent's involvement at school\n(Higher values indicate more involvement)")
plt.legend()
# Distributions of the composite at-home parental involvement indicator for
# high and low performing students
fig = plt.figure(figsize=(4, 4))
ax1 = sns.distplot(df_pi.loc[df_pi.grades_comp == 'A or B'].pi_pro_hm_feats_comp,
                   color='orange', bins=13, norm_hist=True,
                   hist_kws={'alpha': 0.8}, kde=False, label='A or B')
sns.distplot(df_pi.loc[df_pi.grades_comp == 'C or lower'].pi_pro_hm_feats_comp,
             ax=ax1, color='dodgerblue', norm_hist=True, bins=13,
             kde=False, hist_kws={'alpha': 0.8}, label='C or lower')
ax1.set_title('Relationship Between Student Grades and \nDistribution of Parental Involvement at Home')
ax1.set_ylabel('Probability')
ax1.set_xlabel("Composite index for parent's involvement at home\n(Higher values indicate more involvement)")
plt.legend()
plt.xticks(ticks=range(13, 27, 1), labels=range(13, 27, 1))
# For type of parental involvement analysis, reduce dimensions of composite
# parental involvement indocators to two groups
df_pi['schl_comp'] = 'Low'
df_pi['hm_comp'] = 'Low'
i1 = df_pi.loc[df_pi.pi_pro_schl_feats_comp >
               np.mean(df_pi.pi_pro_schl_feats_comp)].index
df_pi.loc[i1, 'schl_comp'] = 'High'
i2 = df_pi.loc[df_pi.pi_pro_hm_feats_comp >
               np.mean(df_pi.pi_pro_hm_feats_comp)].index
df_pi.loc[i2, 'hm_comp'] = 'High'
# Identify high school - low home involvement, and
# low school - high home involvement groups
i1 = df_pi.loc[(df_pi.schl_comp == 'High') & (df_pi.hm_comp == 'Low')].index
i2 = df_pi.loc[(df_pi.schl_comp == 'Low') & (df_pi.hm_comp == 'High')].index
df_pi.loc[i1, 'schl_hm_comp'] = 'More involved at school'
df_pi.loc[i2, 'schl_hm_comp'] = 'More involved at home'
# Plot of the contingency table for the type of parental involvement vs.
# student high-low performing students
props = lambda key: {'color': 'dodgerblue' if 'More involved at home' in key else 'orange'}
labelizer = lambda k: f"{(k == ('More involved at school', 'A or B'))*90 + (k == ('More involved at school', 'C or lower'))*10 + (k == ('More involved at home', 'A or B'))*84 + (k == ('More involved at home', 'C or lower'))*16}%"

mosaic(df_pi[['schl_hm_comp', 'grades_comp']], index=['schl_hm_comp', 'grades_comp'],
       title='Relationship Between Student Grades and \nType of Parental Involvement',
       properties=props, gap=0.025, labelizer=labelizer)
ax1.set_xticklabels(['More involved at school\nLess Involved at home', ''])
plt.show()
df_pi.to_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/df_pi.csv', sep=',')
