from scipy import stats

# Get means and standard deviations of the two student groups
valid_grades_df[['student_performance', 'FSFREQ']].groupby('student_performance').describe()

# Mann-Whitney U test
print(stats.mannwhitneyu(high_students_pi, low_students_pi,
	                        use_continuity=False, alternative=None))

# Calculate the Effect Size with Cohen's D
# Expected differences in mean is 0.
mean_1 = high_students_pi.mean()
mean_2 = low_students_pi.mean()
n_1 = len(high_students_pi)
n_2 = len(low_students_pi)
var1 = np.var(high_students_pi, ddof=1)
var2 = np.var(low_students_pi, ddof=1)

num = (n_1-1)*var1 + (n_2-1)*var2
denom = (n_1+n_2-2)
s_W = np.sqrt(num/denom)

d = np.abs(mean_1 - mean_2)/s_W

print(d)

# Calculate power
from statsmodels.stats.power import TTestIndPower
power_analysis = TTestIndPower()
power_analysis.solve_power(effect_size=d, nobs1=n_1, alpha=.05)
