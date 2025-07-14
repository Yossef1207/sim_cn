import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, chi2  # nur für Vergleich / kritischen Wert

# 1. JSON laden
with open("udp_exp_results.json") as f:
    data = json.load(f)

# 2. Ankunftszeiten extrahieren
root_key = list(data.keys())[0]
arrival_times = data[root_key]["vectors"][0]["time"]

# 3. Pakete pro Zeitfenster zählen
window_size = 1.0
max_time = max(arrival_times)
bins = np.arange(0, max_time + window_size, window_size)
counts, _ = np.histogram(arrival_times, bins=bins)

# 4. Erwartete Poisson-Häufigkeiten
lambda_hat = np.mean(counts)
values = np.arange(0, max(counts)+1)
expected_freq = poisson.pmf(values, mu=lambda_hat) * len(counts)

# 5. Beobachtete Häufigkeiten
observed_freq = np.bincount(counts, minlength=len(values))

# 6. Erwartete Häufigkeiten anpassen (normalisieren)
expected_freq *= observed_freq.sum() / expected_freq.sum()

# ✅ Eigene χ²-Berechnung (Aufgabe 5)
chi2_stat_custom = np.sum((observed_freq - expected_freq)**2 / expected_freq)

# Vergleich mit scipy (optional)
# from scipy.stats import chisquare
# chi2_builtin, pval_builtin = chisquare(f_obs=observed_freq, f_exp=expected_freq)

# 7. Freiheitsgrade (df = Anzahl Klassen - 1 - geschätzte Parameter)
df = len(values) - 1 - 1  # -1 wegen Summe 1, -1 wegen Lambda-Schätzung
p_value_custom = 1 - chi2.cdf(chi2_stat_custom, df)

# 8. Ausgabe
print(f"Eigene Chi²-Statistik: {chi2_stat_custom:.2f}")
print(f"Freiheitsgrade: {df}")
print(f"p-Wert (manuell): {p_value_custom:.4f}")

if p_value_custom > 0.05:
    print("✅ Akzeptiert: Daten passen zur Poissonverteilung.")
else:
    print("❌ Abgelehnt: Daten passen NICHT zur Poissonverteilung.")

# 9. Visualisierung
plt.bar(values, observed_freq, alpha=0.7, label='Observed')
plt.plot(values, expected_freq, 'r-', label='Expected (Poisson)')
plt.xlabel("Packet Count per Second")
plt.ylabel("Frequency")
plt.title("Custom Chi-Square Test for Packet Arrival Rates")
plt.legend()
plt.grid(True)
plt.show()
