import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, chisquare

# 1. Load JSON file
with open("udp_exp_results.json") as f:
    data = json.load(f)

# 2. Extract arrival times
root_key = list(data.keys())[0]
arrival_times = data[root_key]["vectors"][0]["time"]

# 3. Calculate arrival rates (# packets per second)
window_size = 1.0  # 1 second
max_time = max(arrival_times)
bins = np.arange(0, max_time + window_size, window_size)
counts, _ = np.histogram(arrival_times, bins=bins)

# 4. Calculate expected frequencies according to Poisson
lambda_hat = np.mean(counts)
values = np.arange(0, max(counts)+1)
expected_freq = poisson.pmf(values, mu=lambda_hat) * len(counts)

# 5. Calculate observed frequencies
observed_freq = np.bincount(counts, minlength=len(values))

# 6. Adjust expected frequencies to match observed total
expected_freq *= observed_freq.sum() / expected_freq.sum()

# 7. Perform χ² test
chi2_stat, p_value = chisquare(f_obs=observed_freq, f_exp=expected_freq)

# 8. Print results
print(f"Estimated λ (lambda_hat): {lambda_hat:.2f}")
print(f"Chi² statistic: {chi2_stat:.2f}")
print(f"p-value: {p_value:.4f}")
if p_value > 0.05:
    print("✅ The data fits the Poisson distribution well (p > 0.05).")
else:
    print("❌ The data does NOT fit the Poisson distribution well (p <= 0.05).")

# 9. Visualization
plt.bar(values, observed_freq, alpha=0.7, label='Observed')
plt.plot(values, expected_freq, 'r-', label='Expected (Poisson)')
plt.xlabel("Packet Count per Second")
plt.ylabel("Frequency")
plt.title("Chi-Square Goodness-of-Fit for Packet Arrival Rates")
plt.legend()
plt.grid(True)
plt.show()
