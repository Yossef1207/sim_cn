import json
import matplotlib.pyplot as plt
import pandas as pd

# JSON laden
with open("delay_400/tcp_result.json") as f:
    data = json.load(f)

vectors = list(data.values())[0]["vectors"][0]
time = vectors["time"]

df = pd.DataFrame({"time": time})
df["count"] = 1  # jedes empfangene Paket = 1


def plot_throughput_packet_per_second(df):
    df["time_bucket"] = (df["time"] // 1).astype(int)
    packets_per_second = df.groupby("time_bucket")["count"].sum()

    # Plotten
    plt.figure(figsize=(14,5))
    plt.plot(packets_per_second.index, packets_per_second.values, label="Packets/sec")
    plt.axhline(packets_per_second.mean(), color='red', linestyle='--', label=f"Average: {packets_per_second.mean():.2f}")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (packets/sec)")
    plt.title("TCP Packet Arrival Rate (packetReceived)")
    plt.legend()
    plt.grid()
    plt.show()
    return plt


def plot_throughput_bytes_per_second(df):
    # vectors["value"] enthält dann Bytegrößen pro Paket
    df = pd.DataFrame({"time": vectors["time"], "bytes": vectors["value"]})
    df["time_bucket"] = (df["time"] // 1).astype(int)
    throughput_bps = df.groupby("time_bucket")["bytes"].sum()

    plt.plot(throughput_bps.index, throughput_bps.values)
    plt.title("TCP Throughput (bytes/sec)")
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput")
    plt.grid()
    plt.show()
    return plt

#plot_throughput_packet_per_second(df)
plot_throughput_bytes_per_second(df)