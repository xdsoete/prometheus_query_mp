import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define input files and labels
files = {
    "1 pod": "timings_c.csv",
    "4 pods": "timings_c_4.csv",
    "10 pods": "timings_c_10_2.csv",
    "100 pods": "timings_c_100_2.csv"
}

# Set plot style
sns.set(style="whitegrid")

# Create a figure
plt.figure(figsize=(10, 6))

# Process and plot each dataset
for label, filename in files.items():
    df = pd.read_csv(filename)
    durations = df["Duration (ms)"]

    # Optional: print stats
    # print(f"=== {label}===")
    # print(f"Count      : {len(durations)}")
    # print(f"Min        : {durations.min():.2f}")
    # print(f"Max        : {durations.max():.2f}")
    # print(f"Mean       : {durations.mean():.2f}")
    # print(f"Median     : {durations.median():.2f}")
    # print(f"95th pct   : {durations.quantile(0.95):.2f}")
    # print()

    # Plot KDE
    sns.kdeplot(durations, fill=False, label=label, bw_adjust=0.5, linewidth=2)

# Finalize plot
plt.xlabel("Duration (ms)")
plt.ylabel("Density")
plt.title("Latency Distribution")
plt.legend(title="Data Source")
plt.tight_layout()
plt.savefig("latency_comparison_kde_c_3.png")
plt.close()
