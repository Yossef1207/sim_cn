import matplotlib.pyplot as plt

durations = [10, 100, 1000]  # simulation times in seconds
means = [6.32, 42.98, 65.44]  # average packet throughput
ci_lows = [6.30, 42.78, 65.42]
ci_highs = [6.35, 43.17, 65.47]

# yerr muss zwei Listen enthalten: [untere Fehler, obere Fehler]
yerr = [
    [mean - low for mean, low in zip(means, ci_lows)],
    [high - mean for high, mean in zip(ci_highs, means)]
]

plt.figure(figsize=(10, 5))
plt.errorbar(durations, means, yerr=yerr, fmt='o-', capsize=5, label="95% Confidence Interval")
plt.xscale('log')  # log-Skala ist optional, aber bei 10/100/1000 oft hilfreich
plt.xlabel("Simulation Duration (s)")
plt.ylabel("Mean Throughput (packets/sec)")
plt.title("TCP Throughput with 95% Confidence Intervals")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()