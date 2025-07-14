import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from scipy import stats

# Ordner mit den .json-Dateien (anpassen falls nötig)
folder = "."
# Liste aller JSON-Dateien mit "seed_" im Namen
file_list = sorted([f for f in os.listdir(folder) if f.startswith("seed_") and f.endswith(".json")])

# Für CI-Speicherung
mean_throughput_values = []

def plot_throughput_packet_per_second(df, run_name):
    df["time_bucket"] = (df["time"] // 1).astype(int)
    packets_per_second = df.groupby("time_bucket")["count"].sum()

    mean_packets = packets_per_second.mean()
    mean_throughput_values.append(mean_packets)  # Für CI-Berechnung

    plt.figure(figsize=(14, 5))
    plt.plot(packets_per_second.index, packets_per_second.values, label="Packets/sec")
    plt.axhline(mean_packets, color='red', linestyle='--',
                label=f"Average: {mean_packets:.2f}")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (packets/sec)")
    plt.title(f"TCP Packet Arrival Rate - {run_name}")
    plt.legend()
    plt.grid()
    plt.show()

def plot_throughput_bytes_per_second(df, run_name):
    df["time_bucket"] = (df["time"] // 1).astype(int)
    throughput_bps = df.groupby("time_bucket")["bytes"].sum()

    plt.figure(figsize=(14,5))
    plt.plot(throughput_bps.index, throughput_bps.values, label="Bytes/sec")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (bytes/sec)")
    plt.title(f"TCP Byte Throughput - {run_name}")
    plt.grid()
    plt.legend()
    plt.show()

# Verarbeitung aller Dateien
for filename in file_list:
    with open(os.path.join(folder, filename)) as f:
        data = json.load(f)
        vectors = list(data.values())[0]["vectors"][0]
        time = vectors["time"]
        df = pd.DataFrame({"time": time})
        df["count"] = 1

        # Packets pro Sekunde
        plot_throughput_packet_per_second(df.copy(), filename)

        # Bytes pro Sekunde (optional)
        # if "value" in vectors:
        #     df_bytes = pd.DataFrame({"time": vectors["time"], "bytes": vectors["value"]})
        #     plot_throughput_bytes_per_second(df_bytes.copy(), filename)

# Nach der Schleife: 95 % Confidence Interval berechnen
n = len(mean_throughput_values)
mean = np.mean(mean_throughput_values)
std_dev = np.std(mean_throughput_values, ddof=1)
confidence = 0.95
t_critical = stats.t.ppf(1 - (1 - confidence) / 2, df=n - 1)
margin_error = t_critical * (std_dev / np.sqrt(n))
ci_lower = mean - margin_error
ci_upper = mean + margin_error

print(f"\n📊 Across {n} runs:")
print(f"Mean throughput: {mean:.2f} packets/sec")
print(f"95% Confidence Interval: ({ci_lower:.2f}, {ci_upper:.2f})")