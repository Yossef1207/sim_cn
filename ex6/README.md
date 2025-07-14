
## Task 1 

Simulate your network for 10 seconds, for 100 seconds and for 1000 seconds. After each run, have a look at the application layer throughput over time (Attention: Throughput should be computed as discussed in Exercise 4). What do you notice at the beginning of the simulation? What does your observation mean for the data analysis?

### 1. Simulation for **10 seconds**

* **Observation**: You will mostly see the **Slow Start phase** of TCP.
* Throughput begins low and ramps up exponentially as the congestion window (`cwnd`) increases.
* You might **not reach a stable throughput**.

**Implication**:

* This measurement is **not representative** of long-term TCP performance.
* It reflects **initial connection behavior**, not steady-state.

---

### 2. Simulation for **100 seconds**

* **Observation**: After \~10–20s, TCP enters **Congestion Avoidance**.
* Throughput curve shows the **sawtooth pattern**:

  * Increase → Packet loss → Decrease → Repeat
* The average throughput becomes more stable.

**Implication**:

* This is more representative of real-world application performance.
* Still, the first few seconds can distort averages.

---

### 3. Simulation for **1000 seconds**

* **Observation**:

  * You see **long-term behavior**.
  * Occasional packet losses, recovery (Fast Retransmit), and steady throughput.
  * The **startup phase becomes negligible**.

**Implication**:

* Ideal for accurate data analysis.
* You can **discard the first 10–20 seconds** as "warm-up" (transient phase) to get meaningful results.

---

## Conclusion: What Does This Mean for Data Analysis?

* At the beginning of every TCP simulation, the **Slow Start phase** inflates the throughput ramp-up.
* This **biases short simulations**.
* For meaningful data analysis:

  * **Run long simulations** (≥100s).
  * **Exclude initial seconds** (e.g., first 10–20s) from analysis.
  * Calculate average throughput after warm-up.


