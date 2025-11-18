import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Setup argument parser
parser = argparse.ArgumentParser(description='Plot theta vs time for odometry and particle filter')
parser.add_argument('--files', nargs='+', required=True, help='CSV files for Part5, Part6.1, Part6.2')
args = parser.parse_args()

# File paths from command line
file_list = args.files
if len(file_list) != 3:
    print(f"Warning: Expected 3 files, got {len(file_list)}. Please provide files in order: Part5, Part6.1, Part6.2")
    # Pad with None if not enough files
    while len(file_list) < 3:
        file_list.append(None)

files = {
    'Part5': file_list[0],
    'Part6.1': file_list[1],
    'Part6.2': file_list[2]
}

# First, let's check the actual column names in the first file
print("Checking column names in CSV files...")
for part_name, file_path in files.items():
    if file_path:
        try:
            df_test = pd.read_csv(file_path, nrows=1)
            print(f"\n{part_name} ({file_path}) columns:")
            print(df_test.columns.tolist())
        except Exception as e:
            print(f"Could not read {file_path}: {e}")

print("\n" + "="*60)
print("Starting plots...")
print("="*60 + "\n")

# Create figure with subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Theta (Orientation) vs Time: Odometry vs Particle Filter', fontsize=16, fontweight='bold')

# Plot each part
for idx, (part_name, file_path) in enumerate(files.items()):
    ax = axes[idx]
    
    if not file_path:
        ax.text(0.5, 0.5, f'No file provided for {part_name}', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{part_name} - NO FILE', fontsize=14)
        continue
    
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Check for column names (might have spaces or different naming)
        columns = df.columns.tolist()
        
        # Try to find the right columns (case-insensitive and strip spaces)
        col_map = {}
        for col in columns:
            col_clean = col.strip().lower()
            if 'odom' in col_clean and ('th' in col_clean or 'theta' in col_clean):
                col_map['odom_th'] = col
            elif 'pf' in col_clean and ('th' in col_clean or 'theta' in col_clean):
                col_map['pf_th'] = col
            elif 'stamp' in col_clean or 'time' in col_clean:
                col_map['stamp'] = col
        
        # Extract theta and time
        odom_th = df[col_map['odom_th']]
        pf_th = df[col_map['pf_th']]
        time_stamps = df[col_map['stamp']]
        
        # Convert timestamps to relative time (seconds from start)
        if time_stamps.dtype == 'object' or time_stamps.max() > 1e10:
            # If timestamps are in nanoseconds or large values, normalize them
            time_relative = (time_stamps - time_stamps.iloc[0]) / 1e9  # Convert to seconds
        else:
            time_relative = time_stamps - time_stamps.iloc[0]
        
        # Convert theta to degrees for better readability
        odom_th_deg = np.degrees(odom_th)
        pf_th_deg = np.degrees(pf_th)
        
        # Plot on corresponding subplot
        ax.plot(time_relative, odom_th_deg, 'b-', label='Odometry', linewidth=2, alpha=0.7)
        ax.plot(time_relative, pf_th_deg, 'r-', label='Particle Filter', linewidth=2, alpha=0.7)
        
        # Formatting
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Theta (degrees)', fontsize=12)
        ax.set_title(f'{part_name}', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        print(f"Successfully plotted {part_name}")
        print(f"  Time range: {time_relative.iloc[0]:.2f}s to {time_relative.iloc[-1]:.2f}s")
        print(f"  Odom theta range: {odom_th_deg.min():.2f}° to {odom_th_deg.max():.2f}°")
        print(f"  PF theta range: {pf_th_deg.min():.2f}° to {pf_th_deg.max():.2f}°")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {file_path}")
        ax.text(0.5, 0.5, f'File not found:\n{file_path}', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{part_name} - ERROR', fontsize=14)
    except KeyError as e:
        print(f"Error: Could not find column {e} in {part_name}")
        print(f"Available columns: {columns}")
        ax.text(0.5, 0.5, f'Missing column:\n{str(e)}', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{part_name} - ERROR', fontsize=14)
    except Exception as e:
        print(f"Error processing {part_name}: {str(e)}")
        ax.text(0.5, 0.5, f'Error:\n{str(e)}', 
                ha='center', va='center', transform=ax.transAxes)
        ax.set_title(f'{part_name} - ERROR', fontsize=14)

plt.tight_layout()
plt.savefig('theta_vs_time_comparison.png', dpi=300, bbox_inches='tight')
print("\nPlot saved as 'theta_vs_time_comparison.png'")
plt.show()