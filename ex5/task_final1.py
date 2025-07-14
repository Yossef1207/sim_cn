import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, chisquare, chi2

# -----------------------------
# Task 4: χ²-Test with Poisson
# -----------------------------

# Load JSON file
with open("udp_exp_results.json") as f:
    data = json.load(f)

# Extract arrival times
root_key = list(data.keys())[0]
arrival_times = data[root_key]["vectors"][0]["time"]

# Window size, e.g., 1 second
window_size = 1.0
max_time = max(arrival_times)
bins = np.arange(0, max_time + window_size, window_size)

# Count packets per window
counts, _ = np.histogram(arrival_times, bins=bins)

# Expected distribution (Poisson) based on average rate
lambda_hat = np.mean(counts)
values = np.arange(0, max(counts) + 1)
expected_probs = poisson.pmf(values, mu=lambda_hat)
expected_counts = expected_probs * len(counts)

# Count observed frequencies
observed_counts = np.array([np.sum(counts == k) for k in values])

# Scale expected counts to match observed total
expected_counts_scaled = expected_counts * (np.sum(observed_counts) / np.sum(expected_counts))

# χ²-Test (built-in function)
chi2_stat_builtin, p_val_builtin = chisquare(f_obs=observed_counts, f_exp=expected_counts_scaled)

# -----------------------------
# Task 5: Custom χ² function
# -----------------------------

def custom_chi_squared_test(observed, expected):
    observed = np.array(observed)
    expected = np.array(expected)
    chi2_stat = np.sum((observed - expected) ** 2 / expected)
    df = len(observed) - 1
    p_value = chi2.sf(chi2_stat, df)
    return chi2_stat, p_value

# Test with custom method
chi2_stat_custom, p_val_custom = custom_chi_squared_test(observed_counts, expected_counts_scaled)

# -----------------------------
# Print result comparison
# -----------------------------

print(f"\nEstimated lambda (λ): {lambda_hat:.4f}")
print(f"Built-in χ² value: {chi2_stat_builtin:.4f}, p-value: {p_val_builtin:.4f}")
print(f"Custom   χ² value: {chi2_stat_custom:.4f}, p-value: {p_val_custom:.4f}")

# Optional: Plot
plt.bar(values, observed_counts, alpha=0.6, label='Observed')
plt.plot(values, expected_counts_scaled, 'ro-', label='Expected (Poisson)')
plt.xlabel("Packets per window")
plt.ylabel("Number of windows")
plt.legend()
plt.title("χ²-Test: Observed vs. Poisson Distribution")
plt.grid(True)
plt.tight_layout()
plt.show()
