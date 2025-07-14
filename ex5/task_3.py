import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

# JSON-Datei laden
with open("udp_exp_results.json") as f:
    data = json.load(f)

# Zeiten extrahieren (aus dem ersten Vector-Eintrag)
root_key = list(data.keys())[0]
arrival_times = data[root_key]["vectors"][0]["time"]

# Inter-Arrival-Zeiten berechnen
inter_arrival_times = np.diff(arrival_times)

# Histogramm und Exponentialverteilung plotten
plt.hist(inter_arrival_times, bins=30, density=True, alpha=0.7, label='Observed')

# Exponentialverteilung fitten
loc, scale = expon.fit(inter_arrival_times)
x = np.linspace(0, max(inter_arrival_times), 100)
plt.plot(x, expon.pdf(x, loc=loc, scale=scale), color='red', label='Fitted Exponential')

# Plot dekorieren
plt.xlabel("Inter-Arrival Time (s)")
plt.ylabel("Density")
plt.title("UDP Packet Inter-Arrival Times (fitted to Exponential)")
plt.legend()
plt.grid(True)
plt.show()
