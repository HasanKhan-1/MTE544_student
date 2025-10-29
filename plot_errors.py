import matplotlib.pyplot as plt
from utilities import FileReader
import argparse
import numpy as np


def plot_all_required_plots(filename, target_x=-1.0, target_y=-5.0, controller_name="Controller"):
    
    # Read data
    headers, values = FileReader(filename).read_file()
    
    # Extract data
    x_vals = [row[0] for row in values]
    y_vals = [row[1] for row in values]
    theta_vals = [row[2] for row in values]
    stamp_vals = [row[3] for row in values]
    
    # Convert timestamps to seconds (relative to first timestamp)
    first_stamp = stamp_vals[0]
    time_list = [(stamp - first_stamp) * 1e-9 for stamp in stamp_vals]
    
    # Compute error (Euclidean distance to target)
    e_vals = [np.sqrt((target_x - x)**2 + (target_y - y)**2) 
              for x, y in zip(x_vals, y_vals)]
    
    # Compute error derivative (finite difference)
    edot_vals = [0.0]  # First value is zero
    for i in range(1, len(e_vals)):
        dt = time_list[i] - time_list[i-1]
        if dt > 0:
            edot = (e_vals[i] - e_vals[i-1]) / dt
        else:
            edot = 0.0
        edot_vals.append(edot)
    
    # ========== FIGURE 1: {e-t, edot-t} ==========
    fig1 = plt.figure(figsize=(12, 6))
    plt.plot(time_list, e_vals, label='e (error)', marker='o', linestyle='-', 
             markersize=3, color='blue', markevery=10)
    plt.plot(time_list, edot_vals, label='ė (error derivative)', marker='x', 
             linestyle='--', markersize=3, color='red', markevery=10)
    plt.title(f'{controller_name}: Error and Error Derivative vs. Time', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('Error [m] / Error Rate [m/s]', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # ========== FIGURE 2: {x-t, y-t, theta-t} ==========
    fig2 = plt.figure(figsize=(12, 6))
    plt.plot(time_list, x_vals, label='x', marker='o', linestyle='-', 
             markersize=3, color='blue', markevery=10)
    plt.plot(time_list, y_vals, label='y', marker='s', linestyle='-', 
             markersize=3, color='green', markevery=10)
    plt.plot(time_list, theta_vals, label='θ', marker='^', linestyle='-', 
             markersize=3, color='orange', markevery=10)
    plt.title(f'{controller_name}: States vs. Time', fontsize=14, fontweight='bold')
    plt.xlabel('Time [s]', fontsize=12)
    plt.ylabel('State Values', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # ========== FIGURE 3: {x-y} ==========
    fig3 = plt.figure(figsize=(8, 8))
    plt.plot(x_vals, y_vals, marker='o', linestyle='-', markersize=4, 
             linewidth=2, color='purple', markevery=10)
    plt.plot(x_vals[0], y_vals[0], 'go', markersize=12, label='Start', zorder=5)
    plt.plot(x_vals[-1], y_vals[-1], 'ro', markersize=12, label='End', zorder=5)
    plt.title(f'{controller_name}: X-Y Trajectory', fontsize=14, fontweight='bold')
    plt.xlabel('X [m]', fontsize=12)
    plt.ylabel('Y [m]', fontsize=12)
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    
    # ========== FIGURE 4: {e-edot} ==========
    fig4 = plt.figure(figsize=(8, 6))
    plt.plot(e_vals, edot_vals, marker='o', linestyle='-', markersize=3, 
             linewidth=1.5, color='darkred', markevery=5)
    plt.title(f'{controller_name}: Error Phase Plot (e vs. ė)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('e (error) [m]', fontsize=12)
    plt.ylabel('ė (error derivative) [m/s]', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and plot robot trajectory files.')
    parser.add_argument('--files', nargs='+', required=True, 
                        help='List of CSV files to process')
    parser.add_argument('--names', nargs='+', 
                        help='Controller names corresponding to each file (e.g., "P Controller" "PID Controller")')
    parser.add_argument('--target_x', type=float, default=1.0, 
                        help='Target x position (default: 1.0)')
    parser.add_argument('--target_y', type=float, default=1.0, 
                        help='Target y position (default: 1.0)')
    
    args = parser.parse_args()
    
    if args.names is None:
        controller_names = [f"Controller {i+1}" for i in range(len(args.files))]
    else:
        controller_names = args.names
        if len(controller_names) != len(args.files):
            print("Warning: Number of names doesn't match number of files. Using default names.")
            controller_names = [f"Controller {i+1}" for i in range(len(args.files))]
    
    print("Plotting the files:", args.files)
    print(f"Target position: ({args.target_x}, {args.target_y})")
    
    for filename, name in zip(args.files, controller_names):
        print(f"\nProcessing file: {filename} ({name})")
        plot_all_required_plots(filename, args.target_x, args.target_y, name)
