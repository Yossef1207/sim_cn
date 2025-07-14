import json
import matplotlib.pyplot as plt
import pandas as pd
import os

# Verzeichnis mit den .json-Dateien
folder = "10 runs with 10 sec"  # ggf. anpassen

# Alle Dateien, die mit TCP_10s_Repetitions_run*.json enden
file_list = sorted([f for f in os.listdir(folder) if f.startswith("TCP_10s_Repetitions_run") and f.endswith(".json")])

# Alle Daten sammeln
all_dfs = []

for filename in file_list:
    with open(os.path.join(folder, filename)) as f:
        data = json.load(f)
        vectors = list(data.values())[0]["vectors"][0]
        time = vectors["time"]
        df = pd.DataFrame({"time": time})
        df["count"] = 1
        df["run"] = filename  # Run-Kennung merken
        all_dfs.append(df)

# Alle DataFrames zusammenfügen
full_df = pd.concat(all_dfs)

# Gruppieren nach Sekunde und Mittelwert berechnen
full_df["time_bucket"] = (full_df["time"] // 1).astype(int)
throughput_by_second = full_df.groupby(["time_bucket", "run"])["count"].sum().unstack()
mean_throughput = throughput_by_second.mean(axis=1)

# Plot
plt.figure(figsize=(14, 5))
plt.plot(mean_throughput.index, mean_throughput.values, label="Avg. Packets/sec over 10 runs")
plt.axhline(mean_throughput.mean(), color='red', linestyle='--', label=f"Overall Avg: {mean_throughput.mean():.2f}")
plt.xlabel("Time (s)")
plt.ylabel("Throughput (packets/sec)")
plt.title("Average TCP Packet Arrival Rate (10 runs)")
plt.legend()
plt.grid()
plt.show()