import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# List of CSV files to process
csv_files = [
    "timings_c_vm.csv",
    "timings_c_vm_100.csv",
]

labels = [
        "1 pod",
        "100 pods",
]

# First pass: find global min and max across all filtered datasets
global_min = float('inf')
global_max = float('-inf')

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    durations = df["Duration (ms)"]

    # Update global min and max
    global_min = min(global_min, durations.min())
    global_max = max(global_max, durations.max())

# Add some padding to the limits
padding = (global_max - global_min) * 0.05
x_min = max(0, global_min - padding)
x_max = global_max + padding

print(f"Global X-axis range: {x_min:.2f} to {x_max:.2f}")

# Create figure with subplots - vertical arrangement with aligned axes
fig, axes = plt.subplots(len(csv_files), 1, figsize=(10, 4 * len(csv_files)))
fig.suptitle('Latency Distribution Comparison', fontsize=16, y=0.98)

for i, csv_file in enumerate(csv_files):
    # Load CSV
    df = pd.read_csv(csv_file)
    durations = df["Duration (ms)"]
    
    # Create boxplot with aligned x-axis
    sns.boxplot(x=durations, ax=axes[i], color='lightblue', linewidth=1.5)
    axes[i].set_xlabel("Duration (ms)")
    axes[i].set_title(f"Dataset: {labels[i]}")
    axes[i].grid(True)
    
    # Set the same x-axis limits for all plots
    axes[i].set_xlim(x_min, x_max)
    
    # Add vertical grid lines at major intervals for better alignment
    major_ticks = np.arange(np.ceil(x_min / 10) * 10, np.floor(x_max / 10) * 10 + 1, 10)
    axes[i].set_xticks(major_ticks)
    axes[i].grid(True, which='major', axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("combined_latency_boxplots_aligned_2.png", bbox_inches='tight')
plt.close()
