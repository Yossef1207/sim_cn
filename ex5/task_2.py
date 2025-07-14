import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 1. Generate samples
np.random.seed(42)
lambda_poisson = 4
sample_size = 1000
samples = np.random.poisson(lam=lambda_poisson, size=sample_size)

# 2. Observed frequencies
values, observed_freq = np.unique(samples, return_counts=True)

# 3. Expected frequencies from Poisson PMF
expected_freq = stats.poisson.pmf(values, mu=np.mean(samples)) * sample_size
expected_freq *= observed_freq.sum() / expected_freq.sum()  # normalize to match total count

# 4. Chi-squared test
chi2_statistic, p_value = stats.chisquare(f_obs=observed_freq, f_exp=expected_freq)

# 5. Output results
print("Chi-squared Statistic:", chi2_statistic)
print("p-value:", p_value)

# 6. Plot observed vs expected
plt.bar(values, observed_freq, width=0.4, label="Observed", alpha=0.6)
plt.bar(values + 0.4, expected_freq, width=0.4, label="Expected (Poisson)", alpha=0.6)
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Chi-squared Goodness-of-Fit: Poisson Distribution")
plt.legend()
plt.grid(True)
plt.show()
