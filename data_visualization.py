#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 10:43:10 2019

@author: flatironschol
"""
from statsmodels.graphics.mosaicplot import mosaic
import seaborn as sns
import matplotlib.pyplot as plt
i1 = pi_df.loc[pi_df.SEGRADES == 1].index
i2 = pi_df.loc[pi_df.SEGRADES == 2].index
i3 = pi_df.loc[pi_df.SEGRADES == 3].index
i4 = pi_df.loc[pi_df.SEGRADES == 4].index
pi_df.loc[i1, 'grades'] = 'A'
pi_df.loc[i2, 'grades'] = 'B'
pi_df.loc[i3, 'grades'] = 'C'
pi_df.loc[i4, 'grades'] = 'D or lower'
y = pi_df.grades.value_counts()
x = pi_df.grades.unique()
fig = plt.figure(figsize = (4, 5))
ax = sns.barplot(x, y, color = 'dodgerblue')
ax.set_title('Distribution of Student Grades')
ax.set_ylabel('Number of students')

fig = plt.figure(figsize = (6, 4))
ax = sns.distplot(pi_df.FSFREQ, color = 'orangered', kde = False)
ax.set_title('Distribution of Parental Involvement at School')
ax.set_ylabel('Number of parents')
ax.set_xlabel("Parent's participation hours at child's school")

i1 = pi_df.loc[pi_df.SEGRADES <= 2].index
i2 = pi_df.loc[pi_df.SEGRADES >= 3].index
pi_df.loc[i1, 'grades_comp'] = 'A or B'
pi_df.loc[i2, 'grades_comp'] = 'C or lower'
fig = plt.figure(figsize = (8, 4))
ax1 = sns.distplot(pi_df.loc[pi_df.grades_comp == 'A or B'].FSFREQ, color = 'orangered', norm_hist = True, kde = False, label = 'A or B')
sns.distplot(pi_df.loc[pi_df.grades_comp == 'C or lower'].FSFREQ, ax = ax1, color = 'blue', norm_hist = True, kde = False, label = 'C or lower')
ax1.set_title('Relationship Between Student Grades and \nDistribution of Parental Involvement at School')
ax1.set_ylabel('Probability')
ax1.set_xlabel("Parent's participation hours at child's school")
plt.legend()

fig = plt.figure(figsize = (6, 4))
ax1 = sns.distplot(pi_df.loc[pi_df.grades_comp == 'A or B'].pi_pro_schl_feats_comp, color = 'orangered', norm_hist = True, kde = False, label = 'A or B')
sns.distplot(pi_df.loc[pi_df.grades_comp == 'C or lower'].pi_pro_schl_feats_comp, ax = ax1, color = 'blue', norm_hist = True, kde = False, label = 'C or lower')
ax1.set_title('Relationship Between Student Grades and \nDistribution of Parental Involvement at School')
ax1.set_ylabel('Probability')
ax1.set_xlabel("Composite index for parent's involvement at school\n(Higher values indicate more involvement)")
plt.legend()

fig = plt.figure(figsize = (6, 4))
ax1 = sns.distplot(pi_df.loc[pi_df.grades_comp == 'A or B'].pi_pro_hm_feats_comp, color = 'orangered', norm_hist = True, kde = False, label = 'A or B')
sns.distplot(pi_df.loc[pi_df.grades_comp == 'C or lower'].pi_pro_hm_feats_comp, ax = ax1, color = 'blue', norm_hist = True, kde = False, label = 'C or lower')
ax1.set_title('Relationship Between Student Grades and \nDistribution of Parental Involvement at Home')
ax1.set_ylabel('Probability')
ax1.set_xlabel("Composite index for parent's involvement at home\n(Higher values indicate more involvement)")
plt.legend()

props = lambda key: {'color': 'dodgerblue' if 'More involved at home' in key else 'orange'}
labelizer = lambda k: ''
mosaic(pi_df[['schl_hm_comp', 'grades_comp']], index = ['schl_hm_comp', 'grades_comp'], \
       title = 'Relationship Between Student Grades and \nType of Parental Involvement', \
       properties = props, gap = 0.025, labelizer = labelizer)
