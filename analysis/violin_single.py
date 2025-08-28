import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load CSV
csv_file = "timings_c_vm_100.csv"  # Change this to your filename
df = pd.read_csv(csv_file)
durations = df["Duration (ms)"]

# --- Full Stats Before Filtering ---
print("=== Full Latency Statistics (Before Filtering) ===")
print(f"Count      : {len(durations)}")
print(f"Min        : {durations.min():.2f}")
print(f"Max        : {durations.max():.2f}")
print(f"Mean       : {durations.mean():.2f}")
print(f"Median     : {durations.median():.2f}")
print(f"Std Dev    : {durations.std():.2f}")
print(f"95th pct   : {durations.quantile(0.95):.2f}")
print(f"99th pct   : {durations.quantile(0.99):.2f}")
print()

# --- Violin Plot ---
plt.figure(figsize=(12, 8))

# Create violin plot
sns.violinplot(x=durations, color='lightblue', linewidth=2, inner='box')  # inner='box' adds a boxplot inside

# Customize the plot
plt.xlabel("Duration (ms)", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.title("Latency Distribution - 100 pods", fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("latency_violinplot_vm_100.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()
