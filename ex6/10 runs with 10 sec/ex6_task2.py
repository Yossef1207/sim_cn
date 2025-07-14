import json
import matplotlib.pyplot as plt
import pandas as pd
import os

# Ordner mit den .json-Dateien (anpassen falls nötig)
folder = "."
# Liste aller JSON-Dateien mit "seed_" im Namen
file_list = sorted([f for f in os.listdir(folder) if f.startswith("seed_") and f.endswith(".json")])

def plot_throughput_packet_per_second(df, run_name):
    df["time_bucket"] = (df["time"] // 1).astype(int)
    packets_per_second = df.groupby("time_bucket")["count"].sum()

    plt.figure(figsize=(14,5))
    plt.plot(packets_per_second.index, packets_per_second.values, label="Packets/sec")
    plt.axhline(packets_per_second.mean(), color='red', linestyle='--',
                label=f"Average: {packets_per_second.mean():.2f}")
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
            #df_bytes = pd.DataFrame({"time": vectors["time"], "bytes": vectors["value"]})
           # plot_throughput_bytes_per_second(df_bytes.copy(), filename)