from scipy import stats

# Get means and standard deviations of the two student groups
valid_grades_df[['student_performance', 'FSFREQ']].groupby('student_performance').describe()

# Mann-Whitney U test
print(stats.mannwhitneyu(high_students_pi, low_students_pi,
	                        use_continuity=False, alternative=None))
