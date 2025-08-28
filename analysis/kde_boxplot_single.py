import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("timings_c_vm.csv")
durations = df["Duration (ms)"]

# --- Stats ---
print("=== Full Latency Statistics ===")
print(f"Count      : {len(durations)}")
print(f"Min        : {durations.min():.2f}")
print(f"Max        : {durations.max():.2f}")
print(f"Mean       : {durations.mean():.2f}")
print(f"Median     : {durations.median():.2f}")
print(f"Std Dev    : {durations.std():.2f}")
print(f"95th pct   : {durations.quantile(0.95):.2f}")
print(f"99th pct   : {durations.quantile(0.99):.2f}")
print()

# --- KDE Plot ---
plt.figure(figsize=(10, 6))
sns.kdeplot(durations, fill=True, bw_adjust=0.5)
plt.xlabel("Duration (ms)")
plt.ylabel("Density")
plt.title("Latency Distribution")
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_kde_c_vm.png")
plt.close()

# --- Boxplot ---
plt.figure(figsize=(10, 2))
sns.boxplot(x=durations, color='lightblue', linewidth=1.5)
plt.xlabel("Duration (ms)")
plt.title("Latency Distribution")
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_boxplot_c_vm.png")
plt.close()
