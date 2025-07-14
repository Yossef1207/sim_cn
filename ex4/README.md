Danke für die Klarstellung und den Screenshot! Jetzt ist ganz klar, was du meinst:

---

## ❌ Was ist gerade falsch?

Dein aktueller Plot zeigt:

* **kumulative Anzahl** empfangener Pakete (`packetReceived`), also einfach ein wachsender Zähler.
* Dieser wächst **linear**, daher sieht der Graph glatt aus, ohne TCP-typische Schwankungen.

---

## ✅ Was du stattdessen brauchst:

Du willst das **TCP-Verhalten im Zeitverlauf** sehen – also den **Throughput in Byte/s oder Pakete/s**, damit du:

* Slow Start,
* Congestion Avoidance,
* Fast Recovery etc. erkennen kannst.

**Das erreichst du nicht mit einer kumulativen Zählung**, sondern durch die **Rate der empfangenen Pakete pro Zeitintervall** (z. B. pro Sekunde).

---

## 🔁 Die richtige Visualisierung: „Paketrate pro Sekunde“

Hier ist der Code:

```python
import json
import matplotlib.pyplot as plt
import pandas as pd

# JSON laden
with open("tcp_result.json") as f:
    data = json.load(f)

vectors = list(data.values())[0]["vectors"][0]
time = vectors["time"]

df = pd.DataFrame({"time": time})
df["count"] = 1  # jedes empfangene Paket = 1

# Bucketing: Pakete pro Sekunde
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
```

---

### ✅ Warum funktioniert das?

* Die Schwankungen zeigen den **TCP-Staukontrollmechanismus**.
* Du siehst Anstieg → Einbruch → Erholung (klassisches TCP-Muster).
* Das ist viel aussagekräftiger für Experimente mit Delay, BER oder Datarate.

---

### 🎁 Bonus: Wenn du `packetReceivedBytes` benutzt

Falls du anstelle von „Anzahl Pakete“ lieber **Bytes pro Sekunde** analysieren willst (z. B. um Bandbreite zu bewerten):

```python
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
```

---

Sag Bescheid, wenn du auch **UDP vs TCP** vergleichen oder die Auswirkungen von Delay oder BER visualisieren möchtest – ich helfe dir beim Setup!
