import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('~/FIS-Projects/Module-3/FIS-Mod3-Project/data/pfi_pu.csv')

# Creates a sub-dataframe that removes N/A values
valid_grades_df = df.copy()
valid_grades_df = valid_grades_df[(valid_grades_df['SEGRADES'] != -1) & (valid_grades_df['SEGRADES'] != 5)]
# Categoricalize students into two groups based on school performance
valid_grades_df['student_performance'] = valid_grades_df['SEGRADES'].apply(lambda x: math.floor(x/2.5))

# Break the students into a high performing group and a low performing group
low_students_pi = valid_grades_df[valid_grades_df['student_performance'] == 1]['FSFREQ']
high_students_pi = valid_grades_df[valid_grades_df['student_performance'] == 0]['FSFREQ']

#####################
# Plots
#####################

# This plots the Parent's Participation Count
sns.distplot(valid_grades_df['FSFREQ'], kde=False)
plt.title("Parent's Participation Count")
plt.xlabel("Parent's participation hours at child's school")
plt.ylabel("Count")

# This plots the Parent's Participation distribution based on the student's
# performance in school
sns.distplot(low_students_pi, kde=False, norm_hist=True, color="b",
	            label="Low performing student", hist_kws=dict(alpha=0.3))
sns.distplot(high_students_pi, kde=False, norm_hist=True, color="r",
	            label="High performing student", hist_kws=dict(alpha=0.3))
plt.legend()
plt.title("Hours of parental involevment per year distribution")
plt.xlabel("Parent's participation hours at child's school")
plt.ylabel("Probability")
